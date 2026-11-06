# Formal Resubmission Response to the Journal Editor

**Manuscript Reference:** SWEVO-D-26-03280  
**Title:** AERO-Swarm: Adaptive Edge-Resilient Optimization for Heterogeneous Swarms via Cellular Sheaves and Information-Geometric Event Triggering  
**Journal:** *Swarm and Evolutionary Computation* (Elsevier)  
**Author:** Vishal Chandel  
**Date of Resubmission:** November 2026  

---

Dear Editor-in-Chief and Editorial Board,

Thank you for your constructive editorial evaluation of our manuscript. We have carefully studied the reasons for the decline decision:

> *"Although your manuscript falls within the aim and scope of this journal, it is being declined as the research results reported, in their present form, lack the archival value required by this Journal. The performance evaluation campaign is rich in results which, however, are not commented on in a clear enough manner as required by the standards of this Journal. Many of the curves are only commented without sufficient explanatory details on the reason for their trend, and there is a lack of a synthesis that can testify to the generality of the results and that can make it clearer in which conditions the algorithm performs better and under which conditions worse. Besides, the comparison with other solutions should definitely be conducted under a wider range of different conditions and for several other similar approaches available in the literature. More work is needed to substantiate the conclusions in your manuscript."*

We have performed an extensive, rigorous overhaul of the manuscript to elevate it to the highest archival journal standards. Specifically, we have:
1. **Completely rewritten the results commentary (Section 9)** to provide deep, mechanistic physical, topological, and differential-geometric explanations for every single trend, inflection point, and bifurcation.
2. **Introduced an entirely new dedicated section (Section 10: Generality Synthesis, Operational Boundaries, and Failure Envelopes)** that explicitly delineates when AERO-Swarm dominates, when simpler baselines suffice, and the physical failure boundaries of the architecture (supported by a new Operational Boundaries Taxonomy, Table 4).
3. **Substantially expanded the performance evaluation campaign** across **three diverse operational theaters** (Urban SAR Canyon, Open Maritime Logistics, Subterranean Rubble Tunnel) and **three fleet composition heterogeneity configurations** (Scout-Heavy, Balanced, Leader-Heavy), supported by two brand-new publication figures (**Figure 5** and **Figure 6**) and comparisons across 7 state-of-the-art and classical baselines.
4. **Structured all deliverables in an organized, reproducible archival package** (`Updated_significant/`), containing all updated source files, raw CSV datasets, figures, and modular tables.

Below is our point-by-point account detailing how each editorial critique has been thoroughly addressed.

---

## Point-by-Point Rebuttal and Revision Details

### Editorial Concern 1: Lack of Explanatory Commentary on the Reasons for Empirical Trends
> *"Many of the curves are only commented without sufficient explanatory details on the reason for their trend..."*

**Author Response & Revisions:**  
In the revised manuscript (Section 9.1–9.6), every single empirical curve has been expanded with explicit physical, algebraic-topological, and information-geometric causal explanations:

1. **Figure 3(a) & Section 9.1 (TCR vs. Jamming):**
   * *Trend Explained:* Flat-graph CBBA and flocking collapse abruptly at $f_{\mathrm{jam}} \approx 0.35$ ($>95\% \to 23.7\%$), while AERO-Swarm decays smoothly ($98.2\% \to 91.3\% \to 85.2\%$).
   * *Archival Mechanism Added:* We explain that the sharp drop in classical baselines reflects the Erdős-Rényi bond percolation threshold $p_c \approx 1/\langle k \rangle$ on random geometric graphs. When RF jamming drops transmission probability below $p_c$, the giant connected component shatters into isolated subgraphs. These isolated subgraphs continue updating task bundles asynchronously; upon intermittent reconnection, out-of-order bid timestamps trigger circular outbidding deadlocks. Conversely, AERO-Swarm's cellular sheaf endows links with continuous restriction maps $\rho_{v \trianglelefteq e}(t) = \sqrt{\gamma_e(t)} \mathbf{P}_v$, maintaining positive algebraic connectivity $\lambda_2(\mathbf{L}_\mathcal{F}) > 0$ across orthogonal stalk dimensions ($d_v \in \{8, 12, 24\}$). The Bochner curvature tensor identifies localized holonomy bottlenecks prior to disconnection, enabling SHATA to reroute bids through reliable Relay UAVs.

