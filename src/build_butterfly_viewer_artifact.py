"""
build_butterfly_viewer_artifact.py
Builds an interactive Generative UI viewer artifact for the AERO-Swarm Butterfly Flowchart.
"""

import os
import base64

img_path = "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e/fig_butterfly_flowchart.png"
with open(img_path, "rb") as f:
    b64_img = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AERO-Swarm Butterfly Flowchart Architecture</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --bg: #0B0F19;
      --card: #131B2E;
      --card-border: #1E293B;
      --text: #F8FAFC;
      --text-muted: #94A3B8;
      --accent-blue: #38BDF8;
      --accent-purple: #A855F7;
      --accent-emerald: #34D399;
    }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
  </style>
</head>
<body class="p-6 max-w-6xl mx-auto space-y-6">

  <!-- Header Banner -->
  <div class="bg-gradient-to-r from-blue-950 via-purple-950 to-emerald-950 border border-slate-800 rounded-2xl p-6 shadow-2xl">
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/30 mb-2">
          <span>🦋 Architecture Visualizer</span>
          <span>•</span>
          <span>Butterfly Flowchart Paradigm</span>
        </div>
        <h1 class="text-2xl font-bold tracking-tight text-white">AERO-Swarm Butterfly Flowchart System Architecture</h1>
        <p class="text-sm text-slate-400 mt-1">Symmetric two-wing topology: Convergent Inflow Threat Dynamics → Central Decision Core → Divergent Resilient Outflow</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Integrated in Section 3 of Both Manuscripts
        </span>
      </div>
    </div>
  </div>

  <!-- Flowchart Image Display Container -->
  <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl overflow-hidden">
    <div class="flex items-center justify-between mb-3 px-2">
      <h2 class="text-sm font-semibold text-slate-300 flex items-center gap-2">
        <span>High-Resolution Flowchart Render (300 DPI, Simple Shapes, Black Arrows & Icons)</span>
      </h2>
      <a href="data:image/png;base64,{b64_img}" download="fig_butterfly_flowchart.png" class="text-xs px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 transition">
        Download 300 DPI PNG (7090×2670)
      </a>
    </div>
    
    <div class="rounded-xl overflow-hidden border border-slate-800 bg-white p-2">
      <img src="data:image/png;base64,{b64_img}" alt="AERO-Swarm Butterfly Flowchart" class="w-full h-auto rounded-lg shadow-md cursor-zoom-in" onclick="window.open(this.src)">
    </div>
    <p class="text-xs text-slate-500 text-center mt-2 italic">Click image to expand in full resolution. Figure rendered using black arrows, crisp rounded shapes, and intuitive graphics/icons.</p>
  </div>

  <!-- Three Butterfly Zones Breakdown -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
    
    <!-- Left Wing -->
    <div class="bg-blue-950/30 border border-blue-900/40 rounded-xl p-5 space-y-3">
      <div class="flex items-center gap-2 text-blue-400 font-semibold text-sm">
        <span class="text-lg">🪽</span>
        <span>LEFT WING: Inflow & Threats</span>
      </div>
      <p class="text-xs text-slate-400 leading-relaxed">
        Heterogeneous platforms, sensory dynamics, and electronic warfare stress converge inward to the central core.
      </p>
      <ul class="text-xs space-y-2 text-slate-300">
        <li class="flex items-start gap-2 bg-blue-900/20 p-2 rounded-lg border border-blue-800/30">
          <span>🚁</span>
          <div>
            <strong class="text-blue-300">Heterogeneous Fleets:</strong> Scouts (<code class="text-sky-300 font-mono">d_v=12</code>), Leaders (<code class="text-sky-300 font-mono">d_v=24</code>), Relays (<code class="text-sky-300 font-mono">d_v=8</code>).
          </div>
        </li>
        <li class="flex items-start gap-2 bg-blue-900/20 p-2 rounded-lg border border-blue-800/30">
          <span>📊</span>
          <div>
            <strong class="text-blue-300">Belief Dynamics:</strong> Gaussian tracking <code class="text-sky-300 font-mono">N(μ, Σ)</code> on manifold <code class="text-sky-300 font-mono">P_+^6</code>.
          </div>
        </li>
        <li class="flex items-start gap-2 bg-blue-900/20 p-2 rounded-lg border border-blue-800/30">
          <span>📡</span>
          <div>
            <strong class="text-blue-300">Contested EW Threats:</strong> 0–80% directional RF jamming, GPS denial, 10–50% node attrition.
          </div>
        </li>
      </ul>
      <div class="text-[11px] text-blue-400/80 font-mono bg-blue-950/60 px-3 py-1.5 rounded border border-blue-800/40 text-center">
        Solid Black Arrows ➔ Converge to Center
      </div>
    </div>

    <!-- Central Pivot Core -->
    <div class="bg-purple-950/30 border border-purple-900/40 rounded-xl p-5 space-y-3">
      <div class="flex items-center gap-2 text-purple-400 font-semibold text-sm">
        <span class="text-lg">⚙️</span>
        <span>CENTRAL CORE: Decision Pivot</span>
      </div>
      <p class="text-xs text-slate-400 leading-relaxed">
        Unified algebraic topology and information geometry reconciling dimensional mismatches and early bottleneck detection.
      </p>
      <ul class="text-xs space-y-2 text-slate-300">
        <li class="flex items-start gap-2 bg-purple-900/20 p-2 rounded-lg border border-purple-800/30">
          <span>🧬</span>
          <div>
            <strong class="text-purple-300">Sheaf Restriction Kernel:</strong> Continuous SINR maps <code class="text-purple-300 font-mono">ρ_{{v⊴e}}(t)</code> over Sheaf Laplacian <code class="text-purple-300 font-mono">L_F</code>.
          </div>
        </li>
        <li class="flex items-start gap-2 bg-purple-900/20 p-2 rounded-lg border border-purple-800/30">
          <span>📐</span>
          <div>
            <strong class="text-purple-300">Bochner Curvature (SCVI):</strong> <code class="text-purple-300 font-mono">L_F = L_F^{{Bochner}} + Ric_F</code>. Zero percolation threshold guarantee!
          </div>
        </li>
        <li class="flex items-start gap-2 bg-purple-900/20 p-2 rounded-lg border border-purple-800/30">
          <span>⚡</span>
          <div>
            <strong class="text-purple-300">Fisher-Rao Event Gating:</strong> Transmit iff <code class="text-purple-300 font-mono">d_{{FR}} > δ_i(t)</code>. Slashes bandwidth by 79.7%.
          </div>
        </li>
      </ul>
      <div class="text-[11px] text-purple-400/80 font-mono bg-purple-950/60 px-3 py-1.5 rounded border border-purple-800/40 text-center">
        Microprocessor Core Engine
      </div>
    </div>

    <!-- Right Wing -->
    <div class="bg-emerald-950/30 border border-emerald-900/40 rounded-xl p-5 space-y-3">
      <div class="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
        <span class="text-lg">🪽</span>
        <span>RIGHT WING: Outflow & Execution</span>
      </div>
      <p class="text-xs text-slate-400 leading-relaxed">
        Decentralized bundle auctioning, hardware safety assurance, and multi-robot flight actuation branch out into mission success.
      </p>
      <ul class="text-xs space-y-2 text-slate-300">
        <li class="flex items-start gap-2 bg-emerald-900/20 p-2 rounded-lg border border-emerald-800/30">
          <span>🎯</span>
          <div>
            <strong class="text-emerald-300">SHATA Task Allocation:</strong> Polynomial <code class="text-emerald-300 font-mono">O(|V| M D_G)</code> conflict-free bundle auction.
          </div>
        </li>
        <li class="flex items-start gap-2 bg-emerald-900/20 p-2 rounded-lg border border-emerald-800/30">
          <span>🛡️</span>
          <div>
            <strong class="text-emerald-300">RTA Safety Simplex:</strong> Sub-1.2 ms CBF barrier override. Zero safety violations (<code class="text-emerald-300 font-mono">N_{{viol}}=0</code>).
          </div>
        </li>
        <li class="flex items-start gap-2 bg-emerald-900/20 p-2 rounded-lg border border-emerald-800/30">
          <span>✈️</span>
          <div>
            <strong class="text-emerald-300">PX4 Actuation & Formation:</strong> 50 Hz real-time flight control; >91.3% TCR preserved under 60% jamming.
          </div>
        </li>
      </ul>
      <div class="text-[11px] text-emerald-400/80 font-mono bg-emerald-950/60 px-3 py-1.5 rounded border border-emerald-800/40 text-center">
        Solid Black Arrows ➔ Diverge to Actuators
      </div>
    </div>

  </div>

  <!-- Verification Checklist -->
  <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
    <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Verification and Manuscript Placement Status</h3>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
        <div class="text-emerald-400 font-semibold">✓ IEEE T-Cyb Manuscript</div>
        <div class="text-slate-400 mt-1">Figure 2 in Section II-B / III (9 pages, IEEEtran)</div>
      </div>
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
        <div class="text-emerald-400 font-semibold">✓ Elsevier SWEVO/RAS</div>
        <div class="text-slate-400 mt-1">Figure 2 in Section 3 (14 pages, elsarticle)</div>
      </div>
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
        <div class="text-emerald-400 font-semibold">✓ GitHub Repository</div>
        <div class="text-slate-400 mt-1">results/fig_butterfly_flowchart.png committed</div>
      </div>
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
        <div class="text-emerald-400 font-semibold">✓ Release v1.0.0</div>
        <div class="text-slate-400 mt-1">Tagged live on GitHub (Vishal442005/AERO-Swarm)</div>
      </div>
    </div>
  </div>

</body>
</html>
"""

out_html = "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e/BUTTERFLY_FLOWCHART_VIEWER.html"
with open(out_html, "w") as f:
    f.write(html_content)

print(f"Butterfly Flowchart Viewer HTML written successfully to {out_html}")
