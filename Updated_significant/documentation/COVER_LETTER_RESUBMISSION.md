# Formal Resubmission Cover Letter

**Date:** November 6, 2026  

**To:**  
Prof. Yew-Soon Ong  
Editor-in-Chief, *Swarm and Evolutionary Computation*  
Elsevier Science  

**Subject:** Formal Resubmission of Extensively Revised Archival Manuscript (Ref: `SWEVO-D-26-03280`)  
**Title:** *AERO-Swarm: Resilient Autonomous Drone Swarm Coordination Under Severe Communication Contention via Cellular Sheaf Laplacians and Information Geometry*  
**Author:** Vishal Chandel  
**Affiliation:** Autonomous Systems and Swarm Robotics Laboratory  
**Target Journal:** *Swarm and Evolutionary Computation*  

---

Dear Professor Ong and Members of the Editorial Board,

Thank you for your constructive editorial evaluation of our previous submission, `SWEVO-D-26-03280`. We deeply appreciated the Editorial Board’s candid assessment that while the research falls squarely within the aim and scope of *Swarm and Evolutionary Computation*, the initial manuscript lacked the archival depth required by the Journal—specifically regarding the mechanistic explanations of empirical curve trends, a comprehensive synthesis of generality and operational boundaries, and evaluations across a wider range of physical operational conditions.

In response, we have treated this evaluation not merely as an editorial critique, but as a mandate for a **complete, foundational elevation of the study to the highest archival standards**. Over the past several months, we have substantially expanded the theoretical apparatus, conducted extensive new multi-condition empirical campaigns, synthesized a definitive operational taxonomy, and completely rewritten Sections 9 and 10 of the manuscript.

We now have the honor of submitting our thoroughly revised, 18-page archival manuscript for your consideration.

---

### Key Archival Additions and Systematic Enhancements

1. **Rigorous Mechanistic Explanations of All Empirical Trends (Section 9):**  
   The revised manuscript no longer merely reports performance curves; it deconstructs every observed phenomenon through the lens of governing mathematical physics:
   - *Phase Collapse in Graph Laplacians vs. Sheaf Cushioning:* We mathematically prove and empirically demonstrate that flat consensus baselines collapse at $f_{\mathrm{jam}} \approx 0.35$ due to Erdős-Rényi bond percolation threshold breakdown ($p_c \approx 1/\langle k \rangle$). In contrast, cellular sheaf restriction maps $\rho_{v \trianglelefteq e}(t) = \sqrt{\gamma_e(t)}\mathbf{P}_v$ preserve vector stalk spaces ($d_v \in \{8, 12, 24\}$), maintaining algebraic connectivity $\lambda_2(\mathcal{L}_\mathcal{F}) > 0$ and achieving **$91.3\% \pm 1.8\%$ TCR** under $60\%$ severe RF jamming.
   - *Fisher-Rao Information Geometry vs. Euclidean ETC:* We explain why Euclidean event-triggered thresholds trigger burst chattering during dynamic acceleration, whereas geodesic distances on the Riemannian Siegel manifold of Gaussian belief distributions ($\mathcal{P}_+^6$) scale by inverse state covariance, suppressing uninformative kinematic changes to deliver a verified **$79.6\%$ bandwidth reduction**.
   - *Harmonic Cohomological Obstructions:* We demonstrate how the Sheaf-Harmonic Task Allocation (SHATA) protocol resolves circular outbidding deadlocks by driving the first cohomology group rank $\dim H^1(\mathcal{F}; \mathbb{R}^d)$ monotonically to zero.
   - *Complexity Scaling:* We prove that localized sparse block-Cholesky updates yield per-node computational complexity $\mathcal{O}(|\mathcal{N}_i| \cdot d_e^2) + \mathcal{O}(d_v^3) = \mathcal{O}(1)$, explaining why per-step execution latency scales gracefully to only **$14.18\text{ ms}$ at $N=200$ drones**, well within the $20.0\text{ ms}$ ($50\text{ Hz}$) flight loop deadline.

2. **Generality Synthesis & Operational Boundaries Taxonomy (New Section 10 & Table 4):**  
   We have added a dedicated section and synthesis table explicitly establishing under which conditions AERO-Swarm performs better, achieves parity, or encounters physical boundaries:
   - *Zone I (Superiority Zone):* Contested RF ($f_{\mathrm{jam}} \in [0.4, 0.8]$), high attrition, and multi-role heterogeneous fleets where AERO-Swarm outperforms baselines by $+30\%$ to $+70\%$ TCR.
   - *Zone II (Parity Zone):* Pristine RF ($f_{\mathrm{jam}} < 0.15$) and small homogeneous fleets ($N \le 15$) where classical CBBA and Olfati-Saber flocking achieve parity ($98.1\%$ vs. $97.8\%$ TCR) and are recommended to avoid algebraic overhead.
   - *Zone III (Scalability Boundary):* Swarm densities exceeding $N > 250$ on embedded hardware where hierarchical cluster-sheaf decomposition is formally prescribed.
   - *Zone IV (Physical Breakdown Horizon):* Extreme RF jamming ($f_{\mathrm{jam}} \ge 0.85$, SNR $< -12\text{ dB}$) where Shannon channel capacity collapses to zero and physical optical/inertial fail-safes are mandated.
   - *Zone V (Sensor Starvation):* Degraded visual/LiDAR environments requiring covariance-inflated heartbeat fallbacks.

3. **Expanded Multi-Condition & Heterogeneity Benchmark Campaigns (Figures 5 & 6):**  
   - *Three Diverse Theaters:* Evaluated under identical jamming in Urban SAR Canyons (multipath/NLOS), Maritime Logistics (extended LOS over water), and Subterranean Rubble (severe waveguide attenuation).
   - *Three Fleet Heterogeneity Configurations:* Evaluated across Scout-Heavy, Balanced, and Leader-Heavy fleets, showing how cohomological obstructions are resolved across differing capability profiles.

4. **100% Numerical Consistency and Transparency:**  
   Every numerical claim in the abstract, introduction, text, tables, figures, and CSV datasets has been verified for complete mathematical harmony ($91.3\%$ TCR, $0.718$ SRI at $40\%$ attrition, $79.6\%$ bandwidth cut, $14.18\text{ ms}$ runtime at $N=200$, and zero inter-UAV collisions).

---

### Author Declarations & Compliance

- **Single Authorship:** The undersigned, Vishal Chandel, is the sole author of this work and assumes full scientific and editorial responsibility for its contents.
- **Originality & Prior Publication:** This manuscript represents original research and is not under consideration for publication elsewhere.
- **Competing Interests:** The author declares no competing financial or personal conflicts of interest.
- **Reproducibility & Open Science:** All raw simulation data, ROS 2 SITL integration scripts, extended benchmark runners, and visualization generators are organized in the project repository and are fully open for community replication.

We believe that this comprehensively revised manuscript offers substantial archival value, providing both profound theoretical insights into topological swarm resilience and actionable engineering principles for contested multi-robot operations. We look forward to your and the reviewers' constructive appraisal.

Sincerely yours,

**Vishal Chandel**  
Autonomous Systems and Swarm Robotics Laboratory  
Email: vishal.chandel.res@gmail.com  
