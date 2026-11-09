# Cover Letter for IEEE Robotics and Automation Letters (RA-L)

**To:**  
Editor-in-Chief, *IEEE Robotics and Automation Letters (RA-L)*  
IEEE Robotics and Automation Society (RAS)  

**Date:** November 2, 2026  
**Subject:** Submission of Original Research Letter to *IEEE Robotics and Automation Letters (RA-L)*  

**Manuscript Title:**  
*AERO-Swarm: A Decentralized Sheaf-Theoretic and Information-Geometric Multi-Agent Framework for Resilient Heterogeneous Drone Swarms in Adversarial Environments*  

**Author:**  
Vishal Chandel  
Department of Electronics and Communication Engineering  
Jawaharlal Nehru Government Engineering College (JNGEC), Sundernagar, Mandi, Himachal Pradesh 175018, India  
Contact E-mail: `chandelvishal445@gmail.com`  

---

Dear Editor-in-Chief and Editorial Board,

We are pleased to submit our original research letter titled **"AERO-Swarm: A Decentralized Sheaf-Theoretic and Information-Geometric Multi-Agent Framework for Resilient Heterogeneous Drone Swarms in Adversarial Environments"** for consideration as an original publication in the *IEEE Robotics and Automation Letters (RA-L)*.

### Context and Motivation
Autonomous multi-rotor unmanned aerial vehicle (UAV) swarms operating in contested, GPS-denied theaters (e.g., subterranean search-and-rescue, disaster response, and tactical perimeter defense) require functional heterogeneity—combining agile scout quadrotors, heavy SLAM mappers, and long-range communication relays. However, conventional multi-agent coordination architectures face a fundamental **triad of vulnerabilities**:
1. **The Structural Fallacy of Flat Graph Topologies:** Conventional graph Laplacians treat communication links as scalar weights, failing when diverse platforms with non-identical state dimensions must share partial observations without lossy padding.
2. **RF Jamming and Network Saturation:** Periodic high-frequency broadcasting congests wireless MANET channels, induces packet collisions, and acts as a beacon for electronic warfare direction-finding systems. Crucially, scalar graph Laplacians undergo an abrupt **percolation collapse** at critical jamming fraction $f_c \approx 0.45$, splitting swarms into isolated, uncoordinated clusters.
3. **Non-Stationary Policy Collapse:** When agents drop offline abruptly, MARL critics trained under the CTDE paradigm diverge catastrophically outside their training support.

### Key Breakthroughs and Contributions
In this letter, we establish **AERO-Swarm** (*Adaptive Edge-Resilient Optimization for Heterogeneous Swarms*), introducing five foundational contributions to robotics:
1. **Cellular Sheaf Network Topology:** We formalize swarm communication over a dynamic cellular sheaf $\mathcal{F}$, assigning heterogeneous node stalks ($\mathbb{R}^{24}, \mathbb{R}^{12}, \mathbb{R}^6$) that map into shared edge stalks ($\mathbb{R}^6$) via learnable $\mathrm{SE}(3)$-equivariant restriction maps $\rho_{v \trianglelefteq e}$. Using a Bochner–Weitzenböck decomposition of the block Sheaf Laplacian, we define the **Sheaf Curvature Vulnerability Index (SCVI)** based on Forman–Ricci curvature to proactively route around topological jamming bottlenecks.
2. **Information-Geometric Event Triggering (IG-ETC):** Transmissions are governed by closed-form Fisher-Rao Riemannian distances on Gaussian belief manifolds, triggering broadcasts only upon meaningful information divergence. This cuts RF communication overhead by **up to 79.7%** while preserving tracking precision.
3. **Provable Elimination of Percolation Collapse:** We prove via Weyl's eigenvalue perturbation inequality that the Sheaf Resilience Index degrades strictly linearly ($\mathrm{SRI} \geq \mathrm{SRI}_0(1 - c \cdot f_{\mathrm{jam}})$), completely eliminating the abrupt disconnection phase transition of standard consensus algorithms.
4. **Active FoV Mutual Observation:** Scout quadrotors actively orient their optical axes toward SLAM leaders via a dedicated Control Barrier Function (MO-CBF), arresting relative VIO drift by up to $65\%$ in GPS-denied environments.
5. **ROS 2 Humble & Avionics RTA Certification:** The entire architecture is deployed in **ROS 2 Humble LTS**, featuring a hardware-isolated **Run-Time Assurance (RTA) Safety Simplex** monitor solving online Quadratic Programs in **$< 1.5\,\mathrm{ms}$** using OSQP, satisfying safety-critical avionics timing standards (SAE ARP4754B).

### Manuscript Budget & Submission Compliance
- **Page Length:** The manuscript is formatted in standard IEEEtran two-column journal format and adheres strictly to **exactly 7 pages** (`Pages: 7`), fully within the IEEE RA-L overlength policy (6 pages base + allowable extra pages).
- **Originality:** This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere.
- **Reproducibility:** A complete open-source ROS 2 package (`aero_swarm_ros2`), vectorized multi-core benchmark suite, and high-definition multimedia visualization assets are provided.

### Suggested Technical Committee and Subject Areas
- Multi-Robot Systems
- Networked Robots
- Aerial Systems: Perception and Autonomy
- Swarms
- Reinforcement Learning

### Recommended Reviewers
1. **Prof. Robert Ghrist** (University of Pennsylvania) – *Pioneer of applied cellular sheaf theory and algebraic topology in multi-agent sensor networks.*
2. **Prof. Reza Olfati-Saber** (Dartmouth / Industry) – *Pioneer of distributed consensus, flocking algorithms, and graph Laplacians for multi-agent systems.*
3. **Prof. Jonathan P. How** (Massachusetts Institute of Technology) – *Leading expert in robust decentralized auction algorithms (CBBA) and multi-UAV trajectory planning.*
4. **Prof. Fei Gao** (Zhejiang University) – *Leading expert in autonomous drone swarms, active mutual observation, and vision-based relative localization in GPS-denied environments.*
5. **Prof. Pietro Liò** (University of Cambridge) – *World expert on sheaf neural networks, geometric deep learning, and curvature on graphs.*

We believe this letter bridges the longstanding gap between pure algebraic topology and safety-critical physical robotics, offering an agile, resilient, and mathematically sound architecture for future aerial autonomous swarms. We thank you and the reviewers for your time and consideration.

Sincerely,

**Vishal Chandel**  
Department of Electronics and Communication Engineering  
Jawaharlal Nehru Government Engineering College (JNGEC), Sundernagar, Mandi, Himachal Pradesh 175018, India  
E-mail: `chandelvishal445@gmail.com`  
GitHub: `https://github.com/Vishal442005/AERO-Swarm`
