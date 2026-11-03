# Submission Cover Letter: IEEE Transactions on Cybernetics

**Date:** November 3, 2026  
**To:** Prof. Editor-in-Chief  
*IEEE Transactions on Cybernetics*  
**From:** Autonomous Robotics Swarm Research Consortium  
**Subject:** Submission of Original Regular Research Manuscript titled **"AERO-Swarm: A Decentralized Sheaf-Theoretic and Information-Geometric Multi-Agent Framework for Resilient Heterogeneous Drone Swarms in Adversarial Environments"**

---

Dear Prof. Editor-in-Chief and Distinguished Editorial Board,

We are pleased to submit our original regular research manuscript titled **"AERO-Swarm: A Decentralized Sheaf-Theoretic and Information-Geometric Multi-Agent Framework for Resilient Heterogeneous Drone Swarms in Adversarial Environments"** for consideration as a Regular Paper in the *IEEE Transactions on Cybernetics*.

### Motivation and Core Contributions
Coordinating large-scale heterogeneous drone swarms (100–500 aerial agents) operating within GPS-denied, contested, and adversarially jammed theaters represents one of the most demanding frontiers in cybernetics, multi-agent systems, and decentralized cyber-physical control. Conventional multi-agent consensus algorithms and standard graph-theoretic frameworks rely on flat scalar graphs $G=(V, E)$, which inherently fail when platforms with heterogeneous observation-action spaces experience localized directional jamming, state-space dimensional mismatch, and progressive node attrition.

In this paper, we establish **AERO-Swarm**, a mathematically rigorous and computationally validated framework that directly addresses the core scope of *IEEE Transactions on Cybernetics*:
1. **Cellular Sheaf Network Modeling with Asymmetric Stalks:** We model the swarm over a cellular sheaf $\mathcal{F}$ over a dynamic graph $G(t)$, where heterogeneous platform state spaces ($\mathcal{F}_v = \mathbb{R}^{d_v}$) map into mutual edge channels ($\mathcal{F}_e = \mathbb{R}^{d_e}$) via continuous, signal-to-interference-dependent restriction maps $\rho_{v \trianglelefteq e}(t)$. We establish the discrete Bochner--Weitzenb\"ock decomposition $\mathbf{L}_\mathcal{F} = \mathbf{L}_\mathcal{F}^{\mathrm{Bochner}} + \mathbf{Ric}_\mathcal{F}^{\mathrm{Forman}}$ and formulate the Sheaf Curvature Vulnerability Index (SCVI) to proactively identify jamming bottlenecks before physical link disconnection.
2. **Elimination of the Percolation Threshold:** We prove mathematically (Theorem 2) that under progressive link jamming, the Sheaf Laplacian consensus capability degrades strictly linearly ($\mathrm{SRI} \geq \mathrm{SRI}_0(1 - c_{\mathcal{F}} f_{\mathrm{jam}})$), formally proving the total elimination of the catastrophic second-order percolation phase collapse that paralyzes conventional scalar graph Laplacians.
3. **Information-Geometric Event-Triggered Communication (IG-ETC):** Transmissions occur if and only if the Fisher-Rao Riemannian distance on the Gaussian belief manifold exceeds an energy-attenuated threshold $d_{\mathrm{FR}}(p_i(t), p_i(t_{\mathrm{last}})) > \delta_i(E_i, \bar{\gamma}_i)$, cutting communication bandwidth by up to $79.7\%$ without tracking degradation.
4. **Stochastic Differential Game on $\mathrm{SE}(3)$ & MARL Convergence:** We formulate mission execution as an $N$-player stochastic differential game with compound Poisson jumps and prove exponential spatial decoupling (Theorem 1). Furthermore, we establish guaranteed $\mathcal{O}(1/K)$ acceleration of policy gradient convergence under sheaf Dirichlet regularization (Theorem 3).
5. **Dual-Tier Empirical & ROS 2 Humble Validation:** We validate the framework on both a 12-vCPU vectorized benchmark sweep across $N=10$ to $200$ drones (retaining $>91.3\%$ task completion under $60\%$ jamming where classical CBBA and flat graph consensus drop below $24\%$) and an end-to-end ROS 2 Humble flight architecture integrated with hardware-isolated Run-Time Assurance (RTA) Simplex safety monitors ($N_{\mathrm{viol}} = 0$).

### Alignment with IEEE Transactions on Cybernetics
This manuscript directly builds upon and advances recent theoretical milestones published in *IEEE Transactions on Cybernetics*, including:
- Event-triggered resilient consensus under Byzantine attacks (Sun et al., *IEEE Trans. Cybern.*, 2025);
- Contingency safety-critical planning for multi-agent autonomous systems (vol. 56, no. 5, May 2026);
- Prescribed-time distributed optimization for high-order nonlinear multi-agent systems (vol. 55, no. 10, Oct. 2025).

### Author Declarations & Reproducibility
- **Originality:** This manuscript is an original work that has not been published elsewhere and is not under consideration by any other journal or conference.
- **Ethics & Open Source:** All authors have approved the manuscript. The complete vectorized benchmark suite, mathematical simulation scripts, and ROS 2 Humble packages are open-source and fully reproducible.

Thank you very much for your time, consideration, and handling of our submission.

Sincerely,  
**Autonomous Robotics Swarm Research Consortium**  
Division of Robotics and Autonomous Systems  
Autonomous Multi-Agent Robotics Laboratory  
Contact Email: `research@autonomous-swarms.org`
