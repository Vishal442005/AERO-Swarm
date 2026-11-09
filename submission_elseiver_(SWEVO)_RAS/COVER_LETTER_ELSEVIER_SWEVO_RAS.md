# Submission Cover Letter: Elsevier (Swarm and Evolutionary Computation)

**Date:** November 5, 2026  
**To:** The Editor-in-Chief and Editorial Board  
*Swarm and Evolutionary Computation* (Elsevier)  
**From:** Vishal Chandel  
Autonomous Multi-Agent Robotics Laboratory, Cambridge, United Kingdom  
**Subject:** Submission of Revised Manuscript titled **"AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments"**  
**Manuscript Reference:** `SWEVO-D-26-03280`

---

Dear Editor-in-Chief and Editorial Board of *Swarm and Evolutionary Computation*,

We are pleased to submit our thoroughly revised manuscript entitled **"AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments"** for publication as an Original Research Article in *Swarm and Evolutionary Computation*.

### Context and Motivation
Autonomous aerial multi-robot swarms are essential for mission-critical applications including subterranean exploration, civilian search-and-rescue (SAR), and disaster response in contested or GPS-denied environments. In these scenarios, deploying homogeneous fleets is inherently sub-optimal: operational efficiency demands functional heterogeneity (agile monocular scouts, heavy 3D LiDAR mapping leaders, and long-range communications relays). However, existing decentralized swarm coordination and task allocation frameworks (e.g., Consensus-Based Bundle Algorithms and standard Graph-Laplacian flocking) rely on flat scalar graph models $G=(V, E)$, which fail catastrophically under dimensional observation mismatches and intentional electronic warfare (EW) radio-frequency jamming.

### Key Methodological Innovations and Contributions
In this article, we propose **AERO-Swarm** (*Adaptive Edge-Resilient Optimization for Heterogeneous Swarms*), uniting cellular sheaf theory, discrete differential geometry, information geometry, and decentralized auction optimization:
1. **Heterogeneous Cellular Sheaf Coordination:** We introduce the first cellular sheaf architecture for 6-DoF aerial swarms, explicitly modeling vertex stalks $\mathcal{F}_v = \mathbb{R}^{d_v}$ for diverse robotic platforms (scouts: $\mathbb{R}^{12}$, leaders: $\mathbb{R}^{24}$, relays: $\mathbb{R}^8$) and edge stalks $\mathcal{F}_e = \mathbb{R}^6$ connected via continuous, SINR-aware restriction maps $\rho_{v \trianglelefteq e}(t)$.
2. **Bochner--Weitzenböck Curvature & Zero-Percolation-Threshold Resilience:** We establish a discrete Bochner decomposition $\mathbf{L}_\mathcal{F} = \mathbf{L}_\mathcal{F}^{\mathrm{Bochner}} + \mathbf{Ric}_\mathcal{F}^{\mathrm{Forman}}$ that proactively flags jamming bottlenecks through a Sheaf Curvature Vulnerability Index (SCVI). We prove (Theorem 1) that the swarm resilience index degrades strictly linearly under link jamming ($\mathrm{SRI} \geq \mathrm{SRI}_0(1 - c_{\mathcal{F}} f_{\mathrm{jam}})$), completely eliminating the catastrophic percolation threshold of classical graph Laplacians.
3. **Fisher-Rao Information-Geometric Event Triggering (IG-ETC):** Transmissions are triggered if and only if the Fisher-Rao Riemannian distance on the Gaussian belief manifold exceeds an energy-attenuated threshold $d_{\mathrm{FR}}(p_i, p_{\mathrm{last}}) \geq \delta_i(E_i, \bar{\gamma}_i)$, slashing inter-drone wireless bandwidth by up to $79.6\%$ without tracking or consensus degradation.
4. **Sheaf Heterogeneous Auction for Task Allocation (SHATA):** We design the SHATA auction algorithm for decentralized bundle allocation over sheaf stalks, proving polynomial-time convergence $\mathcal{O}(|V| \cdot M \cdot D_G)$ across heterogeneous drone capabilities.
5. **Dual-Tier Validation (Large-Scale Fleet Sweeps + ROS 2 Humble Flight Stack):**
   - **Tier-1:** Evaluates scalability across $N=10$ to $200$ drones, progressive RF jamming sweeps ($0\%$ to $80\%$), and sudden node destruction ($10\%$ to $50\%$) across 50 Monte Carlo trials with rigorous Wilcoxon signed-rank and Friedman non-parametric statistical hypothesis testing. AERO-Swarm achieves $>91.3\%$ task completion rate under $60\%$ severe link jamming where classical CBBA and flat graph consensus collapse below $24\%$.
   - **Tier-2:** Implements a production-grade ROS 2 Humble node architecture integrated with a hardware-isolated Run-Time Assurance (RTA) Safety Simplex monitor, achieving zero safety violations ($N_{\mathrm{viol}} = 0$) in cluttered 3D obstacle fields with sub-$1.2\,\mathrm{ms}$ fallback intervention.

### Alignment with Swarm and Evolutionary Computation
This article directly aligns with the core scope of *Swarm and Evolutionary Computation*, advancing distributed swarm intelligence, robust multi-agent optimization, resilience under adversarial degradation, and scalable decentralized algorithms. Our benchmarks directly relate to and extend foundational contributions in decentralized swarm consensus, resilient auction heuristics, and bio-inspired distributed coordination.

### Declarations
- The manuscript represents original work, has not been published previously, and is not under consideration for publication elsewhere.
- The author has approved the manuscript and confirms that there are no financial or commercial competing interests.
- All benchmark suites, evaluation scripts, and ROS 2 packages are fully reproducible and open-source at: `https://github.com/Vishal442005/AERO-Swarm`.

Thank you for your consideration of our work.

Sincerely yours,  
**Vishal Chandel**  
Department of Electronics and Communication Engineering  
Jawaharlal Nehru Government Engineering College (JNGEC), Sundernagar  
Mandi, Himachal Pradesh 175018, India  
Email: `chandelvishal445@gmail.com`
