"""
AERO-Swarm: Decentralized Actor and Centralized Critic Networks
Actor networks condition on local physical state and ST-GAT-S sheaf embeddings.
Centralized Critic conditions on global state for CTDE training.
"""

import torch
import torch.nn as nn
from typing import Dict, Tuple


class HeterogeneousActor(nn.Module):
    def __init__(self, raw_state_dim: int, sheaf_emb_dim: int = 128, action_dim: int = 4):
        """
        Action vector: [v_x, v_y, v_z, yaw_rate]
        """
        super().__init__()
        in_dim = raw_state_dim + sheaf_emb_dim
        self.net = nn.Sequential(
            nn.Linear(in_dim, 128),
            nn.LayerNorm(128),
            nn.Tanh(),
            nn.Linear(128, 64),
            nn.Tanh(),
            nn.Linear(64, action_dim * 2) # Mean and log_std for Gaussian policy
        )
        self.action_dim = action_dim

    def forward(self, raw_state: torch.Tensor, sheaf_emb: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x = torch.cat([raw_state, sheaf_emb], dim=-1)
        out = self.net(x)
        mean = torch.tanh(out[..., :self.action_dim]) # Bound normalized actions to [-1, 1]
        log_std = torch.clamp(out[..., self.action_dim:], -2.0, 0.5)
        return mean, log_std

    def sample_action(self, raw_state: torch.Tensor, sheaf_emb: torch.Tensor, deterministic: bool = False):
        mean, log_std = self.forward(raw_state, sheaf_emb)
        if deterministic:
            return mean
        std = torch.exp(log_std)
        eps = torch.randn_like(mean)
        return mean + eps * std


class CentralizedCritic(nn.Module):
    def __init__(self, global_state_dim: int, hidden_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(global_state_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, global_state: torch.Tensor) -> torch.Tensor:
        return self.net(global_state).squeeze(-1)
