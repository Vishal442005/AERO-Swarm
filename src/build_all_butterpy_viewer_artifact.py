"""
build_all_butterpy_viewer_artifact.py
Builds an interactive Generative UI viewer artifact showcasing all 3 butterpy-generated flowcharts
and simplified block diagrams with pure black-and-white aesthetic (white boxes, black borders, black arrows, icons).
"""

import os
import base64

def load_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

brain_dir = "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e"

b64_fc1 = load_b64(os.path.join(brain_dir, "fig_flowchart1_sheaf_coordination.png"))
b64_fc2 = load_b64(os.path.join(brain_dir, "fig_flowchart2_ig_etc.png"))
b64_fc3 = load_b64(os.path.join(brain_dir, "fig_flowchart3_shata_auction.png"))
b64_ros2 = load_b64(os.path.join(brain_dir, "fig_ros2_architecture.png"))
b64_teaser = load_b64(os.path.join(brain_dir, "fig_teaser_sheaf_concept.png"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AERO-Swarm butterpy Flowcharts & Simple Block Diagrams</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --bg: #0F172A;
      --card: #1E293B;
      --text: #F8FAFC;
    }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .tab-btn.active {{
      background-color: #38BDF8;
      color: #0F172A;
      font-weight: 700;
    }}
  </style>
</head>
<body class="p-6 max-w-6xl mx-auto space-y-6">

  <!-- Header Banner -->
  <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/30 mb-2">
          <span>⚡ butterpy Extension</span>
          <span>•</span>
          <span>Ultra-Simple Flowcharts & Block Diagrams</span>
          <span>•</span>
          <span>Zero Box Color, Black Outlines & Arrows</span>
        </div>
        <h1 class="text-2xl font-bold tracking-tight text-white">AERO-Swarm Publication Diagrams (butterpy Suite)</h1>
        <p class="text-sm text-slate-400 mt-1">Strict publication minimalism: Pure white box fills, crisp black borders, black arrows, black text, and vector domain icons.</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Integrated into Section 3 of Both Manuscripts
        </span>
      </div>
    </div>
  </div>

  <!-- Interactive Tabs -->
  <div class="flex gap-2 border-b border-slate-800 pb-3 overflow-x-auto">
    <button onclick="switchTab('fc1')" id="tab-fc1" class="tab-btn active px-4 py-2 rounded-lg text-xs border border-slate-700 bg-slate-800 hover:bg-slate-700 transition">
      Flowchart 1: Sheaf Coordination
    </button>
    <button onclick="switchTab('fc2')" id="tab-fc2" class="tab-btn px-4 py-2 rounded-lg text-xs border border-slate-700 bg-slate-800 hover:bg-slate-700 transition">
      Flowchart 2: IG-ETC Communication
    </button>
    <button onclick="switchTab('fc3')" id="tab-fc3" class="tab-btn px-4 py-2 rounded-lg text-xs border border-slate-700 bg-slate-800 hover:bg-slate-700 transition">
      Flowchart 3: SHATA & Safety Simplex
    </button>
    <button onclick="switchTab('ros2')" id="tab-ros2" class="tab-btn px-4 py-2 rounded-lg text-xs border border-slate-700 bg-slate-800 hover:bg-slate-700 transition">
      Block Diagram: ROS 2 Pipeline
    </button>
    <button onclick="switchTab('teaser')" id="tab-teaser" class="tab-btn px-4 py-2 rounded-lg text-xs border border-slate-700 bg-slate-800 hover:bg-slate-700 transition">
      Block Diagram: Cellular Sheaf Concept
    </button>
  </div>

  <!-- Content Panels -->

  <!-- Panel 1: Flowchart 1 -->
  <div id="panel-fc1" class="tab-panel space-y-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
      <div class="flex items-center justify-between mb-3 px-2">
        <h2 class="text-sm font-semibold text-slate-200">Flowchart 1: Sheaf-Theoretic Distributed Swarm Coordination Pipeline</h2>
        <a href="data:image/png;base64,{b64_fc1}" download="fig_flowchart1_sheaf_coordination.png" class="text-xs px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700">
          Download 300 DPI PNG
        </a>
      </div>
      <div class="rounded-xl overflow-hidden border border-slate-800 bg-white p-4 flex justify-center">
        <img src="data:image/png;base64,{b64_fc1}" class="max-h-[750px] w-auto cursor-zoom-in" onclick="window.open(this.src)">
      </div>
      <p class="text-xs text-slate-400 text-center mt-3">Simple linear-branching flow: Swarm Init → Belief Dynamics → Sheaf Construction → Forman-Ricci Jamming Decision → Reweight / Nominal → Distributed Cochain Consensus → Actuation → Convergence.</p>
    </div>
  </div>

  <!-- Panel 2: Flowchart 2 -->
  <div id="panel-fc2" class="tab-panel hidden space-y-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
      <div class="flex items-center justify-between mb-3 px-2">
        <h2 class="text-sm font-semibold text-slate-200">Flowchart 2: Information-Geometric Event-Triggered Communication (IG-ETC)</h2>
        <a href="data:image/png;base64,{b64_fc2}" download="fig_flowchart2_ig_etc.png" class="text-xs px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700">
          Download 300 DPI PNG
        </a>
      </div>
      <div class="rounded-xl overflow-hidden border border-slate-800 bg-white p-4 flex justify-center">
        <img src="data:image/png;base64,{b64_fc2}" class="max-h-[750px] w-auto cursor-zoom-in" onclick="window.open(this.src)">
      </div>
      <p class="text-xs text-slate-400 text-center mt-3">Information-theoretic trigger logic: Belief Ingestion → Fisher-Rao Geodesic Distance → Dynamic Threshold → Divergence Check (Yes: Broadcast RF / No: Radio Silence 79.7% Saved) → Sync & Next Cycle.</p>
    </div>
  </div>

  <!-- Panel 3: Flowchart 3 -->
  <div id="panel-fc3" class="tab-panel hidden space-y-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
      <div class="flex items-center justify-between mb-3 px-2">
        <h2 class="text-sm font-semibold text-slate-200">Flowchart 3: Decentralized SHATA Auction & RTA Simplex Safety</h2>
        <a href="data:image/png;base64,{b64_fc3}" download="fig_flowchart3_shata_auction.png" class="text-xs px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700">
          Download 300 DPI PNG
        </a>
      </div>
      <div class="rounded-xl overflow-hidden border border-slate-800 bg-white p-4 flex justify-center">
        <img src="data:image/png;base64,{b64_fc3}" class="max-h-[750px] w-auto cursor-zoom-in" onclick="window.open(this.src)">
      </div>
      <p class="text-xs text-slate-400 text-center mt-3">Auction & Avionics Safety: Task Ingestion → Marginal Score Bidding → Sheaf Cochain Consensus → Outbid Decision (Re-bid Loop) → Safety Simplex CBF Check (Safe QP Fallback / Nominal Flight) → Motor Actuation.</p>
    </div>
  </div>

  <!-- Panel 4: ROS 2 Architecture -->
  <div id="panel-ros2" class="tab-panel hidden space-y-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
      <div class="flex items-center justify-between mb-3 px-2">
        <h2 class="text-sm font-semibold text-slate-200">Block Diagram: ROS 2 Humble Distributed Architecture</h2>
        <a href="data:image/png;base64,{b64_ros2}" download="fig_ros2_architecture.png" class="text-xs px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700">
          Download 300 DPI PNG
        </a>
      </div>
      <div class="rounded-xl overflow-hidden border border-slate-800 bg-white p-4 flex justify-center">
        <img src="data:image/png;base64,{b64_ros2}" class="max-h-[500px] w-auto cursor-zoom-in" onclick="window.open(this.src)">
      </div>
      <p class="text-xs text-slate-400 text-center mt-3">Pure black-and-white block diagram: PX4 Autopilot SITL → State Estimator EKF → IG-ETC Trigger Node → Sheaf Consensus & SCVI → RTA Safety Simplex Monitor.</p>
    </div>
  </div>

  <!-- Panel 5: Cellular Sheaf Concept -->
  <div id="panel-teaser" class="tab-panel hidden space-y-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
      <div class="flex items-center justify-between mb-3 px-2">
        <h2 class="text-sm font-semibold text-slate-200">Block Diagram: Cellular Sheaf Conceptual Architecture</h2>
        <a href="data:image/png;base64,{b64_teaser}" download="fig_teaser_sheaf_concept.png" class="text-xs px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-400 border border-slate-700">
          Download 300 DPI PNG
        </a>
      </div>
      <div class="rounded-xl overflow-hidden border border-slate-800 bg-white p-4 flex justify-center">
        <img src="data:image/png;base64,{b64_teaser}" class="max-h-[500px] w-auto cursor-zoom-in" onclick="window.open(this.src)">
      </div>
      <p class="text-xs text-slate-400 text-center mt-3">Pure black-and-white conceptual diagram: Leader UAV stalk (24D) and Scout UAV stalk (12D) mapped to Edge Stalk (6D) under RF Jamming.</p>
    </div>
  </div>

  <script>
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => {{
        b.classList.remove('active');
        b.classList.remove('bg-sky-400', 'text-slate-950');
        b.classList.add('bg-slate-800', 'text-slate-300');
      }});
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));

      const activeBtn = document.getElementById('tab-' + tabId);
      activeBtn.classList.add('active');
      activeBtn.classList.remove('bg-slate-800', 'text-slate-300');
      
      const panel = document.getElementById('panel-' + tabId);
      if (panel) {{
        panel.classList.remove('hidden');
      }}
    }}
  </script>
</body>
</html>
"""

out_html = os.path.join(brain_dir, "BUTTERPY_FLOWCHART_VIEWER.html")
with open(out_html, "w") as f:
    f.write(html_content)

print(f"Interactive viewer written to: {out_html}")
