# IEEE PaperCept Submission Metadata Sheet

**Conference/Journal Portal:** [IEEE Robotics and Automation Letters (RA-L) Submission Portal](https://ras.papercept.net/)  
**Submission Category:** RA-L Regular Paper (Letter)  
**Target Window:** 2026 Submission Cycle  

---

## 1. Manuscript Metadata Fields

| Field Name | Value to Input into PaperCept Form |
| :--- | :--- |
| **Title** | `AERO-Swarm: A Decentralized Sheaf-Theoretic and Information-Geometric Multi-Agent Framework for Resilient Heterogeneous Drone Swarms in Adversarial Environments` |
| **Running Head / Short Title** | `AERO-Swarm: Resilient Heterogeneous Swarms` |
| **Number of Pages** | `7` |
| **Overlength Page Charge** | `Yes, authors acknowledge and accept page charges for Page 7 ($175/page above 6 pages).` |
| **Primary Subject Category (EDICS)** | `Multi-Robot Systems` |
| **Secondary Subject Categories** | `Networked Robots`, `Aerial Systems: Perception and Autonomy`, `Swarm Robotics` |
| **Conference Option** | `RA-L Only (no joint conference presentation requested)` |

---

## 2. Plaintext Abstract (Ready for Web Portal Form)

```text
Coordinating large-scale heterogeneous drone swarms (100 to 500 aerial agents) operating within GPS-denied, contested, and adversarially jammed environments represents one of the most demanding frontiers in modern robotics. Traditional multi-agent reinforcement learning (MARL) paradigms and classical graph-theoretic consensus models treat communication topologies as simple flat graphs G=(V, E) with scalar weights and assume homogeneous observation-action spaces. These assumptions fail catastrophically when diverse platforms (e.g., compute-dense SLAM leaders, agile sensor scouts, and long-range communication relays) experience localized directional jamming, state-space dimensional mismatch, and progressive node attrition.

In this letter, we establish AERO-Swarm (Adaptive Edge-Resilient Optimization for Heterogeneous Swarms), a foundational mathematical and algorithmic architecture that unifies algebraic topology, information geometry, stochastic differential games, and deep reinforcement learning. Specifically: (1) We formalize swarm coordination over a Cellular Sheaf over a dynamic graph, where heterogeneous node stalks map into edge stalks via learnable restriction maps that continuously attenuate under RF interference. We introduce a Bochner-Weitzenboeck curvature decomposition that proactively identifies jamming bottlenecks via a Sheaf Curvature Vulnerability Index (SCVI). (2) We design an Information-Geometric Event-Triggered Communication (IG-ETC) protocol wherein transmissions occur if and only if the Fisher-Rao Riemannian distance between a drone's true belief distribution and its neighbors' last acknowledged estimate exceeds an energy-annealed threshold. (3) We formulate mission execution as an N-player stochastic differential game on SE(3) with compound Poisson jumps and prove that the global game decouples into local games over sheaf star neighborhoods with an exponential spatial decay bound. (4) We prove that sheaf regularization accelerates MARL convergence at rate O(1/sqrt(K) + lambda_sheaf / (lambda_min * K)), and establish that sheaf consensus degrades strictly linearly under progressive link jamming, eliminating the catastrophic percolation threshold that plagues standard graph-Laplacian swarm systems.

We validate AERO-Swarm across a Dual-Tier pipeline: Tier-1 benchmarks large-scale scalability (N = 10 to 200 UAVs) under progressive jamming (0% to 80%) and catastrophic node attrition (10% to 50%), and Tier-2 validates real-time ROS 2 Humble deployment with hardware-isolated Run-Time Assurance (RTA) Safety Simplex monitors. Empirical results confirm that AERO-Swarm maintains robust coordination and cuts inter-drone communication overhead by up to 79.7%.
```

---

## 3. Keywords Selection (IEEE RAS Taxonomy)

1. `Multi-Robot Systems`
2. `Networked Robots`
3. `Swarms`
4. `Aerial Systems: Perception and Autonomy`
5. `Cellular Sheaves`
6. `Information Geometry`

---

## 4. Suggested Editorial Board Matching

- **Recommended Senior Editor (SE):**
  - **Prof. Antonio Bicchi** / **Prof. Paolo Robuffo Giordano** (*Multi-Robot Systems and Distributed Control*)
- **Recommended Associate Editors (AE):**
  - **Dr. Giuseppe Loianno** (New York University) – *Autonomous Aerial Systems and Vision-based Swarms*
  - **Dr. Dario Brescianini** / **Dr. Javier Alonso-Mora** (TU Delft) – *Multi-Robot Trajectory Planning & Differential Games*
  - **Dr. Lifeng Zhou** (Drexel University) – *Resilient Multi-Robot Coordination under Adversarial Attacks*

---

## 5. Reviewer Nomination & Exclusion

### Recommended Reviewers (5 Nominees)
1. **Prof. Robert Ghrist** (University of Pennsylvania)
   - *Expertise:* Applied algebraic topology, cellular sheaf theory, sensor networks.
2. **Prof. Reza Olfati-Saber** (Autonomous Systems Specialist)
   - *Expertise:* Consensus algorithms, distributed control, graph Laplacians.
3. **Prof. Fei Gao** (Zhejiang University)
   - *Expertise:* Autonomous drone swarms, GPS-denied relative localization, active mutual observation.
4. **Prof. Jonathan P. How** (MIT Aerospace Controls Lab)
   - *Expertise:* Multi-robot task allocation, CBBA auction algorithms, safe autonomy.
5. **Prof. Pietro Liò** (University of Cambridge)
   - *Expertise:* Sheaf neural networks, Bochner-Weitzenböck decomposition, graph curvature.

### Non-Preferred Reviewers
- *None required (no commercial conflicts).*

---

## 6. Multimedia Video Attachment Declaration

- **File Name:** `aero_swarm_mission_replay.gif` (or converted `aero_swarm_mission_replay.mp4`)
- **Duration:** 15 seconds looping high-definition 3D simulation
- **Resolution:** $1080 \times 840$ (100 DPI)
- **File Size:** $7.4\,\mathrm{MB}$ (Well within the $10\,\mathrm{MB}$ IEEE PaperCept limit for video attachments)
- **Caption:**  
  *3D visualization of 30 heterogeneous UAVs (Leaders: Orange, Scouts: Blue, Relays: Green) executing autonomous search-and-rescue while traversing an active Electronic Warfare (EW) jamming field. Demonstrates dynamic sheaf link degradation, Active FoV mutual observation cones, and real-time telemetry confirming 79.7% communication suppression.*

---

## 7. Submission Checklist for Corresponding Author

- [x] Manuscript compiled in LaTeX with IEEEtran journal template (`main.pdf`)
- [x] Page count verified: **Strictly 7 pages** (No trailing overflow onto Page 8)
- [x] High-resolution vector/raster plots (600 DPI PNG / clean vector lines)
- [x] All 18 bibliography citations formatted per IEEE style with DOI/arXiv IDs
- [x] ROS 2 Humble open-source package compiled and verified (`ros2 launch aero_swarm_ros2 swarm_simulation.launch.py`)
- [x] 12-vCPU benchmark suite verified (`python3 benchmark_suite.py`)
- [x] Cover letter prepared (`COVER_LETTER_IEEE_RAL.md`)
- [x] PDF passes IEEE PDF eXpress check (all Type 1 / TrueType fonts embedded)
