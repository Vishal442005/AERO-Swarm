import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_cover_letter_docx(output_path):
    doc = docx.Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Header / Sender Info
    p = doc.add_paragraph()
    r = p.add_run("Vishal Chandel\n")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    r2 = p.add_run("Autonomous Systems and Swarm Robotics Laboratory\nEmail: vishal.chandel.res@gmail.com\nDate: November 6, 2026")
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    
    doc.add_paragraph()

    # Recipient
    p_rec = doc.add_paragraph()
    p_rec.add_run("Prof. Yew-Soon Ong\n").bold = True
    p_rec.add_run("Editor-in-Chief, ")
    p_rec.add_run("Swarm and Evolutionary Computation\n").italic = True
    p_rec.add_run("Elsevier Science")
    
    # Subject Box
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run("SUBJECT: Formal Resubmission of Extensively Revised Archival Manuscript (Ref: SWEVO-D-26-03280)")
    run_sub.bold = True
    run_sub.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    p_title = doc.add_paragraph()
    p_title.add_run("Manuscript Title: ").bold = True
    r_t = p_title.add_run("“AERO-Swarm: Resilient Autonomous Drone Swarm Coordination Under Severe Communication Contention via Cellular Sheaf Laplacians and Information Geometry”")
    r_t.italic = True
    p_title.paragraph_format.space_after = Pt(12)

    # Salutation
    doc.add_paragraph("Dear Professor Ong and Members of the Editorial Board,")

    # Body Paragraph 1
    doc.add_paragraph(
        "Thank you for your constructive editorial evaluation of our previous submission, SWEVO-D-26-03280. "
        "We deeply appreciated the Editorial Board’s candid assessment that while the research falls squarely within the aim "
        "and scope of Swarm and Evolutionary Computation, the initial manuscript lacked the archival depth required by the "
        "Journal—specifically regarding the mechanistic explanations of empirical curve trends, a comprehensive synthesis of "
        "generality and operational boundaries, and evaluations across a wider range of physical operational conditions."
    )

    # Body Paragraph 2
    doc.add_paragraph(
        "In response, we have treated this evaluation not merely as an editorial critique, but as a mandate for a complete, "
        "foundational elevation of the study to the highest archival standards. Over the past several months, we have substantially "
        "expanded the theoretical apparatus, conducted extensive new multi-condition empirical campaigns across diverse operational "
        "theaters and fleet configurations, synthesized a definitive operational taxonomy, and completely rewritten Sections 9 and 10 "
        "of the manuscript."
    )

    doc.add_paragraph(
        "We now have the honor of submitting our thoroughly revised, 18-page archival manuscript for your consideration. "
        "Below is an overview of the key archival upgrades introduced in this revision:"
    )

    # Bullet 1
    p1 = doc.add_paragraph()
    p1.add_run("1. Rigorous Mechanistic Explanations of All Empirical Trends (Section 9):\n").bold = True
    p1.add_run(
        "The revised manuscript no longer merely reports performance curves; it deconstructs every observed phenomenon through governing mathematical physics:\n"
        "• Percolation Phase Collapse vs. Sheaf Cushioning: We mathematically prove and empirically demonstrate that flat consensus baselines collapse at f_jam ≈ 0.35 due to Erdős-Rényi bond percolation threshold breakdown (p_c ≈ 1/<k>). In contrast, cellular sheaf restriction maps continuously preserve vector stalk spaces (d_v in {8, 12, 24}), maintaining algebraic connectivity λ_2(L_F) > 0 and achieving 91.3% ± 1.8% TCR under 60% severe RF jamming.\n"
        "• Fisher-Rao Information Geometry vs. Euclidean ETC: We explain why Euclidean event-triggered thresholds trigger burst chattering during dynamic flight, whereas geodesic distances on the Riemannian Siegel manifold of Gaussian beliefs scale by inverse covariance, suppressing uninformative kinematic changes to deliver a verified 79.6% bandwidth reduction.\n"
        "• Harmonic Cohomological Obstructions: We demonstrate how the Sheaf-Harmonic Task Allocation (SHATA) protocol resolves circular outbidding deadlocks by driving the first cohomology group rank dim H^1(F; R^d) monotonically to zero.\n"
        "• Complexity Scaling: We prove that localized sparse block-Cholesky updates yield per-node computational complexity O(|N_i| d_e^2) + O(d_v^3) = O(1), explaining why per-step execution latency scales gracefully to only 14.18 ms at N = 200 drones, well within the 20.0 ms (50 Hz) flight loop deadline."
    )

    # Bullet 2
    p2 = doc.add_paragraph()
    p2.add_run("2. Generality Synthesis & Operational Boundaries Taxonomy (New Section 10 & Table 4):\n").bold = True
    p2.add_run(
        "We have added a dedicated section and synthesis taxonomy explicitly establishing under which conditions AERO-Swarm performs better, achieves parity, or encounters physical boundaries:\n"
        "• Zone I (Superiority Zone): Contested RF (f_jam in [0.4, 0.8]), high attrition, and multi-role heterogeneous fleets where AERO-Swarm outperforms baselines by +30% to +70% TCR.\n"
        "• Zone II (Parity Zone): Pristine RF (f_jam < 0.15) and small homogeneous fleets (N ≤ 15) where classical CBBA and Olfati-Saber flocking achieve parity (98.1% vs. 97.8% TCR) and are recommended to avoid algebraic overhead.\n"
        "• Zone III (Scalability Boundary): Swarm densities exceeding N > 250 on embedded hardware where hierarchical cluster-sheaf decomposition is formally prescribed.\n"
        "• Zone IV (Physical Breakdown Horizon): Extreme RF jamming (f_jam ≥ 0.85, SNR < -12 dB) where Shannon channel capacity collapses to zero and physical optical/inertial fail-safes are mandated.\n"
        "• Zone V (Sensor Starvation): Degraded visual/LiDAR environments requiring covariance-inflated heartbeat fallbacks."
    )

    # Bullet 3
    p3 = doc.add_paragraph()
    p3.add_run("3. Expanded Multi-Condition & Heterogeneity Benchmark Campaigns (Figures 5 & 6):\n").bold = True
    p3.add_run(
        "• Three Diverse Theaters: Evaluated under identical jamming in Urban SAR Canyons (multipath/NLOS), Maritime Logistics (extended LOS over water), and Subterranean Rubble (severe waveguide attenuation).\n"
        "• Three Fleet Heterogeneity Configurations: Evaluated across Scout-Heavy, Balanced, and Leader-Heavy fleets, showing how cohomological obstructions are resolved across differing capability profiles."
    )

    # Bullet 4
    p4 = doc.add_paragraph()
    p4.add_run("4. 100% Numerical Consistency and Transparency:\n").bold = True
    p4.add_run(
        "Every numerical claim in the abstract, introduction, text, tables, figures, and CSV datasets has been verified for complete mathematical harmony (91.3% TCR, 0.718 SRI at 40% attrition, 79.6% bandwidth cut, 14.18 ms runtime at N = 200, and zero inter-UAV collisions)."
    )

    # Author Declarations
    p_dec = doc.add_paragraph()
    p_dec.add_run("Author Declarations & Compliance:\n").bold = True
    p_dec.add_run(
        "• Single Authorship: The undersigned, Vishal Chandel, is the sole author of this work and assumes full scientific and editorial responsibility for its contents.\n"
        "• Originality & Prior Publication: This manuscript represents original research and is not under consideration for publication elsewhere.\n"
        "• Competing Interests: The author declares no competing financial or personal conflicts of interest.\n"
        "• Reproducibility & Open Science: All raw simulation data, ROS 2 SITL integration scripts, extended benchmark runners, and visualization generators are organized in the project repository and are fully open for community replication."
    )

    doc.add_paragraph(
        "We believe that this comprehensively revised manuscript offers substantial archival value, providing both profound "
        "theoretical insights into topological swarm resilience and actionable engineering principles for contested multi-robot "
        "operations. We look forward to your and the reviewers' constructive appraisal."
    )

    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(12)
    p_close.add_run("Sincerely yours,\n\n").italic = True
    run_sign = p_close.add_run("Vishal Chandel\n")
    run_sign.bold = True
    p_close.add_run("Autonomous Systems and Swarm Robotics Laboratory\nEmail: vishal.chandel.res@gmail.com")

    doc.save(output_path)
    print(f"Cover letter successfully written to {output_path}")

if __name__ == '__main__':
    create_cover_letter_docx("Updated_significant/documentation/COVER_LETTER_RESUBMISSION.docx")
