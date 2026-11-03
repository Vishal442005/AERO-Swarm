# AERO-Swarm v1.1.0: Ultra-Simple butterpy Flowcharts & Publication Diagrams

**AERO-Swarm (Adaptive Edge-Resilient Optimization for Heterogeneous Swarms)** is an open-source, mathematically grounded, and production-ready coordination stack for large-scale heterogeneous aerial drone swarms in GPS-denied, contested, and electronically jammed environments.

## Highlights of v1.1.0 Release
- **`butterpy` Python Flowchart Extension (`src/butterpy/`):** Generates publication-grade, ultra-simple flowcharts and block diagrams conforming strictly to top IEEE and Elsevier standards:
  - **Zero box fill colors:** Pure white box interiors.
  - **Crisp solid black outlines and directed black arrows.**
  - **Standard geometric primitives:** Capsules (Terminals), Rectangles (Processes), and Diamonds (Decisions).
  - **Embedded vector icons:** Drone, Sensor, Sheaf Core ($L$), Decision ($?$), Jammer Tower, Target, and Safety Shield.
- **The 3 Publication Flowcharts:**
  1. `fig_flowchart1_sheaf_coordination.png`: System-level cellular sheaf Laplacian coordination, Bochner--Weitzenböck curvature jamming detection, and distributed state consensus.
  2. `fig_flowchart2_ig_etc.png`: Information-Geometric Event-Triggered Communication (IG-ETC) using Fisher-Rao Riemannian geodesic divergence on $\mathcal{P}_+^6$ manifolds ($79.7\%$ communication suppression).
  3. `fig_flowchart3_shata_auction.png`: Decentralized Sheaf Heterogeneous Auction for Task Allocation (SHATA) bundled with hardware-isolated Run-Time Assurance (RTA) Safety Simplex barrier monitors ($<1.2\,\mathrm{ms}$ override latency, zero safety violations).
- **Simplified Publication Block Diagrams:**
  - `fig_ros2_architecture.png`: Minimalist pure black-and-white ROS 2 Humble node architecture.
  - `fig_teaser_sheaf_concept.png`: Minimalist pure black-and-white cellular sheaf projection model.
- **Journal Submissions Verified & Recompiled:**
  - `submission_ieee_(T-Cyb)/`: Formatted for *IEEE Transactions on Cybernetics* (9 pages, letter format, zero compile errors).
  - `submission_elseiver_(SWEVO)_RAS/`: Formatted for *Elsevier Swarm and Evolutionary Computation / RAS* (14 pages, 2-column elsarticle, zero compile errors).
  - Official formal `.docx` and `.md` cover letters provided for both journal targets.

*(Note: In accordance with repository publication guidelines, manuscript `.tex` and `.pdf` files are strictly excluded from the Git tree).*
