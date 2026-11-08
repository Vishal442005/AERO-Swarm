"""
Unit tests for Cellular Sheaf and Bochner-Weitzenböck Curvature Decomposition
"""

import pytest
import numpy as np
from src.core.sheaf import CellularSheaf, DroneType, STALK_DIMS, EDGE_STALK_DIM


def test_sheaf_initialization():
    drone_types = [DroneType.LEADER, DroneType.SCOUT, DroneType.RELAY]
    sheaf = CellularSheaf(3, drone_types)
    
    assert sheaf.num_nodes == 3
    assert sheaf.stalk_dims == [24, 12, 8]
    assert sheaf.total_dim == 24 + 12 + 8
    assert sheaf.edge_dim == EDGE_STALK_DIM
    assert sheaf.offsets == [0, 24, 36, 44]


def test_restriction_maps_dimensions():
    drone_types = [DroneType.LEADER, DroneType.SCOUT, DroneType.RELAY]
    sheaf = CellularSheaf(3, drone_types)
    
    for t in [DroneType.LEADER, DroneType.SCOUT, DroneType.RELAY]:
        P = sheaf.base_restriction_maps[t]
        assert P.shape == (EDGE_STALK_DIM, STALK_DIMS[t])
        # Position and velocity identities
        assert np.allclose(P[0:3, 0:3], np.eye(3))
        assert np.allclose(P[3:6, 3:6], np.eye(3))


def test_sheaf_laplacian_properties():
    drone_types = [DroneType.LEADER, DroneType.SCOUT, DroneType.RELAY]
    sheaf = CellularSheaf(3, drone_types)
    edges = [(0, 1), (1, 2), (0, 2)]
    integrities = {(0, 1): 0.9, (1, 2): 0.8, (0, 2): 0.95}
    
    L_sheaf, L_boch, ric = sheaf.build_sheaf_laplacian(edges, integrities)
    
    # 1. Symmetry
    assert np.allclose(L_sheaf, L_sheaf.T, atol=1e-6)
    
    # 2. Positive Semi-Definiteness (all eigenvalues >= -1e-6)
    eigvals = np.linalg.eigvalsh(L_sheaf)
    assert np.all(eigvals >= -1e-6)
    
    # 3. Bochner decomposition: L_sheaf = L_boch + ric
    assert np.allclose(L_sheaf, L_boch + ric, atol=1e-6)


def test_scvi_curvature_computation():
    drone_types = [DroneType.LEADER, DroneType.SCOUT, DroneType.RELAY]
    sheaf = CellularSheaf(3, drone_types)
    edges = [(0, 1), (1, 2)]
    integrities = {(0, 1): 0.9, (1, 2): 0.8}
    
    _, _, ric = sheaf.build_sheaf_laplacian(edges, integrities)
    scvi = sheaf.compute_curvature_vulnerability(ric)
    
    assert len(scvi) == 3
    assert np.all(np.isfinite(scvi))
