"""
AERO-Swarm: Spatio-Temporal Graph Attention Network on Sheaves (ST-GAT-S)
PyTorch implementation of Sheaf GNN with SE(3)-equivariant restriction maps,
multi-head attention gated by RF link integrity gamma_{ij}(t), and temporal GRU aggregation.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple


class SheafAttentionLayer(nn.Module):
    def __init__(self, in_features_dict: Dict[int, int], out_dim: int = 64, 
                 edge_dim: int = 6, num_heads: int = 4):
        """
        Args:
            in_features_dict: Dict mapping drone type -> raw stalk dimension
            out_dim: Dimension of latent node embedding
            edge_dim: Shared edge stalk dimension (6D: Pos + Vel)
            num_heads: Number of attention heads
        """
        super().__init__()
        self.out_dim = out_dim
        self.edge_dim = edge_dim
        self.num_heads = num_heads
        self.head_dim = out_dim // num_heads
        
        # Type-specific linear projections to uniform latent dimension
        self.type_projectors = nn.ModuleDict({
            str(t): nn.Linear(dim, out_dim) for t, dim in in_features_dict.items()
        })
        
        # Learnable SE(3)-equivariant restriction maps for each drone type
        # Maps from latent space out_dim to edge_dim
        self.restriction_maps = nn.ParameterDict({
            str(t): nn.Parameter(torch.randn(edge_dim, out_dim) * 0.1) 
            for t in in_features_dict.keys()
        })
        
        # Attention parameter vectors
        self.attn_src = nn.Parameter(torch.randn(num_heads, self.head_dim))
        self.attn_dst = nn.Parameter(torch.randn(num_heads, self.head_dim))
        self.attn_edge = nn.Parameter(torch.randn(num_heads, 1))
        
        self.leaky_relu = nn.LeakyReLU(0.2)
        self.W_out = nn.Linear(out_dim, out_dim)

    def forward(self, node_features: List[torch.Tensor], 
                node_types: List[int], 
                edge_index: torch.Tensor, 
                edge_weights: torch.Tensor) -> torch.Tensor:
        """
        Args:
            node_features: List of N tensors with variable stalk dimensions
            node_types: List of length N with integer types (0, 1, 2)
            edge_index: Tensor of shape (2, E)
            edge_weights: Tensor of shape (E,) with link integrities gamma in [0, 1]
        """
        num_nodes = len(node_features)
        device = node_features[0].device
        
        # 1. Project variable-length node stalks to uniform latent dimension
        h = torch.zeros(num_nodes, self.out_dim, device=device)
        for i in range(num_nodes):
            t_str = str(node_types[i])
            h[i] = self.type_projectors[t_str](node_features[i])
            
        if edge_index.size(1) == 0:
            return self.W_out(h)
            
        src, dst = edge_index[0], edge_index[1]
        
        # 2. Sheaf message transport across edge stalks:
        # m_{j -> i} = P_{i <| e}^T @ P_{j <| e} @ h_j
        num_edges = edge_index.size(1)
        transported_msgs = torch.zeros(num_edges, self.out_dim, device=device)
        
        for e in range(num_edges):
            u, v = src[e].item(), dst[e].item()
            t_u, t_v = str(node_types[u]), str(node_types[v])
            P_u = self.restriction_maps[t_u] # (edge_dim, out_dim)
            P_v = self.restriction_maps[t_v] # (edge_dim, out_dim)
            
            # Transport operator across edge stalk
            transport_op = P_v.t() @ P_u # (out_dim, out_dim)
            gamma = edge_weights[e]
            transported_msgs[e] = gamma * (transport_op @ h[u])
            
        # 3. Multi-Head Attention over transported messages
        h_reshaped = h.view(num_nodes, self.num_heads, self.head_dim)
        msg_reshaped = transported_msgs.view(num_edges, self.num_heads, self.head_dim)
        
        # Compute attention logits
        alpha_src = (h_reshaped[dst] * self.attn_dst).sum(dim=-1) # (E, num_heads)
        alpha_msg = (msg_reshaped * self.attn_src).sum(dim=-1)    # (E, num_heads)
        alpha_gamma = edge_weights.unsqueeze(-1) * self.attn_edge.squeeze(-1)
        
        alpha = self.leaky_relu(alpha_src + alpha_msg + alpha_gamma)
        
        # Softmax normalization per target node
        alpha_exp = torch.exp(alpha)
        denom = torch.zeros(num_nodes, self.num_heads, device=device)
        denom.index_add_(0, dst, alpha_exp)
        denom = denom.clamp(min=1e-6)
        alpha_norm = alpha_exp / denom[dst] # (E, num_heads)
        
        # 4. Message aggregation
        out_heads = torch.zeros(num_nodes, self.num_heads, self.head_dim, device=device)
        weighted_msgs = msg_reshaped * alpha_norm.unsqueeze(-1)
        out_heads.index_add_(0, dst, weighted_msgs)
        
        out = out_heads.view(num_nodes, self.out_dim)
        return F.elu(self.W_out(out + h)) # Residual skip connection


class STGATSNetwork(nn.Module):
    def __init__(self, in_features_dict: Dict[int, int] = None, 
                 hidden_dim: int = 64, out_embedding_dim: int = 128):
        """
        Complete Spatio-Temporal Graph Attention Network on Sheaves.
        """
        super().__init__()
        if in_features_dict is None:
            in_features_dict = {0: 24, 1: 12, 2: 6}
            
        self.sheaf_layer1 = SheafAttentionLayer(in_features_dict, hidden_dim)
        self.sheaf_layer2 = SheafAttentionLayer({t: hidden_dim for t in in_features_dict}, hidden_dim)
        self.gru = nn.GRUCell(hidden_dim, out_embedding_dim)
        self.out_embedding_dim = out_embedding_dim

    def forward(self, node_features: List[torch.Tensor], 
                node_types: List[int], 
                edge_index: torch.Tensor, 
                edge_weights: torch.Tensor, 
                prev_hidden: torch.Tensor = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass producing spatio-temporal representations.
        """
        # Layer 1 Sheaf Attention
        z1 = self.sheaf_layer1(node_features, node_types, edge_index, edge_weights)
        # Layer 2 Sheaf Attention
        z1_list = [z1[i] for i in range(len(node_features))]
        z2 = self.sheaf_layer2(z1_list, node_types, edge_index, edge_weights)
        
        # Temporal GRU update
        num_nodes = len(node_features)
        if prev_hidden is None:
            prev_hidden = torch.zeros(num_nodes, self.out_embedding_dim, device=z2.device)
            
        h_next = self.gru(z2, prev_hidden)
        return h_next, h_next
