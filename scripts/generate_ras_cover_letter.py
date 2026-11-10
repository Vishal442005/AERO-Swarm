"""
scripts/generate_ras_cover_letter.py
Generates professional, publication-grade DOCX cover letters for:
Robotics and Autonomous Systems (RAS) - Elsevier
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_horizontal_rule(doc, color_hex="0F766E", size_pt=2.0):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="{int(size_pt*8)}" w:space="1" w:color="{color_hex}"/></w:pBdr>')
    p._p.get_or_add_pPr().append(pBdr)

def build_ras_cover_letter(output_path):
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10.0)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Letterhead
    p_head = doc.add_paragraph()
    p_head.paragraph_format.space_after = Pt(2)
    run_org = p_head.add_run("DEPARTMENT OF ELECTRONICS AND COMMUNICATION ENGINEERING")
    run_org.bold = True
    run_org.font.size = Pt(12)
    run_org.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(4)
    run_sub = p_sub.add_run("Jawaharlal Nehru Government Engineering College (JNGEC)\nSundernagar, Mandi, Himachal Pradesh 175018, India • Email: chandelvishal445@gmail.com")
    run_sub.font.size = Pt(8.5)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    add_horizontal_rule(doc, color_hex="0F766E", size_pt=2.0)
    
    # Date & Recipient
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_after = Pt(6)
    r_date = p_date.add_run("Date: November 10, 2026\n")
    r_date.bold = True
    p_date.add_run("To: Prof. Dr. Karsten Berns, Prof. Maria Gini, and Prof. Jun Ota\n")
    p_date.add_run("Editors-in-Chief and Editorial Board\n")
    r_recip = p_date.add_run("Robotics and Autonomous Systems\n")
    r_recip.bold = True
    r_recip.font.color.rgb = RGBColor(15, 118, 110)
    p_date.add_run("Elsevier ScienceDirect Journals")
    
    # Subject Callout Box
    table_subj = doc.add_table(rows=1, cols=1)
    table_subj.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_s = table_subj.cell(0, 0)
    set_cell_background(cell_s, "F0FDFA")
    set_cell_margins(cell_s, top=140, bottom=140, left=200, right=200)
    p_subj = cell_s.paragraphs[0]
    p_subj.paragraph_format.space_before = Pt(2)
    p_subj.paragraph_format.space_after = Pt(2)
    r_st = p_subj.add_run("SUBJECT: SUBMISSION OF ORIGINAL REGULAR RESEARCH MANUSCRIPT\n")
    r_st.bold = True
    r_st.font.size = Pt(9.5)
    r_st.font.color.rgb = RGBColor(13, 148, 136)
    
    r_title = p_subj.add_run("Title: ")
    r_title.bold = True
    r_title.font.size = Pt(10.0)
    r_title_txt = p_subj.add_run("“AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments”\n")
    r_title_txt.bold = True
    r_title_txt.font.size = Pt(10.0)
    r_title_txt.font.color.rgb = RGBColor(15, 23, 42)
    
    r_meta = p_subj.add_run("Manuscript Type: Original Full-Length Research Article (22 pages, Elsevier elsarticle format) • Field: Autonomous Multi-Robot Systems")
    r_meta.font.size = Pt(8.5)
    r_meta.font.italic = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Salutation & Body
    p_body1 = doc.add_paragraph()
    p_body1.paragraph_format.space_after = Pt(6)
    p_body1.add_run("Dear Editors-in-Chief Prof. Berns, Prof. Gini, Prof. Ota, and Esteemed Editorial Board,\n\n")
    p_body1.add_run(
        "We are pleased to submit our original research manuscript entitled above for publication as a Full-Length Research Article in "
    )
    r_j = p_body1.add_run("Robotics and Autonomous Systems")
    r_j.bold = True
    p_body1.add_run(
        ". In this work, we present AERO-Swarm (Adaptive Edge-Resilient Optimization for Heterogeneous Swarms), a novel decentralized coordination, task allocation, and provably safe control framework engineered for heterogeneous aerial robot fleets operating in contested, GPS-denied environments."
    )
    
    p_body2 = doc.add_paragraph()
    p_body2.paragraph_format.space_after = Pt(6)
    r_mhead = p_body2.add_run("Motivation and Technical Challenges: ")
    r_mhead.bold = True
    p_body2.add_run(
        "Deploying autonomous multi-UAV swarms in complex subterranean search-and-rescue, environmental disaster mapping, and tactical inspection fundamentally necessitates functional heterogeneity (coupling agile monocular scouts, heavy 3D LiDAR mapping leaders, and long-range communication relays). However, state-of-the-art multi-robot algorithms (such as CBBA and standard Graph-Laplacian flocking) rely on flat scalar graphs G=(V, E) and presuppose identical observation-action manifolds. Under severe directional radio-frequency (RF) jamming, moving physical obstacles, and node attrition, classical algorithms suffer catastrophic failure: flat graph Laplacians undergo percolation phase collapse at ~35% edge loss, auction heuristics accumulate cyclic outbidding deadlocks, and periodic RF broadcasts flood the wireless spectrum."
    )
    
    p_contrib_head = doc.add_paragraph()
    p_contrib_head.paragraph_format.space_after = Pt(4)
    r_ch = p_contrib_head.add_run("Core Methodological Contributions of AERO-Swarm:")
    r_ch.bold = True
    r_ch.font.color.rgb = RGBColor(15, 118, 110)
    
    contribs = [
        ("Heterogeneous Cellular Sheaf Modeling: ",
         "We establish the first cellular sheaf architecture for 6-DoF aerial swarms. Disparate robotic state spaces F_v = R^{d_v} (Scouts: R^12, Leaders: R^24, Relays: R^8) are reconciled over mutual edge stalks F_e = R^6 via continuous, SINR-modulated restriction maps rho_{v⊴e}(t) = sqrt(gamma_e(t)) P_v, preserving algebraic connectivity across dimensional mismatches."),
        ("Bochner Curvature Decomposition & Zero-Percolation Decay: ",
         "Via discrete Bochner--Weitzenböck decomposition L_F = L_F^{Bochner} + Ric_F^{Forman}, we formulate the local Sheaf Curvature Vulnerability Index (SCVI) to proactively identify jamming bottlenecks. We prove (Theorem 1) that sheaf consensus resilience degrades strictly linearly (SRI >= SRI_0(1 - c_F f_jam)), eliminating the catastrophic percolation phase collapse inherent in scalar graphs."),
        ("Fisher-Rao Information-Geometric Event Triggering (IG-ETC): ",
         "To mitigate wireless spectrum congestion, transmissions are gated on the Riemannian Gaussian belief manifold P_+^6, firing if and only if the Fisher-Rao geodesic distance exceeds an energy-annealed threshold. This slashes RF communication bandwidth by an exact 79.6% without tracking or consensus degradation."),
        ("Sheaf Heterogeneous Auction for Task Allocation (SHATA): ",
         "We formulate SHATA, incorporating local sheaf connectivity discounting and first-cohomology group (dim H^1) harmonic projection. We prove conflict-free convergence in O(|V| M D_G) iterations and formalize (Proposition 1) that per-agent computation is O(d_v^2 + M), strictly independent of total swarm size N."),
        ("Hardware-Isolated Run-Time Assurance (RTA) Safety Simplex: ",
         "To ensure certified collision-freedom in obstacle-dense canyons, each drone integrates a formal RTA Simplex monitor enforcing high-order Control Barrier Functions (CBFs). A closed-form minimum-intervention quadratic program (QP) overrides high-level setpoints within <1.2 ms, provably guaranteeing forward invariance of safe set C.")
    ]
    
    for title, desc in contribs:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.left_indent = Inches(0.2)
        p_c.paragraph_format.space_after = Pt(2.5)
        r_t = p_c.add_run("• " + title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(15, 23, 42)
        p_c.add_run(desc)
        
    p_val = doc.add_paragraph()
    p_val.paragraph_format.space_before = Pt(4)
    p_val.paragraph_format.space_after = Pt(6)
    r_vh = p_val.add_run("Comprehensive Dual-Tier Validation Campaign: ")
    r_vh.bold = True
    p_val.add_run(
        "Our framework is validated across a rigorous dual-tier pipeline: (1) Tier-1 multi-core parallel sweeps benchmarking fleet scalability (N=10 to 200), RF jamming (0% to 80%), and physical node attrition (10% to 50%) over 50 Monte Carlo trials, substantiated by non-parametric Wilcoxon signed-rank tests (p < 10^-6 to p < 10^-12, Cohen's d = 2.45 to 4.12) and Friedman tests (chi_F^2 = 184.6, p < 10^-15), where AERO-Swarm preserves 91.3% TCR under 60% jamming; (2) Tier-2 production-ready ROS 2 Humble deployment over CycloneDDS with PX4 SITL autopilot integration, achieving zero safety violations (N_viol = 0) in dense 3D obstacle canyons with 44.8 μs P99 QP solve latency (33x below the SAE ARP4754B 1.5 ms limit)."
    )
    
    p_align = doc.add_paragraph()
    p_align.paragraph_format.space_before = Pt(2)
    p_align.paragraph_format.space_after = Pt(6)
    r_ah = p_align.add_run("Direct Alignment with Robotics and Autonomous Systems: ")
    r_ah.bold = True
    p_align.add_run(
        "This manuscript directly addresses core topics of Robotics and Autonomous Systems, including autonomous multi-robot coordination, heterogeneous aerial swarms, safety-critical control barrier functions, distributed task allocation, and real-time ROS 2 software architectures. The blend of rigorous mathematical topology and field-ready robotic implementation makes this paper an ideal fit for the readership of RAS."
    )
    
    # Suggested Reviewers
    p_rev = doc.add_paragraph()
    p_rev.paragraph_format.space_after = Pt(4)
    r_rh = p_rev.add_run("Suggested Expert Reviewers:\n")
    r_rh.bold = True
    p_rev.add_run("1. Prof. Vijay Kumar (University of Pennsylvania, USA) — kumar@seas.upenn.edu (Multi-robot aerial swarms, autonomy)\n")
    p_rev.add_run("2. Prof. Magnus Egerstedt (University of California, Irvine, USA) — magnus@uci.edu (Control Barrier Functions, multi-agent safety)\n")
    p_rev.add_run("3. Prof. Michael Schwager (Stanford University, USA) — schwager@stanford.edu (Distributed multi-robot task allocation)\n")
    p_rev.add_run("4. Prof. Florian Bullo (University of California, Santa Barbara, USA) — bullo@engineering.ucsb.edu (Networked robotic systems, consensus)\n")
    p_rev.add_run("5. Prof. Pietro Liò (University of Cambridge, UK) — pl219@cam.ac.uk (Cellular sheaf Laplacians, topological learning)")
    
    # Declarations
    p_decl = doc.add_paragraph()
    p_decl.paragraph_format.space_before = Pt(2)
    p_decl.paragraph_format.space_after = Pt(6)
    r_dh = p_decl.add_run("Declarations and Open-Science Reproducibility:\n")
    r_dh.bold = True
    p_decl.add_run("1. Originality: The paper is original, has not been published previously, and is not under consideration elsewhere.\n")
    p_decl.add_run("2. Author Approval: The author has reviewed, verified, and approved the submitted manuscript in its entirety.\n")
    p_decl.add_run("3. Competing Interests: The author declares no competing financial, commercial, or personal interests.\n")
    p_decl.add_run("4. Code & Artifact Availability: The complete codebase—including ROS 2 Humble packages, micro-XRCE-DDS bridge configurations, evaluation scripts, and benchmark telemetry—is publicly available at: ")
    r_gh = p_decl.add_run("https://github.com/Vishal442005/AERO-Swarm")
    r_gh.bold = True
    r_gh.font.color.rgb = RGBColor(13, 148, 136)
    p_decl.add_run(" (Release v1.0.0).")
    
    # Closing
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(4)
    p_close.paragraph_format.space_after = Pt(12)
    p_close.add_run("Thank you very much for considering our manuscript for publication in Robotics and Autonomous Systems.\n\n")
    r_sig = p_close.add_run("Sincerely yours,\n\n")
    r_sig.font.italic = True
    
    r_team = p_close.add_run("Vishal Chandel\n")
    r_team.bold = True
    p_close.add_run("Department of Electronics and Communication Engineering\nJawaharlal Nehru Government Engineering College (JNGEC), Sundernagar\nMandi, Himachal Pradesh 175018, India\nEmail: chandelvishal445@gmail.com")
    
    doc.save(output_path)
    print(f"Successfully generated RAS Cover Letter: {output_path}")

if __name__ == "__main__":
    targets = [
        "submission_elseiver_(SWEVO)_RAS/COVER_LETTER_RAS.docx",
        "submission_elseiver_(SWEVO)_RAS/COVER_LETTER_ELSEVIER_SWEVO_RAS.docx"
    ]
    for t in targets:
        build_ras_cover_letter(t)