2. **Figure 3(b) & Section 9.2 (SRI vs. Attrition):**
   * *Trend Explained:* Scalar graph Laplacians collapse to $\mathrm{SRI} = 0.082$ at $40\%$ attrition, while the Sheaf Laplacian retains $\mathrm{SRI} = 0.718$.
   * *Archival Mechanism Added:* Scalar Laplacians assign scalar degrees $d_i = \sum A_{ij}$; losing high-degree nodes immediately zeroes out entire matrix blocks, dissolving the spectral gap. In cellular sheaves, node stalks possess dimensional cushioning ($d_v \in \{8, 12, 24\}$); destroying an agent removes only a single subspace projection, while surviving agents maintain relational alignment along orthogonal cochains, validating the linear degradation bound proved in Theorem 1.

3. **Figure 3(c) & Section 9.3 (Communication Bandwidth Conservation):**
   * *Trend Explained:* Periodic broadcast consumes $188.2 \times 10^3$ packets; Euclidean ETC consumes $102.4 \times 10^3$; Fisher-Rao IG-ETC consumes only $38.4 \times 10^3$ ($-79.6\%$).
   * *Archival Mechanism Added:* We contrast the differential geometry of Euclidean vs. Riemannian belief manifolds. Euclidean triggering $\|x - x_{\mathrm{last}}\| > \delta$ is coordinate-dependent and isotropic; during high-speed steady flight, drones travel large distances while covariance is stationary, generating bursts of false-alarm packets. In contrast, the Fisher-Rao metric $d_{\mathrm{FR}}^2$ measures geodesic distance between probability measures on the Siegel upper half-space $\mathcal{P}_+^6$. It scales step size by the inverse covariance $\boldsymbol{\Sigma}^{-1}$, remaining strictly silent during predictable motion and firing only upon true statistical divergence.

4. **Figure 3(d) & Section 9.4 (Computational Scalability):**
   * *Trend Explained:* AERO-Swarm executes in $4.92\,\mathrm{ms}$ ($N=100$) and $14.18\,\mathrm{ms}$ ($N=200$), while attention MARL (AC-MASAC) surges to $142.2\,\mathrm{ms}$.
   * *Archival Mechanism Added:* Attention mechanisms scale quadratically $\mathcal{O}(|V|^2)$ as all-to-all dot products must be computed. AERO-Swarm operates over local 1-hop star-graph cochain assemblies $\mathcal{O}(|\mathcal{N}_i| d_{\max}^2)$ with bounded physical degrees $|\mathcal{N}_i| \le 12$, guaranteeing sub-20 ms latency on 12 vCPUs.

---

### Editorial Concern 2: Lack of Synthesis Testifying to Generality & Operational Boundaries
> *"there is a lack of a synthesis that can testify to the generality of the results and that can make it clearer in which conditions the algorithm performs better and under which conditions worse..."*

**Author Response & Revisions:**  
We have introduced a comprehensive new section: **Section 10: Generality Synthesis, Operational Boundaries, and Failure Envelopes**, accompanied by **Table 4 (Operational Boundaries Taxonomy)** and **Figure 5(b) (Generality Contour Map)**:

* **Zone I: Superiority Domain (Where AERO-Swarm Dominates):**
  - *Conditions:* Severe adversarial RF jamming ($f_{\mathrm{jam}} \in [0.4, 0.8]$), high agent heterogeneity ($d_v \in \{8, 12, 24\}$), large swarm scales ($N \ge 30$ up to $200+$), and covert/bandwidth-limited operations.
  - *Advantage:* Delivers $+60\%$ to $+68\%$ TCR superiority over classical CBBA and flocking by eliminating percolation collapse.
* **Zone II: Parity / Diminishing Returns Domain (Where Simpler Baselines Suffice):**
  - *Conditions:* Benign, unperturbed line-of-sight environments ($f_{\mathrm{jam}} \le 0.15$), small homogeneous fleets ($N \le 8$), and unlimited battery reserves.
  - *Behavior:* Restriction maps collapse to scalar identity; AERO-Swarm's TCR advantage narrows to only $+2\%$ to $+5\%$. Here, standard periodic broadcast or classical CBBA is computationally lighter and practically sufficient.
* **Zone III: High-Dynamic Scalability Domain (Massive Swarms):**
  - *Conditions:* Fleet sizes $N \in [50, 200+]$ under strict real-time control deadlines ($50\,\mathrm{Hz} / 20\,\mathrm{ms}$).
  - *Behavior:* Local star-graph cochain assembly keeps execution latency under $14.2\,\mathrm{ms}$, whereas centralized learning models violate flight stability.
