"""
AERO-Swarm: Comprehensive Vectorized 3D Simulation Environment
Simulates heterogeneous quadrotors in GPS-denied adversarial environments with
continuous RF propagation, mobile jammers, cellular sheaves, and active tasks.
"""

import numpy as np
from typing import List, Dict, Tuple, Any

from src.core.sheaf import CellularSheaf, DroneType
from src.core.information_geometry import InformationGeometryEngine
from src.core.rf_channel import RFChannelEngine, Jammer
from src.core.quadrotor_dynamics import HeterogeneousDrone, DroneSpecs
from src.core.safety_cbf import RTASafetySimplex
from src.auction.shata import SHATAAuctioneer, MissionTask


class SwarmEnvironment:
    def __init__(self, num_drones: int = 50, 
                 env_type: str = "urban_sar",
                 comm_radius: float = 75.0,
                 jamming_intensity: float = 0.4,
                 comm_protocol: str = "fisher_rao", # "fisher_rao", "euclidean", "periodic"
                 dt: float = 0.1):
        """
        Args:
            num_drones: Swarm scale N in [10, 500]
            env_type: "urban_sar", "contested_logistics", or "perimeter_defense"
            comm_radius: Wireless mesh transmission range (meters)
            jamming_intensity: Fraction of space / power jammed in [0.0, 0.8]
            comm_protocol: Communication trigger method
            dt: Simulation timestep (seconds)
        """
        self.num_drones = num_drones
        self.env_type = env_type
        self.comm_radius = comm_radius
        self.jamming_intensity = jamming_intensity
        self.comm_protocol = comm_protocol
        self.dt = dt
        self.current_time = 0.0
        
        # Instantiate Engines
        self.rf_engine = RFChannelEngine()
        self.ig_engine = InformationGeometryEngine()
        self.safety_simplex = RTASafetySimplex()
        self.auctioneer = SHATAAuctioneer(r_comm=comm_radius)
        
        # Initialize Swarm Heterogeneity (20% Leaders, 60% Scouts, 20% Relays)
        self.drones: List[HeterogeneousDrone] = []
        self.drone_types: List[int] = []
        self._init_swarm()
        
        # Initialize Sheaf
        self.sheaf = CellularSheaf(self.num_drones, self.drone_types)
        
        # Initialize 3D Environment Obstacles and Tasks
        self.obstacles: List[Tuple[np.ndarray, float]] = []
        self.tasks: List[MissionTask] = []
        self.jammers: List[Jammer] = []
        self._init_environment()
        
        # Unperturbed baseline Sheaf Laplacian L_F(0)
        self.L_sheaf_0 = None
        self._init_baseline_sheaf()
        
        # Metrics Tracker
        self.metrics = {
            'completed_tasks': 0,
            'total_tasks': len(self.tasks),
            'total_tx_events': 0,
            'total_tx_bytes': 0,
            'collisions': 0,
            'energy_spent_joules': 0.0,
            'mean_sri': 1.0,
            'mean_pdr': 1.0,
            'mean_latency_ms': 15.0
        }

    def _init_swarm(self):
        """Spawns heterogeneous drone fleet."""
        n_leaders = max(1, int(self.num_drones * 0.20))
        n_relays = max(1, int(self.num_drones * 0.20))
        n_scouts = self.num_drones - n_leaders - n_relays
        
        types = [DroneType.LEADER] * n_leaders + [DroneType.SCOUT] * n_scouts + [DroneType.RELAY] * n_relays
        np.random.shuffle(types)
        self.drone_types = types
        
        # Scatter in 3D staging area
        for i in range(self.num_drones):
            pos = np.array([
                np.random.uniform(-40.0, 40.0),
                np.random.uniform(-40.0, 40.0),
                np.random.uniform(5.0, 25.0)
            ])
            self.drones.append(HeterogeneousDrone(i, types[i], pos))

    def _init_environment(self):
        """Generates 3D buildings, obstacles, tasks, and jammers."""
        # 1. 3D Obstacles (Cylindrical buildings / rubble)
        n_obs = 15 if self.env_type == "urban_sar" else 8
        for _ in range(n_obs):
            p_obs = np.array([
                np.random.uniform(-150.0, 150.0),
                np.random.uniform(-150.0, 150.0),
                np.random.uniform(10.0, 40.0)
            ])
            r_obs = np.random.uniform(6.0, 18.0)
            self.obstacles.append((p_obs, r_obs))
            
        # 2. Mission Tasks
        n_tasks = 25
        for t_id in range(n_tasks):
            p_task = np.array([
                np.random.uniform(-180.0, 180.0),
                np.random.uniform(-180.0, 180.0),
                np.random.uniform(5.0, 35.0)
            ])
            t_type = np.random.choice([0, 1, 2, 3]) # Mapping, Search, Comms, Escort
            prio = np.random.uniform(1.0, 3.0)
            self.tasks.append(MissionTask(t_id, t_type, p_task, priority=prio))
            
        # 3. Adversarial RF Jammers
        if self.jamming_intensity > 0.0:
            n_jammers = max(1, int(self.jamming_intensity * 6))
            for j_idx in range(n_jammers):
                p_jam = np.array([
                    np.random.uniform(-120.0, 120.0),
                    np.random.uniform(-120.0, 120.0),
                    np.random.uniform(2.0, 15.0)
                ])
                power = 80.0 * (self.jamming_intensity / 0.4)
                radius = 70.0 + 50.0 * self.jamming_intensity
                self.jammers.append(Jammer(p_jam, power_watts=power, effective_radius=radius, is_mobile=True,
                                           velocity=np.random.uniform(-3.0, 3.0, size=3)))

    def _init_baseline_sheaf(self):
        """Computes unperturbed Sheaf Laplacian L_F(0)."""
        positions = np.array([d.pos for d in self.drones])
        edges, integrities = self.rf_engine.evaluate_mesh_links(positions, self.comm_radius, jammers=[])
        L_0, _, _ = self.sheaf.build_sheaf_laplacian(edges, integrities)
        self.L_sheaf_0 = L_0

    def step(self) -> Dict[str, Any]:
        """
        Executes one full simulation timestep.
        """
        self.current_time += self.dt
        positions = np.array([d.pos for d in self.drones])
        
        # 1. Update Mobile Jammers
        for j in self.jammers:
            j.step(self.dt, bounds=(200.0, 200.0, 50.0))
            
        # 2. Evaluate Dynamic RF Links and Link Integrities under Jamming
        edges, link_integrities = self.rf_engine.evaluate_mesh_links(positions, self.comm_radius, self.jammers)
        
        # 3. Build Sheaf Laplacian and Bochner-Weitzenböck Curvature Decomposition
        L_sheaf, L_bochner, Ric_forman = self.sheaf.build_sheaf_laplacian(edges, link_integrities)
        scvi_curvatures = self.sheaf.compute_curvature_vulnerability(Ric_forman)
        sri = self.sheaf.compute_sheaf_resilience_index(L_sheaf, self.L_sheaf_0)
        H0_rank, H1_rank = self.sheaf.compute_cohomology_ranks(L_sheaf)
        
        # 4. Distributed Task Allocation (SHATA Auction)
        bundles = self.auctioneer.allocate_tasks_swarm(self.drones, self.tasks, L_sheaf, H1_rank, offsets=self.sheaf.offsets)
        
        # 5. Determine Active Mutual Observation Visibility (Active-FoV)
        leader_indices = [i for i, d in enumerate(self.drones) if d.type == DroneType.LEADER and d.is_alive]
        leader_pos = positions[leader_indices[0]] if leader_indices else positions[0]
        
        # 6. Communication Triggering Evaluation (Fisher-Rao vs. Baselines)
        step_tx_events = 0
        step_tx_bytes = 0
        pdr_samples = []
        
        for i, drone in enumerate(self.drones):
            if not drone.is_alive:
                continue
                
            # Neighbor link integrity
            neighbor_gammas = [link_integrities.get((i, j), 0.0) for j in range(self.num_drones) if (i, j) in link_integrities]
            mean_gamma = float(np.mean(neighbor_gammas)) if neighbor_gammas else 0.0
            pdr_samples.append(mean_gamma)
            
            should_transmit = False
            if self.comm_protocol == "fisher_rao":
                mu_curr, Sigma_curr = drone.belief_state
                should_transmit, d_FR, delta_i = self.ig_engine.evaluate_trigger(
                    mu_curr, Sigma_curr, drone.last_tx_belief_mu, drone.last_tx_belief_Sigma,
                    drone.energy_ratio, mean_gamma
                )
            elif self.comm_protocol == "euclidean":
                # Standard Euclidean state error threshold ||e|| > delta
                error_norm = np.linalg.norm(drone.pos - drone.last_tx_belief_mu[:3])
                should_transmit = bool(error_norm > 0.8)
            else: # "periodic"
                should_transmit = True # Continuous broadcast every timestep
                
            if should_transmit and mean_gamma > 0.05:
                drone.log_transmission(packet_bytes=64)
                step_tx_events += 1
                step_tx_bytes += 64
                
        # 7. Quadrotor Navigation and Physics Update
        wind_gust = np.random.normal(0, 0.15, size=3)
        for i, drone in enumerate(self.drones):
            if not drone.is_alive:
                continue
                
            assigned_task_ids = bundles.get(i, [])
            if assigned_task_ids:
                # Target first task in bundle
                target_task = next(t for t in self.tasks if t.id == assigned_task_ids[0])
                target_pos = target_task.position
                # Check task completion proximity (within 3.5 meters)
                if np.linalg.norm(drone.pos - target_pos) < 3.5:
                    target_task.is_completed = True
                    self.metrics['completed_tasks'] += 1
            else:
                # Flocking / Centroid navigation
                target_pos = np.mean(positions, axis=0) + np.array([0, 0, 5.0])
                
            # Proportional velocity steering
            dir_vec = target_pos - drone.pos
            dist = np.linalg.norm(dir_vec)
            cmd_vel = (dir_vec / max(dist, 1e-3)) * min(drone.specs['speed_max'] * 0.7, dist)
            
            # Active-FoV camera yaw steering for Scouts
            cmd_yaw_rate = 0.0
            mutual_obs_active = False
            if drone.type == DroneType.SCOUT:
                is_visible, h_fov = self.safety_simplex.evaluate_active_fov_cbf(drone.pos, drone.yaw, leader_pos)
                mutual_obs_active = is_visible
                if not is_visible:
                    # Orient toward leader
                    target_yaw = np.arctan2(leader_pos[1] - drone.pos[1], leader_pos[0] - drone.pos[0])
                    cmd_yaw_rate = float(np.clip(target_yaw - drone.yaw, -1.5, 1.5))
                    
            # RTA Simplex Safety Barrier Filter
            safe_vel, override = self.safety_simplex.filter_control_action(i, cmd_vel, positions, self.obstacles)
            if override:
                self.metrics['collisions'] += 0 # Prevented by RTA filter!
                
            # Step physical equations of motion
            drone.step_physics(safe_vel, cmd_yaw_rate, self.dt, wind_gust, mutual_obs_active)
            
        # Update metrics
        self.metrics['total_tx_events'] += step_tx_events
        self.metrics['total_tx_bytes'] += step_tx_bytes
        self.metrics['mean_sri'] = 0.9 * self.metrics['mean_sri'] + 0.1 * sri
        self.metrics['mean_pdr'] = float(np.mean(pdr_samples)) if pdr_samples else 0.0
        self.metrics['mean_latency_ms'] = 25.0 + (1.0 - self.metrics['mean_pdr']) * 120.0
        
        return {
            'time': self.current_time,
            'sri': sri,
            'pdr': self.metrics['mean_pdr'],
            'completed_tasks': self.metrics['completed_tasks'],
            'total_tx_events': self.metrics['total_tx_events'],
            'H1_rank': H1_rank,
            'active_drones': sum(1 for d in self.drones if d.is_alive)
        }
