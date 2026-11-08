# Table 1: Systematic Comparative Analysis: AERO-Swarm vs. State-of-the-Art Multi-Robot Paradigms

| Framework | Topological Model | Stalk Heterogeneity | Jamming Resilience | Comm. Efficiency | Dynamic Scalability | Safety Assurance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Standard CBBA** (Choi et al., 2009) | Flat Graph $G(V,E)$ | None (Scalar bids) | Fragile (Percolation collapse) | Low (100% periodic) | $\mathcal{O}(\vert V \vert^2)$ | None (Heuristic) |
| **Flocking Consensus** (Olfati-Saber, 2006) | Scalar Graph Laplacian | None (Homogeneous) | Fails under DoS | Medium (100% periodic) | $\mathcal{O}(\vert V \vert \cdot d)$ | Barrier certificates |
| **Phy-GAIL Swarms** (2026) | Physics-Informed GNN | Fixed-dim embedding | Moderate (GNN-learned) | Low (100% sync) | $\mathcal{O}(\vert V \vert \cdot \vert \mathcal{N} \vert)$ | Soft reward penalty |
| **AC-MASAC** (2026) | CTDE Attention | Shared feature size | Fragile (Out-of-distribution) | High (Learned policy) | $\mathcal{O}(\vert V \vert^2)$ attention | Empirical only |
| **Byzantine Consensus** (Sun et al., 2025) | Digraph Laplacian | Homogeneous states | High (Malicious nodes) | Medium (Triggered) | $\mathcal{O}(\vert V \vert^2)$ | Lyapunov stability |
| **AERO-Swarm (Ours)** | **Cellular Sheaf** $(\mathcal{F}, G)$ | **Asymmetric** ($\mathcal{F}_v \neq \mathcal{F}_w$) | **High** ($\text{SRI} \propto 1 - c f_{\mathrm{jam}}$) | **Ultra-Low** ($\mathbf{79.6\%}$ cut) | $\boldsymbol{\mathcal{O}(\vert V \vert d_{\max}^3)}$ | **Hardware RTA Simplex** |
