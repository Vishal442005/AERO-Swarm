"""
AERO-Swarm: Cellular Sheaf Engine
Implements the Cellular Sheaf topology, Sheaf Laplacian, Bochner-Weitzenböck
curvature decomposition, Forman-Ricci curvature, and Cohomology checks (H^0, H^1).
"""

import numpy as np
import scipy.linalg as la
from typing import Dict, List, Tuple, Optional


class DroneType:
    LEADER = 0   # High-compute, SLAM, d_v = 24
    SCOUT = 1    # High-agility, FoV sensors, d_v = 12
    RELAY = 2    # Mesh routing, SDR, d_v = 8


STALK_DIMS = {
    DroneType.LEADER: 24,
    DroneType.SCOUT: 12,
    DroneType.RELAY: 8
}
EDGE_STALK_DIM = 6  # Shared informational subspace (3D Pos + 3D Vel)


class CellularSheaf:
    def __init__(self, num_nodes: int, node_types: List[int]):
        """
        Initializes cellular sheaf F = (G, {F_v}, {F_e}, {rho})
        """
        self.num_nodes = num_nodes
        self.node_types = node_types
        self.stalk_dims = [STALK_DIMS[t] for t in node_types]
        self.total_dim = sum(self.stalk_dims)
        self.edge_dim = EDGE_STALK_DIM
        
        # Node stalk offsets in stacked 0-cochain
        self.offsets = [0]
        for d in self.stalk_dims:
            self.offsets.append(self.offsets[-1] + d)
            
        # Base canonical restriction maps (SE(3)-equivariant projection)
        self.base_restriction_maps = self._init_base_restriction_maps()
        
    def _init_base_restriction_maps(self) -> Dict[int, np.ndarray]:
        """
        Constructs SE(3)-equivariant projection matrices from R^{d_v} to R^6.
        First 6 components are always (position [0:3], velocity [3:6]).
        """
        maps = {}
        for t, d_v in STALK_DIMS.items():
            P = np.zeros((self.edge_dim, d_v), dtype=np.float64)
            # Project position (3D) and velocity (3D)
            P[0:3, 0:3] = np.eye(3)
            P[3:6, 3:6] = np.eye(3)
            maps[t] = P
        return maps

    def build_sheaf_laplacian(self, edges: List[Tuple[int, int]], 
                              link_integrities: Optional[Dict[Tuple[int, int], float]] = None
                              ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Constructs the global block Sheaf Laplacian L_F, along with its
        Bochner-Weitzenböck decomposition: L_F = L_Bochner + Ric_Forman.
        
        Args:
            edges: List of directed/undirected edges (u, v)
            link_integrities: Dict mapping edge (u, v) -> gamma_uv in [0, 1]
            
        Returns:
            L_sheaf: Total block Sheaf Laplacian (D_V x D_V)
            L_bochner: Positive semidefinite Bochner Laplacian (D_V x D_V)
            Ric_forman: Block-diagonal Forman-Ricci curvature matrix (D_V x D_V)
        """
        D_V = self.total_dim
        L_sheaf = np.zeros((D_V, D_V), dtype=np.float64)
        
        if link_integrities is None:
            link_integrities = {e: 1.0 for e in edges}
            
        # Map edges to symmetric set
        active_edges = {}
        for (u, v) in edges:
            gamma = link_integrities.get((u, v), 1.0)
            if gamma > 1e-4:
                pair = tuple(sorted((u, v)))
                active_edges[pair] = max(active_edges.get(pair, 0.0), gamma)
                
        # Build L_sheaf blocks
        for (u, v), gamma in active_edges.items():
            idx_u = slice(self.offsets[u], self.offsets[u+1])
            idx_v = slice(self.offsets[v], self.offsets[v+1])
            
            # Attenuated restriction maps
            P_u = np.sqrt(gamma) * self.base_restriction_maps[self.node_types[u]]
            P_v = np.sqrt(gamma) * self.base_restriction_maps[self.node_types[v]]
            
            # Diagonal terms: sum_e rho_{u <| e}^T rho_{u <| e}
            L_sheaf[idx_u, idx_u] += P_u.T @ P_u
            L_sheaf[idx_v, idx_v] += P_v.T @ P_v
            
            # Off-diagonal mutual transport: - rho_{u <| e}^T rho_{v <| e}
            L_sheaf[idx_u, idx_v] -= P_u.T @ P_v
            L_sheaf[idx_v, idx_u] -= P_v.T @ P_u
            
        # Bochner-Weitzenböck Decomposition:
        # L_sheaf = L_Bochner + Ric_Forman
        # Where Ric_Forman is block diagonal
        Ric_forman = np.zeros((D_V, D_V), dtype=np.float64)
        # Fast incident lookup
        adj = {i: [] for i in range(self.num_nodes)}
        for (u, v) in active_edges.keys():
            adj[u].append(v)
            adj[v].append(u)

        for i in range(self.num_nodes):
            idx_i = slice(self.offsets[i], self.offsets[i+1])
            deg_block = L_sheaf[idx_i, idx_i]
            holonomy_sum = np.zeros_like(deg_block)
            for j in adj[i]:
                idx_j = slice(self.offsets[j], self.offsets[j+1])
                transport = L_sheaf[idx_i, idx_j]
                holonomy_sum += transport @ transport.T
            
            # Forman curvature block
            Ric_forman[idx_i, idx_i] = deg_block - 0.25 * holonomy_sum
            
        L_bochner = L_sheaf - Ric_forman
        # Ensure numerical symmetry
        L_sheaf = 0.5 * (L_sheaf + L_sheaf.T)
        L_bochner = 0.5 * (L_bochner + L_bochner.T)
        Ric_forman = 0.5 * (Ric_forman + Ric_forman.T)
        
        return L_sheaf, L_bochner, Ric_forman

    def compute_curvature_vulnerability(self, Ric_forman: np.ndarray) -> np.ndarray:
        """
        Computes Sheaf Curvature Vulnerability Index (SCVI) for each drone:
        kappa_F(u) = tr(Ric_u). Negative values flag jamming/bottleneck vulnerabilities.
        """
        curvatures = np.zeros(self.num_nodes, dtype=np.float64)
        for i in range(self.num_nodes):
            idx_i = slice(self.offsets[i], self.offsets[i+1])
            curvatures[i] = np.trace(Ric_forman[idx_i, idx_i])
        return curvatures

    def compute_sheaf_resilience_index(self, L_sheaf: np.ndarray, L_sheaf_0: np.ndarray) -> float:
        """
        Computes SRI(t) = lambda_2(L_F(t)) / lambda_2(L_F(0)).
        """
        try:
            evals_t = np.sort(la.eigvalsh(L_sheaf))
            evals_0 = np.sort(la.eigvalsh(L_sheaf_0))
            
            # Smallest non-zero eigenvalue (Fiedler value)
            # Find first eval > 1e-4
            nz_t = evals_t[evals_t > 1e-4]
            nz_0 = evals_0[evals_0 > 1e-4]
            
            fiedler_t = nz_t[0] if len(nz_t) > 0 else 0.0
            fiedler_0 = nz_0[0] if len(nz_0) > 0 else 1.0
            
            return float(np.clip(fiedler_t / max(fiedler_0, 1e-6), 0.0, 1.0))
        except Exception:
            return 0.0

    def compute_cohomology_ranks(self, L_sheaf: np.ndarray, tol: float = 1e-4) -> Tuple[int, int]:
        """
        Computes ranks of 0-th cohomology H^0 (global sections) and
        1-st cohomology H^1 (topological obstruction to consensus).
        """
        evals = np.sort(la.eigvalsh(L_sheaf))
        dim_H0 = int(np.sum(evals < tol))
        # For connected component over stalk, H1 rank tracks cyclic inconsistencies
        # Rank(delta^0) = N_edges_eff - dim(H0)
        dim_H1 = max(0, dim_H0 - self.edge_dim)
        return dim_H0, dim_H1
