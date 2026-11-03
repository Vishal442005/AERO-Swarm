# Submission Cover Letter: Elsevier (Swarm and Evolutionary Computation / Robotics and Autonomous Systems)

**Date:** November 3, 2026  
**To:** The Editors-in-Chief  
*Swarm and Evolutionary Computation* / *Robotics and Autonomous Systems* (Elsevier)  
**From:** Autonomous Robotics Swarm Research Consortium  
**Subject:** Submission of Original Research Article titled **"AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments"**

---

Dear Editors-in-Chief and Editorial Board,

We are delighted to submit our original research manuscript entitled **"AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments"** for publication in *Swarm and Evolutionary Computation* (or *Robotics and Autonomous Systems*).

### Context and Motivation
Autonomous multi-robot and aerial drone swarms are critical for large-scale subterranean exploration, civilian search-and-rescue (SAR), and disaster response in contested or GPS-denied environments. In these scenarios, deploying homogeneous fleets is inherently sub-optimal: operational efficiency demands functional heterogeneity (agile monocular scouts, heavy 3D LiDAR mapping leaders, and long-range SDR communications relays). However, existing swarm consensus protocols (e.g. Olfati-Saber flocking) and decentralized task allocation algorithms (e.g. CBBA) rely on scalar graph models $G=(V, E)$, which fail catastrophically under dimensional observation mismatches and electronic warfare (EW) signal jamming.

### Key Innovations and Contributions
In this article, we propose **AERO-Swarm** (*Adaptive Edge-Resilient Optimization for Heterogeneous Swarms*), combining cellular sheaf theory, discrete differential geometry, information geometry, and decentralized auction optimization:
1. **Heterogeneous Cellular Sheaf Coordination:** We introduce the first cellular sheaf architecture for 6-DoF aerial swarms, explicitly modeling vertex stalks $\mathcal{F}_v = \mathbb{R}^{d_v}$ for diverse robotic platforms and edge stalks $\mathcal{F}_e = \mathbb{R}^{d_e}$ connected via continuous, SINR-aware restriction maps $\rho_{v \trianglelefteq e}(t)$.
2. **Bochner--Weitzenb\"ock Curvature & Zero-Percolation-Threshold Resilience:** We establish a discrete Bochner decomposition $\mathbf{L}_\mathcal{F} = \mathbf{L}_\mathcal{F}^{\mathrm{Bochner}} + \mathbf{Ric}_\mathcal{F}^{\mathrm{Forman}}$ that proactively flags jamming bottlenecks through a Sheaf Curvature Vulnerability Index (SCVI). We prove (Theorem 2) that the swarm resilience index degrades strictly linearly under link jamming ($\mathrm{SRI} \geq \mathrm{SRI}_0(1 - c f_{\mathrm{jam}})$), completely eliminating the catastrophic percolation threshold of classical graph Laplacians.
3. **Fisher-Rao Information-Geometric Event Triggering (IG-ETC):** Transmissions are triggered if and only if the Fisher-Rao Riemannian distance on the Gaussian belief manifold exceeds an energy-attenuated threshold $d_{\mathrm{FR}}^2(p_1, p_2) \geq \delta_i(E_i, \bar{\gamma}_i)$, slashing inter-drone wireless bandwidth by up to $79.7\%$.
4. **Sheaf Heterogeneous Auction for Task Allocation (SHATA):** We design the SHATA auction algorithm for decentralized bundle allocation over sheaf stalks, proving polynomial-time convergence $\mathcal{O}(|V| \cdot M \cdot D_G)$ across heterogeneous drone capabilities.
5. **Dual-Tier Validation (Large-Scale Fleet Sweeps + ROS 2 Humble Flight Stack):**
   - Tier-1 evaluates scalability across $N=10$ to $200$ drones, progressive RF jamming sweeps ($0\%$ to $80\%$), and sudden node destruction ($10\%$ to $50\%$). AERO-Swarm achieves $>91.3\%$ task completion rate under $60\%$ severe link jamming where classical CBBA and flat graph consensus collapse below $24\%$.
   - Tier-2 implements a production-grade ROS 2 Humble node architecture integrated with a hardware-isolated Run-Time Assurance (RTA) Safety Simplex monitor, achieving zero safety violations ($N_{\mathrm{viol}} = 0$) in cluttered 3D obstacle fields with sub-$1.2\,\mathrm{ms}$ fallback intervention.

### Alignment with the Journal Scope
This article directly intersects the core objectives of both *Swarm and Evolutionary Computation* and *Robotics and Autonomous Systems*:
- Advances distributed swarm intelligence, decentralized task scheduling, and heuristic multi-robot optimization;
- Bridges mathematical graph and sheaf theory with realistic ROS 2 robotics deployment, real-time loop guarantees, and flight autopilot integration;
- Directly references and benchmarks against recent high-impact articles in SWEVO (*2606.26164*, *2506.23734*, *2512.19321*) and RAS (*2304.03057*, *2610.35582*, *2407.07409*, *2209.10513*).

### Declarations
- The manuscript is original, has not been published previously, and is not concurrently submitted elsewhere.
- All authors have reviewed and approved the manuscript for submission.
- All benchmark suites, evaluation scripts, and ROS 2 packages are fully reproducible and open-source.

We look forward to hearing from you and hope that this work will be of strong interest to the readership.

Sincerely,  
**Autonomous Robotics Swarm Research Consortium**  
Division of Robotics and Autonomous Systems  
Autonomous Multi-Agent Robotics Laboratory  
Contact Email: `research@autonomous-swarms.org`
