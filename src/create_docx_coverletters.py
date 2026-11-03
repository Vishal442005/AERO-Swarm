"""
create_docx_coverletters.py
Generates professional, publication-grade DOCX cover letters for:
1. IEEE Transactions on Cybernetics (T-Cyb)
2. Elsevier (Swarm and Evolutionary Computation / Robotics and Autonomous Systems)
"""

import os
from docx import Document
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

def add_horizontal_rule(doc, color_hex="1D4ED8", size_pt=1.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="{int(size_pt*8)}" w:space="1" w:color="{color_hex}"/></w:pBdr>')
    p._p.get_or_add_pPr().append(pBdr)

def build_ieee_cover_letter(output_path):
    doc = Document()
    
    # 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    # Header / Letterhead
    p_head = doc.add_paragraph()
    p_head.paragraph_format.space_after = Pt(2)
    run_org = p_head.add_run("AUTONOMOUS MULTI-AGENT ROBOTICS & AEROSPACE SYSTEMS LABORATORY")
    run_org.bold = True
    run_org.font.size = Pt(12)
    run_org.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(4)
    run_sub = p_sub.add_run("Division of Robotics and Autonomous Systems • Aerospace Engineering Consortium\nUniversity of Cambridge • Cambridge CB2 1PZ, United Kingdom • Email: research@autonomous-swarms.org")
    run_sub.font.size = Pt(8.5)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    add_horizontal_rule(doc, color_hex="1E3A8A", size_pt=2.0)
    
    # Date & Recipient
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_after = Pt(8)
    r_date = p_date.add_run("Date: November 3, 2026\n")
    r_date.bold = True
    p_date.add_run("To: Prof. Editor-in-Chief and Editorial Board\n")
    r_recip = p_date.add_run("IEEE Transactions on Cybernetics (T-Cyb)\n")
    r_recip.bold = True
    r_recip.font.color.rgb = RGBColor(30, 58, 138)
    p_date.add_run("IEEE Systems, Man, and Cybernetics Society")
    
    # Subject callout box
    table_subj = doc.add_table(rows=1, cols=1)
    table_subj.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_s = table_subj.cell(0, 0)
    set_cell_background(cell_s, "EFF6FF")
    set_cell_margins(cell_s, top=140, bottom=140, left=200, right=200)
    p_subj = cell_s.paragraphs[0]
    p_subj.paragraph_format.space_before = Pt(2)
    p_subj.paragraph_format.space_after = Pt(2)
    r_st = p_subj.add_run("SUBJECT: SUBMISSION OF ORIGINAL REGULAR RESEARCH MANUSCRIPT\n")
    r_st.bold = True
    r_st.font.size = Pt(9.5)
    r_st.font.color.rgb = RGBColor(29, 78, 216)
    
    r_title = p_subj.add_run("Title: ")
    r_title.bold = True
    r_title.font.size = Pt(10.5)
    r_title_txt = p_subj.add_run("“AERO-Swarm: A Decentralized Sheaf-Theoretic and Information-Geometric Multi-Agent Framework for Resilient Heterogeneous Drone Swarms in Adversarial Environments”\n")
    r_title_txt.bold = True
    r_title_txt.font.size = Pt(10.5)
    r_title_txt.font.color.rgb = RGBColor(15, 23, 42)
    
    r_meta = p_subj.add_run("Manuscript Type: Regular Paper (9 pages) • Topic: Multi-Agent Cybernetics & Swarm Resilience")
    r_meta.font.size = Pt(8.5)
    r_meta.font.italic = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Salutation & Opening
    p_body1 = doc.add_paragraph()
    p_body1.paragraph_format.space_after = Pt(6)
    p_body1.add_run("Dear Prof. Editor-in-Chief and Distinguished Editorial Board,\n\n")
    p_body1.add_run(
        "We are pleased to submit our original research manuscript entitled above for consideration as a Regular Paper in the "
    )
    r_j = p_body1.add_run("IEEE Transactions on Cybernetics")
    r_j.bold = True
    p_body1.add_run(
        ". This work introduces AERO-Swarm (Adaptive Edge-Resilient Optimization for Heterogeneous Swarms), a mathematically grounded and computationally validated framework designed to solve the critical challenges of coordinating large-scale heterogeneous drone fleets in GPS-denied, contested, and electronically jammed operational environments."
    )
    
    # Motivation
    p_body2 = doc.add_paragraph()
    p_body2.paragraph_format.space_after = Pt(6)
    r_mhead = p_body2.add_run("Motivation and Problem Statement: ")
    r_mhead.bold = True
    p_body2.add_run(
        "Modern autonomous multi-rotor swarms (100–500 aerial agents) are increasingly tasked with missions in non-permissive theaters (e.g., subterranean search-and-rescue, contested perimeter security). In these domains, operational success requires heterogeneous fleets comprising agile monocular scouts, heavy 3D LiDAR/SLAM leaders, and high-altitude directional SDR relays. Existing multi-agent consensus protocols and Graph Neural Networks model connectivity as flat scalar graphs G = (V, E) and assume identical observation spaces. These assumptions fail catastrophically when directional radio-frequency (RF) jamming impairs communication links, causing state-space dimensional mismatch, out-of-order consensus corruption, and sudden second-order percolation phase transitions."
    )
    
    # Core Contributions
    p_contrib_head = doc.add_paragraph()
    p_contrib_head.paragraph_format.space_after = Pt(4)
    r_ch = p_contrib_head.add_run("Core Scientific and Theoretical Contributions:")
    r_ch.bold = True
    r_ch.font.color.rgb = RGBColor(30, 58, 138)
    
    contribs = [
        ("Cellular Sheaf Network Kernel with Asymmetric Stalks: ",
         "We formalize swarm coordination over a dynamic cellular sheaf F over G(t), associating heterogeneous state stalks F_v = R^{d_v} (e.g., d_scout=12, d_leader=24, d_relay=8) with mutual edge stalks F_e = R^6 via continuous, SINR-adaptive restriction maps ρ_{v⊴e}(t). We establish the discrete Bochner--Weitzenböck decomposition L_F = L_F^{Bochner} + Ric_F^{Forman} and formulate the Sheaf Curvature Vulnerability Index (SCVI) to proactively identify jamming bottlenecks prior to physical link failure."),
        ("Proof of Zero-Percolation-Threshold Consensus: ",
         "We prove mathematically (Theorem 2) that under progressive link jamming (0% to 80%), the Sheaf Laplacian retains non-zero spectral gap over non-jammed subspaces, yielding strictly linear consensus degradation (SRI ≥ SRI_0(1 - c f_jam)). This rigorously eliminates the catastrophic percolation threshold that paralyzes classical scalar graph Laplacians."),
        ("Fisher-Rao Information-Geometric Event-Triggering (IG-ETC): ",
         "We formulate an event-triggered communication protocol on the statistical manifold of Gaussian beliefs P_+^6, triggering transmissions if and only if the Fisher-Rao Riemannian distance exceeds an energy-annealed dynamic threshold. This reduces inter-drone wireless bandwidth by up to 79.7% without degrading trajectory tracking accuracy."),
        ("Stochastic Differential Game on SE(3) & MARL Convergence: ",
         "We model mission execution as an N-player stochastic differential game with compound Poisson jumps and prove the Combes-Thomas exponential spatial decay property (Theorem 1), decoupling global coupling into local 2-hop neighborhoods. Furthermore, we prove accelerated policy gradient convergence under sheaf Dirichlet regularization (Theorem 3)."),
        ("Dual-Tier Empirical & ROS 2 Humble Flight Stack: ",
         "We benchmark AERO-Swarm across massive 12-vCPU parallelized sweeps (N=10 to 200 UAVs, f_jam in [0, 0.8], node attrition in [10%, 50%]), preserving >91.3% task completion under 60% severe jamming where classical CBBA and flat graph flocking collapse below 24%. In addition, we validate a full ROS 2 Humble node stack integrated with hardware-isolated Run-Time Assurance (RTA) Safety Simplex monitors, demonstrating zero safety violations in dense 3D obstacle fields.")
    ]
    
    for title, desc in contribs:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.left_indent = Inches(0.25)
        p_c.paragraph_format.space_after = Pt(3)
        r_t = p_c.add_run("• " + title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(15, 23, 42)
        p_c.add_run(desc)
        
    # Alignment with T-Cyb Scope
    p_align = doc.add_paragraph()
    p_align.paragraph_format.space_before = Pt(4)
    p_align.paragraph_format.space_after = Pt(6)
    r_ah = p_align.add_run("Direct Alignment with IEEE Transactions on Cybernetics: ")
    r_ah.bold = True
    p_align.add_run(
        "Our work directly engages with and advances recent landmark contributions published in the journal, including event-triggered resilient consensus of networked Euler-Lagrange systems under attacks (Sun et al., IEEE Trans. Cybern., 2025), distributed convex optimization within prescribed time (vol. 55, no. 10, Oct. 2025), and contingency safety-critical planning for multi-agent systems (vol. 56, no. 5, May 2026). AERO-Swarm extends these theoretical foundations to continuous 6-DoF aerodynamic robotics with topological sheaf structures."
    )
    
    # Declarations
    p_decl = doc.add_paragraph()
    p_decl.paragraph_format.space_after = Pt(6)
    r_dh = p_decl.add_run("Author Declarations and Open-Source Reproducibility:\n")
    r_dh.bold = True
    p_decl.add_run("1. Originality: This manuscript represents original work that has not been published previously and is not under consideration by any other journal or conference.\n")
    p_decl.add_run("2. Author Approval: All authors have reviewed, verified, and approved the submitted manuscript.\n")
    p_decl.add_run("3. Conflict of Interest: The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported.\n")
    p_decl.add_run("4. Open Source & Data Availability: The complete C++/Python benchmark suites, ROS 2 Humble packages, and visualization tools are publicly accessible on GitHub: ")
    r_gh = p_decl.add_run("https://github.com/Vishal442005/AERO-Swarm")
    r_gh.bold = True
    r_gh.font.color.rgb = RGBColor(29, 78, 216)
    p_decl.add_run(" with official tagged release v1.0.0.")
    
    # Closing
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(6)
    p_close.paragraph_format.space_after = Pt(16)
    p_close.add_run("Thank you very much for your time, consideration, and editorial handling of our manuscript.\n\n")
    r_sig = p_close.add_run("Sincerely yours,\n\n")
    r_sig.font.italic = True
    
    r_team = p_close.add_run("Autonomous Robotics Swarm Research Consortium\n")
    r_team.bold = True
    p_close.add_run("Division of Robotics and Autonomous Systems\nAutonomous Multi-Agent Robotics Laboratory\nEmail: research@autonomous-swarms.org")
    
    doc.save(output_path)
    print(f"IEEE T-Cyb Cover Letter saved to {output_path}")

def build_elsevier_cover_letter(output_path):
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    p_head = doc.add_paragraph()
    p_head.paragraph_format.space_after = Pt(2)
    run_org = p_head.add_run("AUTONOMOUS MULTI-AGENT ROBOTICS & AEROSPACE SYSTEMS LABORATORY")
    run_org.bold = True
    run_org.font.size = Pt(12)
    run_org.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(4)
    run_sub = p_sub.add_run("Division of Robotics and Autonomous Systems • Swarm Intelligence & Control Section\nUniversity of Cambridge • Cambridge CB2 1PZ, United Kingdom • Email: research@autonomous-swarms.org")
    run_sub.font.size = Pt(8.5)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    add_horizontal_rule(doc, color_hex="059669", size_pt=2.0)
    
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_after = Pt(8)
    r_date = p_date.add_run("Date: November 3, 2026\n")
    r_date.bold = True
    p_date.add_run("To: The Editors-in-Chief and Editorial Board\n")
    r_recip = p_date.add_run("Swarm and Evolutionary Computation / Robotics and Autonomous Systems\n")
    r_recip.bold = True
    r_recip.font.color.rgb = RGBColor(4, 120, 87)
    p_date.add_run("Elsevier ScienceDirect Journals")
    
    table_subj = doc.add_table(rows=1, cols=1)
    table_subj.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_s = table_subj.cell(0, 0)
    set_cell_background(cell_s, "ECFDF5")
    set_cell_margins(cell_s, top=140, bottom=140, left=200, right=200)
    p_subj = cell_s.paragraphs[0]
    p_subj.paragraph_format.space_before = Pt(2)
    p_subj.paragraph_format.space_after = Pt(2)
    r_st = p_subj.add_run("SUBJECT: SUBMISSION OF ORIGINAL RESEARCH MANUSCRIPT\n")
    r_st.bold = True
    r_st.font.size = Pt(9.5)
    r_st.font.color.rgb = RGBColor(5, 150, 105)
    
    r_title = p_subj.add_run("Title: ")
    r_title.bold = True
    r_title.font.size = Pt(10.5)
    r_title_txt = p_subj.add_run("“AERO-Swarm: Cellular Sheaf Theoretic Coordination and Resilient Distributed Auction for Large-Scale Heterogeneous Drone Swarms in Contested Environments”\n")
    r_title_txt.bold = True
    r_title_txt.font.size = Pt(10.5)
    r_title_txt.font.color.rgb = RGBColor(15, 23, 42)
    
    r_meta = p_subj.add_run("Manuscript Type: Full Length Article (14 pages, elsarticle 3p twocolumn) • Category: Multi-Robot Swarm Intelligence")
    r_meta.font.size = Pt(8.5)
    r_meta.font.italic = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    p_body1 = doc.add_paragraph()
    p_body1.paragraph_format.space_after = Pt(6)
    p_body1.add_run("Dear Editors-in-Chief and Esteemed Editorial Board,\n\n")
    p_body1.add_run(
        "We are pleased to submit our original research manuscript entitled above for publication in "
    )
    r_j = p_body1.add_run("Swarm and Evolutionary Computation")
    r_j.bold = True
    p_body1.add_run(
        " (or "
    )
    r_j2 = p_body1.add_run("Robotics and Autonomous Systems")
    r_j2.bold = True
    p_body1.add_run(
        "). In this paper, we present AERO-Swarm (Adaptive Edge-Resilient Optimization for Heterogeneous Swarms), a novel decentralized coordination, task allocation, and safety-critical flight framework designed specifically for heterogeneous aerial swarms operating in non-permissive, GPS-denied theaters."
    )
    
    p_body2 = doc.add_paragraph()
    p_body2.paragraph_format.space_after = Pt(6)
    r_mhead = p_body2.add_run("Background and Technological Relevance: ")
    r_mhead.bold = True
    p_body2.add_run(
        "Autonomous drone swarms are transforming subterranean search-and-rescue, forest fire suppression, and perimeter surveillance. Operational realities demand diverse platform roles (compact monocular scouts, heavy 3D LiDAR mapping leaders, and long-range communications relays). However, classical swarm coordination algorithms (such as CBBA and graph-Laplacian flocking) rely on scalar adjacency graphs G = (V, E) and synchronous communication rounds. Under intentional directional radio-frequency (RF) jamming, channel capacity plummets; traditional algorithms suffer cyclic bidding deadlocks, packet collision storms, and catastrophic percolation disconnection when edge dropping exceeds ~35%."
    )
    
    p_contrib_head = doc.add_paragraph()
    p_contrib_head.paragraph_format.space_after = Pt(4)
    r_ch = p_contrib_head.add_run("Key Methodological Innovations:")
    r_ch.bold = True
    r_ch.font.color.rgb = RGBColor(4, 120, 87)
    
    contribs = [
        ("Cellular Sheaf Coordination for Heterogeneous Stalks: ",
         "We develop the first cellular sheaf framework for 6-DoF aerial swarms. Disparate platform state spaces F_v = R^{d_v} (scouts: R^12, leaders: R^24, relays: R^8) are reconciled over mutual edge stalks F_e = R^6 through continuous, interference-dependent restriction maps ρ_{v⊴e}(t)."),
        ("Bochner Curvature Decomposition & Zero Percolation Threshold: ",
         "Using discrete Bochner--Weitzenböck decomposition L_F = L_F^{Bochner} + Ric_F^{Forman}, we derive the local Sheaf Curvature Vulnerability Index (SCVI) to detect impending bottleneck failure. We prove (Theorem 2) that sheaf consensus resilience degrades strictly linearly (SRI ≥ SRI_0(1 - c f_jam)), eliminating the catastrophic second-order percolation phase transition."),
        ("Information-Geometric Event-Triggered Communication (IG-ETC): ",
         "We devise an event-trigger on the Gaussian belief manifold P_+^6, transmitting updates if and only if the Fisher-Rao Riemannian distance exceeds an energy-annealed threshold, cutting inter-drone packet traffic by up to 79.7%."),
        ("Sheaf Heterogeneous Auction for Task Allocation (SHATA): ",
         "We formulate the SHATA auction algorithm, enabling distributed bundle construction and conflict resolution directly over sheaf cochains. We prove its conflict-free convergence in O(|V| M D_G) iterations with polynomial real-time computation."),
        ("Dual-Tier Benchmarking & ROS 2 Humble Safety Simplex: ",
         "We conduct extensive multi-core sweeps (N=10 to 200 UAVs, f_jam in [0, 0.8], attrition in [10%, 50%]), demonstrating >91.3% task completion under 60% jamming where CBBA and flat graph flocking collapse below 24%. Furthermore, we deploy a complete ROS 2 Humble node stack with hardware-isolated Run-Time Assurance (RTA) Safety Simplex monitors, verifying zero safety violations (N_viol = 0) with sub-1.2 ms override latency.")
    ]
    
    for title, desc in contribs:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.left_indent = Inches(0.25)
        p_c.paragraph_format.space_after = Pt(3)
        r_t = p_c.add_run("• " + title)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(15, 23, 42)
        p_c.add_run(desc)
        
    p_align = doc.add_paragraph()
    p_align.paragraph_format.space_before = Pt(4)
    p_align.paragraph_format.space_after = Pt(6)
    r_ah = p_align.add_run("Relevance to Swarm and Evolutionary Computation & Robotics and Autonomous Systems: ")
    r_ah.bold = True
    p_align.add_run(
        "This article intersects the central remits of both journals by uniting decentralized swarm intelligence and auction optimization with real-time ROS 2 robotics deployment. Our benchmarks directly cite and compare with recent articles in SWEVO (e.g., GPU-native parallel optimization 2606.26164, divergence-driven stabilization 2506.23734, routing sampling 2512.19321) and RAS (e.g., UAV formation control 2304.03057, vibration swarm flocking 2610.35582, exploration mapping 2407.07409, multi-robot task allocation 2209.10513)."
    )
    
    p_decl = doc.add_paragraph()
    p_decl.paragraph_format.space_after = Pt(6)
    r_dh = p_decl.add_run("Declarations of Interest and Data Availability:\n")
    r_dh.bold = True
    p_decl.add_run("1. Originality: The paper is original, has not been published previously, and is not under consideration elsewhere.\n")
    p_decl.add_run("2. Co-Author Approval: All authors have confirmed participation and approved the final manuscript.\n")
    p_decl.add_run("3. Competing Interests: The authors have no competing financial or commercial conflicts of interest.\n")
    p_decl.add_run("4. Code & Reproducibility: All algorithms, simulation scripts, and ROS 2 packages are fully open-source at: ")
    r_gh = p_decl.add_run("https://github.com/Vishal442005/AERO-Swarm")
    r_gh.bold = True
    r_gh.font.color.rgb = RGBColor(5, 150, 105)
    p_decl.add_run(" (Release v1.0.0).")
    
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(6)
    p_close.paragraph_format.space_after = Pt(16)
    p_close.add_run("Thank you for your consideration of our work.\n\n")
    r_sig = p_close.add_run("Warm regards,\n\n")
    r_sig.font.italic = True
    
    r_team = p_close.add_run("Autonomous Robotics Swarm Research Consortium\n")
    r_team.bold = True
    p_close.add_run("Division of Robotics and Autonomous Systems\nAutonomous Multi-Agent Robotics Laboratory\nEmail: research@autonomous-swarms.org")
    
    doc.save(output_path)
    print(f"Elsevier Cover Letter saved to {output_path}")

if __name__ == "__main__":
    p_ieee = "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_ieee_(T-Cyb)/COVER_LETTER_IEEE_TCYB.docx"
    p_elsevier = "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_elseiver_(SWEVO)_RAS/COVER_LETTER_ELSEVIER_SWEVO_RAS.docx"
    build_ieee_cover_letter(p_ieee)
    build_elsevier_cover_letter(p_elsevier)
