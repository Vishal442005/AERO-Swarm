# AERO-Swarm v1.0.0: Resilient Heterogeneous Drone Swarm Framework

**AERO-Swarm (Adaptive Edge-Resilient Optimization for Heterogeneous Swarms)** is an open-source, mathematically grounded, and production-ready coordination stack for large-scale heterogeneous aerial drone swarms in GPS-denied, contested, and electronically jammed environments.

## Highlights of this Release
- **Cellular Sheaf Network Kernel:** Formulates heterogeneous 6-DoF drone coordination over dynamic cellular sheaves, reconciling asymmetric platform state stalks ($\mathcal{F}_v = \mathbb{R}^{d_v}$) into edge stalks ($\mathcal{F}_e = \mathbb{R}^6$) via learnable, SINR-adaptive restriction maps $\rho_{v \trianglelefteq e}(t)$.
- **Bochner--Weitzenböck SCVI Curvature:** Decomposes the Sheaf Laplacian into connection diffusion and Forman Ricci curvature ($\mathbf{L}_\mathcal{F} = \mathbf{L}_\mathcal{F}^{\mathrm{Bochner}} + \mathbf{Ric}_\mathcal{F}$), proving strictly linear degradation ($\mathrm{SRI} \geq \mathrm{SRI}_0(1 - c f_{\mathrm{jam}})$) and eliminating the catastrophic percolation threshold of classical graph Laplacians.
- **Fisher-Rao Riemannian Event-Triggered Communication (IG-ETC):** Suppresses redundant wireless broadcasts by up to $79.7\%$ by gating transmissions on the Riemannian statistical divergence on the Gaussian belief manifold $\mathcal{P}_+^6$.
- **SHATA Decentralized Task Allocation:** Solves multi-robot auction bundles over sheaf cochains with polynomial runtime $\mathcal{O}(|V| \cdot M \cdot D_G)$.
- **Dual-Tier System & ROS 2 Humble Stack:** Includes vectorized 12-vCPU parallelized benchmark engines ($N=10$ to $200$ UAVs) and full ROS 2 Humble packages (`aero_swarm_ros2`) with hardware-isolated Run-Time Assurance (RTA) Safety Simplex barrier monitors ($<1.2\,\mathrm{ms}$ override latency, zero safety violations).
- **Butterfly Architecture Flowchart:** Features a comprehensive, publication-grade butterfly flowchart visualizing inflow threat dynamics, central decision kernels, and decentralized flight execution.

## Repository Contents
- `src/`: Core mathematical modules (Cellular Sheaves, Information Geometry, Quadrotor Dynamics, Safety CBF, SHATA Auction, ST-GAT-S MARL, Butterfly Flowchart generator).
- `ros2_ws/`: Production ROS 2 Humble package with C++/Python nodes and launch pipelines.
- `results/`: Empirical CSV logs across all 5 operational scenarios, high-resolution publication figures, and 3D mission replay animations.
- `papers/`: Target venue literature analysis and extracted insights across *IEEE Transactions on Cybernetics*, *Swarm and Evolutionary Computation (SWEVO)*, and *Robotics and Autonomous Systems (RAS)*.
- `submission_ieee_(T-Cyb)/` & `submission_elseiver_(SWEVO)_RAS/`: Submission dossiers, figure directories, and tailored Cover Letters for journal submission.

*(Note: In accordance with repository publication guidelines, manuscript `.tex` and `.pdf` files are strictly excluded from the Git tree).*