* **Zone IV: Physical Breakdown Boundary (Failure Envelope):**
  - *Conditions:* Extreme jamming ($f_{\mathrm{jam}} > 0.85$), where physical received signal power drops below thermal noise across all channels simultaneously ($k < 1$).
  - *Behavior:* All decentralized consensus breaks down (TCR $<35\%$). Drones trigger certified hardware RTA failsafe Return-To-Launch (RTL) protocols.
* **Zone V: Sensor Starvation Boundary (Visibility Limits):**
  - *Conditions:* Extreme fleet skew ($>90\%$ Scouts) in cluttered canyons where line-of-sight to Leaders is permanently occluded.
  - *Behavior:* Active-FoV visual tracking is lost, accelerating visual odometry drift. We identify an operational fleet rebalancing threshold: at least $15\%$ Leader/Relay presence is required to anchor cochain stability.

---

### Editorial Concern 3: Wider Range of Comparative Conditions and Approaches
> *"Besides, the comparison with other solutions should definitely be conducted under a wider range of different conditions and for several other similar approaches available in the literature..."*

**Author Response & Revisions:**  
We have substantially broadened the experimental scope across multiple environmental theaters, fleet compositions, and recent state-of-the-art baselines:

1. **Three Distinct Operational Theaters (Figure 5a):**
   * *Urban SAR Canyon:* High obstacle density, severe multi-path fading ($\alpha = 3.8$), and shadowing.
   * *Maritime / Contested Logistics:* Wide-open domain, high wind turbulence ($2.5\,\mathrm{m/s}$), long-range wireless links ($92.8\%$ TCR under $60\%$ jamming).
   * *Subterranean Rubble Tunnel:* Confined corridors, extreme non-line-of-sight ($87.6\%$ TCR vs. $16.8\%$ CBBA collapse).
2. **Three Fleet Heterogeneity Ratios (Figure 6a):**
   * *Scout-Heavy ($10\mathrm{L}/80\mathrm{S}/10\mathrm{R}$):* Fast agility, compute-limited ($88.4\%$ TCR vs. $16.8\%$ CBBA).
   * *Balanced ($20\mathrm{L}/60\mathrm{S}/20\mathrm{R}$):* Optimal tactical fleet ($91.3\%$ TCR, $38.5\%$ energy consumption).
   * *Leader-Heavy ($40\mathrm{L}/40\mathrm{S}/20\mathrm{R}$):* Compute-abundant ($93.6\%$ TCR, $45.8\%$ hover energy).
3. **Cohomological Obstruction Resolution (Figure 6b):**
   * We prove empirically that flat-graph bidding creates persistent non-zero 1-cochain curls ($\dim H^1 > 0$), manifesting as bidding deadlocks. SHATA's restriction projection along the coboundary operator systematically drives $\dim H^1 \to 0$, formally eliminating conflict loops.
4. **Comprehensive Benchmarking Against 7 Approaches (Table 2 & 3):**
   * CBBA (Choi et al., IEEE T-RO 2009)
   * Flocking Consensus (Olfati-Saber, IEEE TAC 2006)
   * FoV Mutual Observation Flocking (Guo et al., IEEE RA-L 2024)
   * Resilient Event-Triggered Consensus (Sun et al., IEEE T-CYB 2025)
   * Physics-Informed GNN Swarms (Phy-GAIL, 2026)
   * Attentive Actor-Critic MARL (AC-MASAC, 2026)
   * Fixed Sheaf Network (Bodnar et al., NeurIPS 2022)

---

## Summary of Updated Deliverables in `Updated_significant/`

The complete updated dossier is organized within `Updated_significant/`:
* `manuscript/`: Expanded 18-page publication-grade PDF (`main.pdf`) and LaTeX source (`main.tex`).
* `figures/`: High-resolution figures, including new multi-panel analytical additions:
  - `fig5_operational_envelope.png` (Multi-theater curves & generality boundary map)
  - `fig6_fleet_heterogeneity.png` (Composition sensitivity & $\dim H^1$ cohomological conflict resolution)
  - Updated Figures 1–4, flowcharts, and 3D simulation telemetry replay GIF (`aero_swarm_mission_replay.gif`).
* `tables/`: Modular markdown and LaTeX tables (`table1` to `table4`).
* `results_data/`: Complete CSV datasets for all 6 benchmark scenarios (`scenario1`, `2`, `3`, `5`, `6`, and `7`).
* `scripts/`: Python benchmark execution and plotting scripts.

We believe this thorough revision directly resolves every concern, provides lasting archival scientific value, and substantiates all conclusions. We look forward to your reconsideration of our manuscript for publication in *Swarm and Evolutionary Computation*.

Sincerely,  
**Vishal Chandel**  
Corresponding Author
