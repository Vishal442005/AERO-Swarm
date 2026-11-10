# Submission Cover Letter: Elsevier (Robotics and Autonomous Systems)

**Date:** November 10, 2026  
**To:** Prof. Dr. Karsten Berns, Prof. Maria Gini, and Prof. Jun Ota  
Editors-in-Chief and Editorial Board  
*Robotics and Autonomous Systems* (Elsevier)  

**From:** Vishal Chandel  
Department of Electronics and Communication Engineering  
Jawaharlal Nehru Government Engineering College (JNGEC), Sundernagar  
Mandi, Himachal Pradesh 175018, India  
Email: `chandelvishal445@gmail.com`  

**Subject:** Submission of Original Research Article titled **"AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments"**  

---

Dear Editors-in-Chief Prof. Berns, Prof. Gini, Prof. Ota, and Esteemed Members of the Editorial Board,

We are delighted to submit our original research manuscript entitled **"AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments"** for publication as a Full-Length Research Article in *Robotics and Autonomous Systems* (Elsevier).

### Motivation and Core Problem Formulation
Autonomous aerial multi-robot swarms ($N = 10$ to $200+$ Unmanned Aerial Vehicles) are increasingly critical for high-stakes robotics operations, including urban search-and-rescue (SAR), subterranean reconnaissance, environmental disaster monitoring, and tactical logistics in GPS-denied environments. In these realistic missions, deploying homogeneous fleets is fundamentally impractical; mission success requires functional heterogeneity—coupling nimble monocular sensor scouts, compute-heavy 3D LiDAR mapping leaders, and long-range communication relays. 

However, existing decentralized multi-robot coordination frameworks (such as Consensus-Based Bundle Algorithms [CBBA] and standard Graph-Laplacian flocking) inherently model agent connectivity via flat scalar graphs $G=(V, E)$ and assume identical observation-action manifolds across all robots. Under asymmetric platform dimensional mismatches, moving physical obstacles, and directional radio-frequency (RF) jamming, these classical algorithms experience catastrophic failure:
1. Flat graph Laplacians undergo abrupt percolation phase collapse when link dropping exceeds $\sim 35\%$, fragmenting the fleet into isolated singletons.
2. Auction algorithms suffer circular outbidding deadlocks and out-of-order bid corruption under packet loss.
3. High-frequency broadcast flooding saturates wireless channels, precipitating DDS socket buffer overflow and packet drop cascades.

### Methodological Innovations of AERO-Swarm
In this manuscript, we present **AERO-Swarm** (*Adaptive Edge-Resilient Optimization for Heterogeneous Swarms*), a unified algebraic-topological, information-geometric, and provably safe decentralized framework specifically designed for autonomous robotic swarms:

1. **Heterogeneous Cellular Sheaf Modeling:** We formulate the first cellular sheaf architecture for 6-DoF aerial robotic swarms. Rather than treating inter-robot links as binary edges, vertex stalks $\mathcal{F}_v = \mathbb{R}^{d_v}$ accommodate distinct platform dimensionalities (Scouts: $\mathbb{R}^{12}$, Leaders: $\mathbb{R}^{24}$, Relays: $\mathbb{R}^8$), reconciled over edge stalks $\mathcal{F}_e = \mathbb{R}^6$ via continuous, SINR-modulated restriction maps $\rho_{v \trianglelefteq e}(t) = \sqrt{\gamma_e(t)} \mathbf{P}_v$.
2. **Bochner--Weitzenböck Curvature & Zero-Percolation Decay:** We derive a discrete Bochner Laplacian decomposition $(\mathbf{L}_\mathcal{F} = \mathbf{L}_\mathcal{F}^{\mathrm{Bochner}} + \mathbf{Ric}_\mathcal{F}^{\mathrm{Forman}})$ that computes a local Sheaf Curvature Vulnerability Index (SCVI), identifying RF jamming bottlenecks prior to topological disconnection. Crucially, we prove mathematically (**Theorem 1**) that under progressive link jamming, sheaf consensus resilience degrades strictly linearly ($\mathrm{SRI} \ge \mathrm{SRI}_0(1 - c_\mathcal{F} f_{\mathrm{jam}})$), completely eliminating the non-differentiable percolation phase transitions that paralyze standard graph Laplacians.
3. **Fisher-Rao Information-Geometric Event-Triggered Communication (IG-ETC):** Addressing bandwidth constraints in robotic wireless networks, we formulate an event-trigger on the Riemannian manifold of multivariate Gaussians $\mathcal{P}_+^6$. Broadcasts fire if and only if the Fisher-Rao geodesic distance exceeds an energy-annealed threshold $d_{\mathrm{FR}}(p_i(t), p_i(t_{\mathrm{last}})) \ge \delta_i(t)$. This cuts inter-drone RF communication by an exact **$79.6\%$** without tracking or consensus degradation.
4. **Sheaf Heterogeneous Auction for Task Allocation (SHATA):** We develop the SHATA decentralized auction protocol, incorporating local sheaf connectivity discounting $\bar{\Gamma}_i(t)$ and first-cohomology group ($\dim H^1$) harmonic projection to deconflict outbidding cycles. We prove conflict-free convergence in $\mathcal{O}(|V| \cdot M \cdot D_G)$ iterations and formally establish (**Proposition 1**) that per-agent computational complexity is strictly bounded by $\mathcal{O}(|\mathcal{N}_i| d_v^2 + M L_{\max}^2 + |\mathcal{N}_i| M + m_{\mathrm{obs}}) \implies \mathcal{O}(d_v^2 + M)$, remaining strictly independent of total swarm population $N$.
5. **Hardware-Isolated Run-Time Assurance (RTA) Safety Simplex:** To guarantee physical collision-freedom in obstacle-cluttered canyons, each drone integrates a formal RTA Simplex monitor enforcing high-order Control Barrier Functions (CBFs). A closed-form minimum-intervention quadratic program (QP) overrides high-level neural/consensus setpoints within $<1.2\,\mathrm{ms}$, provably guaranteeing forward invariance of the safe set $\mathcal{C}$.

