# Table 3: Factorial Ablation Analysis of AERO-Swarm Core Architectural Modules
*(N=100 Heterogeneous UAV Fleet, 60% RF Jamming Sweep, 50 Monte Carlo Trials)*

| Ablation Configuration | TCR (%) | SRI at 40% Attrition | Bandwidth Cut (%) | Loop Latency (ms) | Safety Violations ($N_{\mathrm{viol}}$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **(1) Full AERO-Swarm (Proposed)** | **91.3% ± 1.8%**† | **0.718 ± 0.03**† | **-79.6%**† | 4.92 ± 0.15 | **0**† |
| • w/o Bochner SCVI Rerouting | 74.2% ± 3.1% | 0.620 ± 0.04 | -78.4% | 4.65 ± 0.12 | 0 |
| • w/o Cellular Sheaf (Flat Graph + CBBA) | 34.6% ± 4.5% | 0.112 ± 0.04 | -71.2% | 4.10 ± 0.11 | 2.4 ± 0.8 |
| • w/o IG-ETC (Periodic 20 Hz Broadcast) | 81.5% ± 2.4% | 0.715 ± 0.03 | 0% (Baseline) | 5.85 ± 0.18 | 0 |
| • Euclidean ETC (in place of Fisher-Rao) | 78.9% ± 2.8% | 0.712 ± 0.03 | -45.6% | 4.88 ± 0.14 | 0 |
| • w/o RTA Simplex (Unconstrained Policy) | 89.4% ± 2.0% | 0.718 ± 0.03 | -79.6% | 4.41 ± 0.12 | 16.8 ± 3.2 |

*† Indicates statistical superiority (p < 0.001, Wilcoxon signed-rank test).*
