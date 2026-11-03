"""
build_butterpy_viewer_artifact.py
Builds an interactive Generative UI viewer artifact for the butterpy-generated flowchart.
"""

import os
import base64

img_path = "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e/fig_butterpy_flowchart.png"
with open(img_path, "rb") as f:
    b64_img = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AERO-Swarm Flowchart (Generated via butterpy)</title>
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
  <div class="bg-gradient-to-r from-blue-950 via-slate-900 to-emerald-950 border border-slate-800 rounded-2xl p-6 shadow-2xl">
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30 mb-2">
          <span>⚡ butterpy Python Extension</span>
          <span>•</span>
          <span>Simple Shapes & Black Arrows</span>
        </div>
        <h1 class="text-2xl font-bold tracking-tight text-white">AERO-Swarm Coordination & Resilience Flowchart</h1>
        <p class="text-sm text-slate-400 mt-1">Generated via <code class="text-sky-300 font-mono">butterpy</code>: Standard flowchart layout (rectangles, diamonds, capsules) with black arrows and domain graphics.</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Embedded in Section 3 of Both Manuscripts
        </span>
      </div>
    </div>
  </div>

  <!-- Flowchart Image Display Container -->
  <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl overflow-hidden">
    <div class="flex items-center justify-between mb-3 px-2">
      <h2 class="text-sm font-semibold text-slate-300 flex items-center gap-2">
        <span>High-Resolution butterpy Render (300 DPI, Simple Shapes, Black Arrows & Icons)</span>
      </h2>
      <a href="data:image/png;base64,{b64_img}" download="fig_butterpy_flowchart.png" class="text-xs px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700 transition">
        Download 300 DPI PNG (4770×2970)
      </a>
    </div>
    
    <div class="rounded-xl overflow-hidden border border-slate-800 bg-white p-2">
      <img src="data:image/png;base64,{b64_img}" alt="AERO-Swarm butterpy Flowchart" class="w-full h-auto rounded-lg shadow-md cursor-zoom-in" onclick="window.open(this.src)">
    </div>
    <p class="text-xs text-slate-500 text-center mt-2 italic">Click image to expand in full resolution. Pure flowchart layout: standard process rectangles, decision diamonds, terminal capsules, solid black arrows, and embedded domain icons.</p>
  </div>

  <!-- Flowchart Stages Breakdown -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
    
    <!-- Stage 1 -->
    <div class="bg-blue-950/30 border border-blue-900/40 rounded-xl p-5 space-y-3">
      <div class="flex items-center gap-2 text-blue-400 font-semibold text-sm">
        <span class="text-lg">1️⃣</span>
        <span>Perception & Gating</span>
      </div>
      <ul class="text-xs space-y-2 text-slate-300">
        <li class="flex items-start gap-2 bg-blue-900/20 p-2 rounded-lg border border-blue-800/30">
          <span>🚁</span>
          <div>
            <strong class="text-blue-300">Swarm Init:</strong> Heterogeneous fleet (<code class="text-sky-300 font-mono">V_scout, V_leader, V_relay</code>).
          </div>
        </li>
        <li class="flex items-start gap-2 bg-blue-900/20 p-2 rounded-lg border border-blue-800/30">
          <span>📡</span>
          <div>
            <strong class="text-blue-300">Belief Dynamics:</strong> Gaussian EKF odometry <code class="text-sky-300 font-mono">p_i(t) ∈ P_+^6</code>.
          </div>
        </li>
        <li class="flex items-start gap-2 bg-blue-900/20 p-2 rounded-lg border border-blue-800/30">
          <span>⚡</span>
          <div>
            <strong class="text-blue-300">Fisher-Rao Gating:</strong> Transmit iff <code class="text-sky-300 font-mono">d_{{FR}} ≥ δ_i(t)</code> (slashes bandwidth 79.7%).
          </div>
        </li>
      </ul>
    </div>

    <!-- Stage 2 -->
    <div class="bg-purple-950/30 border border-purple-900/40 rounded-xl p-5 space-y-3">
      <div class="flex items-center gap-2 text-purple-400 font-semibold text-sm">
        <span class="text-lg">2️⃣</span>
        <span>Sheaf Topology & Jamming</span>
      </div>
      <ul class="text-xs space-y-2 text-slate-300">
        <li class="flex items-start gap-2 bg-purple-900/20 p-2 rounded-lg border border-purple-800/30">
          <span>🧬</span>
          <div>
            <strong class="text-purple-300">Cellular Sheaf:</strong> Continuous restriction maps <code class="text-purple-300 font-mono">ρ_{{v⊴e}}(t)</code> & Sheaf Laplacian <code class="text-purple-300 font-mono">L_F</code>.
          </div>
        </li>
        <li class="flex items-start gap-2 bg-purple-900/20 p-2 rounded-lg border border-purple-800/30">
          <span>📐</span>
          <div>
            <strong class="text-purple-300">Bochner SCVI Check:</strong> <code class="text-purple-300 font-mono">κ_v(t) = λ_{{min}}(Ric_F) < 0?</code>
          </div>
        </li>
        <li class="flex items-start gap-2 bg-purple-900/20 p-2 rounded-lg border border-purple-800/30">
          <span>📡</span>
          <div>
            <strong class="text-purple-300">Jamming Reroute:</strong> Steer relays away from jamming cones.
          </div>
        </li>
      </ul>
    </div>

    <!-- Stage 3 -->
    <div class="bg-emerald-950/30 border border-emerald-900/40 rounded-xl p-5 space-y-3">
      <div class="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
        <span class="text-lg">3️⃣</span>
        <span>Auction, Safety & Actuation</span>
      </div>
      <ul class="text-xs space-y-2 text-slate-300">
        <li class="flex items-start gap-2 bg-emerald-900/20 p-2 rounded-lg border border-emerald-800/30">
          <span>🎯</span>
          <div>
            <strong class="text-emerald-300">SHATA Auction:</strong> Bundle insertion & cochain consensus.
          </div>
        </li>
        <li class="flex items-start gap-2 bg-emerald-900/20 p-2 rounded-lg border border-emerald-800/30">
          <span>🛡️</span>
          <div>
            <strong class="text-emerald-300">RTA Simplex Check:</strong> Sub-1.2 ms certified fallback override. Zero violations (<code class="text-emerald-300 font-mono">N_{{viol}}=0</code>).
          </div>
        </li>
        <li class="flex items-start gap-2 bg-emerald-900/20 p-2 rounded-lg border border-emerald-800/30">
          <span>✈️</span>
          <div>
            <strong class="text-emerald-300">PX4 Flight Actuation:</strong> 50 Hz SE(3) tracking & resilient formation.
          </div>
        </li>
      </ul>
    </div>

  </div>

  <!-- Verification Checklist -->
  <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
    <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Manuscript Verification Status (Section 3)</h3>
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
        <div class="text-emerald-400 font-semibold">✓ butterpy Extension</div>
        <div class="text-slate-400 mt-1">Created in src/butterpy/</div>
      </div>
      <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
        <div class="text-emerald-400 font-semibold">✓ GitHub Repository</div>
        <div class="text-slate-400 mt-1">Committed to Vishal442005/AERO-Swarm</div>
      </div>
    </div>
  </div>

</body>
</html>
"""

out_html = "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e/BUTTERPY_FLOWCHART_VIEWER.html"
with open(out_html, "w") as f:
    f.write(html_content)

print(f"butterpy Flowchart Viewer HTML written successfully to {out_html}")