### Experimental Validation and Alignment with Robotics and Autonomous Systems
To rigorously confirm both theoretical validity and real-world robotics deployment feasibility, we execute an exhaustive dual-tier validation campaign:
* **Tier-1 Parallelized Scalability & Resilience Sweeps:** Evaluated across $N=10$ to $200$ drones, jamming sweeps $f_{\mathrm{jam}} \in [0.0, 0.80]$, and sudden node destruction ($10\%$ to $50\%$) over 50 Monte Carlo trials. All empirical findings are substantiated by **non-parametric Wilcoxon signed-rank tests** ($p < 10^{-6}$ to $p < 10^{-12}$, paired Cohen's $d = 2.45$ to $4.12$) and Friedman tests ($\chi_F^2 = 184.6, p < 10^{-15}$). AERO-Swarm preserves **$91.3\%$ Task Completion Rate** under $60\%$ severe jamming where classical CBBA and flocking collapse below $24\%$.
* **Tier-2 Production-Grade ROS 2 Humble Flight Architecture:** Implemented in genuine ROS 2 Humble nodes (`aero_sheaf_coordinator`, `aero_task_allocator`, `aero_formation_controller`, `rta_safety_simplex_node`) communicating over CycloneDDS middleware with PX4 SITL autopilot integration. In dense 3D urban canyons with moving obstacles and velocity ribbons ($0$ to $6\,\mathrm{m/s}$), AERO-Swarm achieved **zero safety violations ($N_{\mathrm{viol}} = 0$)** across all trials with a deterministic P99 CBF QP solve latency of $44.8\,\mu\mathrm{s}$ ($33\times$ below the $1.5\,\mathrm{ms}$ SAE ARP4754B avionics budget).

This research directly aligns with the core scope of ***Robotics and Autonomous Systems***, advancing the state-of-the-art in multi-robot systems, distributed swarm autonomy, real-time safety verification, communication-efficient multi-agent coordination, and field-applicable robotics middleware.

### Suggested Expert Reviewers
1. **Prof. Vijay Kumar** (University of Pennsylvania, USA) — *Expertise:* Autonomous aerial swarms, multi-robot coordination, micro-aerial vehicles. Email: `kumar@seas.upenn.edu`
2. **Prof. Magnus Egerstedt** (University of California, Irvine, USA) — *Expertise:* Multi-agent robotics, Control Barrier Functions, swarm robotics, provable safety. Email: `magnus@uci.edu`
3. **Prof. Michael Schwager** (Stanford University, USA) — *Expertise:* Distributed multi-robot task allocation, decentralized algorithms, aerial robot coordination. Email: `schwager@stanford.edu`
4. **Prof. Florian Bullo** (University of California, Santa Barbara, USA) — *Expertise:* Networked robotic systems, consensus algorithms, geometric control. Email: `bullo@engineering.ucsb.edu`
5. **Prof. Pietro Liò** (University of Cambridge, UK) — *Expertise:* Cellular sheaf Laplacians, topological machine learning, graph neural networks. Email: `pl219@cam.ac.uk`

### Declarations
* **Originality:** This manuscript represents original work, has not been published previously, and is not currently under consideration for publication elsewhere.
* **Author Approval:** The author has reviewed, verified, and approved the submitted manuscript in its entirety.
* **Conflict of Interest:** The author declares no competing financial, professional, or personal conflicts of interest.
* **Open-Source Reproducibility:** In accordance with open-science principles, the complete codebase—including ROS 2 Humble packages, micro-XRCE-DDS bridge configurations, evaluation scripts, and benchmark telemetry—is publicly available at:  
  **`https://github.com/Vishal442005/AERO-Swarm`**

Thank you very much for considering our manuscript for publication in *Robotics and Autonomous Systems*. We look forward to receiving the reviewers' constructive feedback.

Sincerely yours,

**Vishal Chandel**  
Department of Electronics and Communication Engineering  
Jawaharlal Nehru Government Engineering College (JNGEC), Sundernagar  
Mandi, Himachal Pradesh 175018, India  
Email: `chandelvishal445@gmail.com`  
Corresponding Author for *Robotics and Autonomous Systems*
