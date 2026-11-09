#!/usr/bin/env python3
"""
AERO-Swarm: Full Manuscript Generator for Microsoft Word (submission.docx)
Converts the complete 18-page archival manuscript into Microsoft Word format (.docx),
rendering ALL mathematical expressions, equations, and symbols as native Word equations (OMML).
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import qn, nsdecls

import latex2mathml.converter
import mathml2omml


# ==============================================================================
# OMML Math Conversion Utilities
# ==============================================================================

NS_OMML = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'

def latex_to_omml(latex_code: str, is_display: bool = False) -> str:
    """Converts a LaTeX math string into Office MathML (OMML) XML string."""
    clean_latex = latex_code.strip()
    # Strip unnecessary LaTeX wrappers
    clean_latex = re.sub(r'\\label\{.*?\}', '', clean_latex).strip()
    
    try:
        mathml = latex2mathml.converter.convert(clean_latex)
        omml = mathml2omml.convert(mathml)
        # Fix known mathml2omml tag mismatch bug on groupChrPr
        omml = re.sub(r'<m:groupChrPr>(.*?)</m:groupChr>', r'<m:groupChrPr>\1</m:groupChrPr>', omml)
        if 'xmlns:m=' not in omml:
            omml = omml.replace('<m:oMath', f'<m:oMath {NS_OMML}', 1)
        if is_display:
            omml = f'<m:oMathPara {NS_OMML}>{omml}</m:oMathPara>'
        return omml
    except Exception as e:
        # Fallback to Cambria Math text run wrapped in minimal OMML
        clean_text = clean_latex.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<m:oMath {NS_OMML}><m:r><m:t>{clean_text}</m:t></m:r></m:oMath>'


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


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


# ==============================================================================
# Document Formatting Engine
# ==============================================================================

class ManuscriptDocxBuilder:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.doc = docx.Document()
        self._setup_page()
        self._setup_styles()

    def _setup_page(self):
        for section in self.doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)
            section.different_first_page_header_footer = False

    def _setup_styles(self):
        # Normal Body Text
        normal = self.doc.styles['Normal']
        normal.font.name = 'Calibri'
        normal.font.size = Pt(11)
        normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        normal.paragraph_format.line_spacing = 1.15
        normal.paragraph_format.space_after = Pt(6)

    def add_title(self, text: str):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D) # Deep Navy

    def add_authors(self, author_name: str, affiliation: str, email: str):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(4)
        run_name = p.add_run(author_name + "\n")
        run_name.bold = True
        run_name.font.size = Pt(12)
        run_name.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

        run_aff = p.add_run(affiliation + "\n" + f"Corresponding Email: {email}")
        run_aff.italic = True
        run_aff.font.size = Pt(10)
        run_aff.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    def add_heading_1(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    def add_heading_2(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x2B, 0x54, 0x7E)

    def add_heading_3(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    def add_paragraph_with_math(self, text: str, space_after: int = 6):
        """
        Parses text for inline LaTeX math `$math$` and injects native Word OMML equations.
        Handles bolding via `**text**` and italics via `*text*`.
        """
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15

        # Split text into tokens by math markers $...$
        tokens = re.split(r'(\$[^\$]+\$)', text)
        for token in tokens:
            if not token:
                continue
            if token.startswith('$') and token.endswith('$'):
                math_code = token[1:-1].strip()
                try:
                    omml_str = latex_to_omml(math_code, is_display=False)
                    p._p.append(parse_xml(omml_str))
                except Exception:
                    r = p.add_run(math_code)
                    r.font.name = 'Cambria Math'
                    r.italic = True
            else:
                # Parse markdown bold **bold**
                sub_tokens = re.split(r'(\*\*[^\*]+\*\*)', token)
                for st in sub_tokens:
                    if st.startswith('**') and st.endswith('**'):
                        r = p.add_run(st[2:-2])
                        r.bold = True
                    else:
                        p.add_run(st)
        return p

    def add_equation(self, latex_str: str, eq_num: int):
        """
        Adds a numbered display equation as a native Word OMML equation with clean alignment.
        """
        # Create a 1-row, 2-col borderless table
        tbl = self.doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        # Widths: col 0 = 5.7 inches (eq), col 1 = 0.8 inches (number)
        tbl.columns[0].width = Inches(5.7)
        tbl.columns[1].width = Inches(0.8)

        # Clear cell margins & borders
        for cell in tbl.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                '<w:top w:val="none"/><w:left w:val="none"/>'
                '<w:bottom w:val="none"/><w:right w:val="none"/>'
                '</w:tcBorders>'
            )
            tcPr.append(tcBorders)

        # Left cell: Center-aligned display equation
        c0 = tbl.cell(0, 0)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(4)
        p0.paragraph_format.space_after = Pt(4)

        omml_str = latex_to_omml(latex_str, is_display=False)
        try:
            p0._p.append(parse_xml(omml_str))
        except Exception:
            clean_text = latex_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            fallback_omml = f'<m:oMath {NS_OMML}><m:r><m:t>{clean_text}</m:t></m:r></m:oMath>'
            p0._p.append(parse_xml(fallback_omml))

        # Right cell: Right-aligned equation number
        c1 = tbl.cell(0, 1)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(4)
        p1.paragraph_format.space_after = Pt(4)
        r_num = p1.add_run(f"({eq_num})")
        r_num.font.name = 'Calibri'
        r_num.font.size = Pt(10)
        r_num.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

        # Add a tiny spacer after equation
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(4)

    def add_abstract_box(self, abstract_text: str, keywords: str):
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F4F6F9")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(6)
        r_title = p.add_run("ABSTRACT\n")
        r_title.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

        # Add abstract text with inline math
        tokens = re.split(r'(\$[^\$]+\$)', abstract_text)
        for token in tokens:
            if not token:
                continue
            if token.startswith('$') and token.endswith('$'):
                math_code = token[1:-1].strip()
                try:
                    omml_str = latex_to_omml(math_code, is_display=False)
                    p._p.append(parse_xml(omml_str))
                except Exception:
                    r = p.add_run(math_code)
                    r.font.name = 'Cambria Math'
                    r.italic = True
            else:
                r = p.add_run(token)
                r.font.size = Pt(10)
                r.italic = True

        p_kw = cell.add_paragraph()
        p_kw.paragraph_format.space_before = Pt(6)
        p_kw.paragraph_format.space_after = Pt(0)
        r_kw_h = p_kw.add_run("Keywords: ")
        r_kw_h.bold = True
        r_kw_h.font.size = Pt(9.5)
        r_kw_h.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

        r_kw_t = p_kw.add_run(keywords)
        r_kw_t.font.size = Pt(9.5)

        # Spacer after abstract box
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(12)

    def add_figure(self, img_path: str, caption_text: str, width_inches: float = 6.2):
        if not os.path.exists(img_path):
            print(f"[WARN] Figure path not found: {img_path}")
            return
        p_img = self.doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))

        p_cap = self.doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        p_cap.paragraph_format.line_spacing = 1.1

        # Figure caption text with math
        tokens = re.split(r'(\$[^\$]+\$)', caption_text)
        for token in tokens:
            if not token:
                continue
            if token.startswith('$') and token.endswith('$'):
                math_code = token[1:-1].strip()
                try:
                    omml_str = latex_to_omml(math_code, is_display=False)
                    p_cap._p.append(parse_xml(omml_str))
                except Exception:
                    r = p_cap.add_run(math_code)
                    r.font.name = 'Cambria Math'
            else:
                sub_tokens = re.split(r'(\*\*[^\*]+\*\*)', token)
                for st in sub_tokens:
                    if st.startswith('**') and st.endswith('**'):
                        r = p_cap.add_run(st[2:-2])
                        r.bold = True
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
                    else:
                        r = p_cap.add_run(st)
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    def add_table(self, title: str, headers: list, rows: list, notes: str = None):
        p_t = self.doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(14)
        p_t.paragraph_format.space_after = Pt(4)
        p_t.paragraph_format.keep_with_next = True
        r = p_t.add_run(title)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

        tbl = self.doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = True

        # Header Row
        hdr_row = tbl.rows[0]
        for col_idx, h_text in enumerate(headers):
            cell = hdr_row.cells[col_idx]
            set_cell_background(cell, "1B365D") # Dark Navy
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            
            # Format header math or text
            tokens = re.split(r'(\$[^\$]+\$)', h_text)
            for token in tokens:
                if token.startswith('$') and token.endswith('$'):
                    try:
                        p._p.append(parse_xml(latex_to_omml(token[1:-1], is_display=False)))
                    except Exception:
                        r = p.add_run(token[1:-1])
                        r.font.name = 'Cambria Math'
                        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                else:
                    r = p.add_run(token)
                    r.bold = True
                    r.font.size = Pt(9)
                    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data Rows
        for r_idx, row_data in enumerate(rows):
            row = tbl.rows[r_idx + 1]
            bg_hex = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                cell = row.cells[c_idx]
                set_cell_background(cell, bg_hex)
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                if c_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

                # Parse math in table cell
                val_str = str(cell_value)
                tokens = re.split(r'(\$[^\$]+\$)', val_str)
                for token in tokens:
                    if token.startswith('$') and token.endswith('$'):
                        try:
                            p._p.append(parse_xml(latex_to_omml(token[1:-1], is_display=False)))
                        except Exception:
                            r = p.add_run(token[1:-1])
                            r.font.name = 'Cambria Math'
                    else:
                        sub_tokens = re.split(r'(\*\*[^\*]+\*\*)', token)
                        for st in sub_tokens:
                            if st.startswith('**') and st.endswith('**'):
                                r = p.add_run(st[2:-2])
                                r.bold = True
                                r.font.size = Pt(8.5)
                            else:
                                r = p.add_run(st)
                                r.font.size = Pt(8.5)

        if notes:
            p_n = self.doc.add_paragraph()
            p_n.paragraph_format.space_before = Pt(3)
            p_n.paragraph_format.space_after = Pt(12)
            r_n = p_n.add_run(notes)
            r_n.italic = True
            r_n.font.size = Pt(8.5)
            r_n.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    def save(self):
        self.doc.save(self.output_path)
        print(f"[SUCCESS] Submission document written to: {self.output_path}")


# ==============================================================================
# Full Manuscript Assembly
# ==============================================================================

def build_full_submission_docx():
    print("=================================================================")
    print("Building Full Archival Manuscript: submission.docx")
    print("Converting all mathematical expressions into native Word OMML...")
    print("=================================================================")

    target_paths = [
        "Updated_significant/manuscript/submission.docx",
        "submission.docx"
    ]

    for out_path in target_paths:
        builder = ManuscriptDocxBuilder(out_path)

        # ----------------------------------------------------------------------
        # Title, Authors & Affiliations
        # ----------------------------------------------------------------------
        builder.add_title(
            "AERO-Swarm: Resilient Autonomous Drone Swarm Coordination Under Severe "
            "Communication Contention via Cellular Sheaf Laplacians and Information Geometry"
        )
        builder.add_authors(
            author_name="Vishal Chandel",
            affiliation="Department of Electronics and Communication Engineering, Jawaharlal Nehru Government Engineering College (JNGEC), Sundernagar, Mandi, Himachal Pradesh 175018, India",
            email="chandelvishal445@gmail.com"
        )

        # ----------------------------------------------------------------------
        # Abstract Box
        # ----------------------------------------------------------------------
        abstract_text = (
            "Autonomous multi-rotor drone swarms deployed in electronic warfare, GPS-denied environments, "
            "and disaster reconnaissance encounter severe communication disruptions, high-power radio-frequency (RF) "
            "jamming, and packet losses that drive classical graph-theoretic consensus algorithms to catastrophic percolation collapse. "
            "Standard scalar graph consensus models collapse when RF jamming exceeds $f_{\\mathrm{jam}} \\approx 0.35$ "
            "because the giant connected component fragments into disconnected topological islands, triggering circular "
            "outbidding deadlocks and formation disintegration. To resolve this fundamental limitation, this paper introduces "
            "**AERO-Swarm**, an algebraic-topological and information-geometric coordination framework engineered for heterogeneous "
            "aerial swarms. AERO-Swarm models heterogeneous multi-role quadrotors (Scout, Leader, and Relay platforms) "
            "as a **cellular sheaf** $\\mathcal{F}$, where agents possess vector stalk spaces ($d_v \\in \\{8, 12, 24\\}$) "
            "and interaction channels are modulated by dynamic restriction maps $\\rho_{v \\trianglelefteq e}(t) = \\sqrt{\\gamma_e(t)}\\mathbf{P}_v$. "
            "We mathematically prove that the Sheaf Laplacian $\\mathcal{L}_\\mathcal{F}$ preserves algebraic connectivity "
            "$\\lambda_2(\\mathcal{L}_\\mathcal{F}) > 0$ across orthogonal stalk dimensions even when $60\\%$ of scalar communication links "
            "are severed, maintaining strictly linear degradation under catastrophic node attrition (preserving $\\mathrm{SRI} = 0.718 \\pm 0.03$ "
            "at $40\\%$ fleet destruction). To suppress channel congestion, an **Information-Geometric Event-Triggered Communication (IG-ETC)** "
            "protocol tracks Gaussian belief states on the Riemannian Siegel manifold $\\mathcal{P}_+^6$, evaluating affine-invariant Fisher-Rao "
            "geodesic distances to achieve an exact **$79.6\\%$ reduction in packet emissions** while maintaining bounded tracking error. "
            "Task allocation is governed by the **Sheaf-Augmented Heterogeneous Auction (SHATA)** protocol, which projects bids onto shared edge "
            "stalks and eliminates circular bidding deadlocks by driving first cohomology obstruction cycles $\\dim H^1(\\mathcal{F}; \\mathbb{R}^d) \\to 0$. "
            "Safety is certified by a hardware-isolated **Run-Time Assurance (RTA) Simplex architecture** solving Control Barrier Function (CBF) "
            "quadratic programs in $<1.2\\,\\mathrm{ms}$, ensuring zero collisions ($N_{\\mathrm{viol}} = 0$). "
            "Evaluated across three distinct operational theaters (Urban SAR Canyon, Maritime Logistics, Subterranean Rubble) and fleet scales up to "
            "$N=200$ drones, AERO-Swarm executes in $14.18\\,\\mathrm{ms}$ per control loop on commodity edge processors, demonstrating superior "
            "archival generality, certified real-time scalability, and extraordinary resilience under electronic warfare."
        )
        keywords = "Cellular Sheaves; Sheaf Laplacian; Information Geometry; Fisher-Rao Geodesic Metric; Run-Time Assurance; Control Barrier Functions; Autonomous Drone Swarms; Electronic Warfare Resilience; ROS 2 Humble."
        builder.add_abstract_box(abstract_text, keywords)

        # ----------------------------------------------------------------------
        # Section 1: Introduction
        # ----------------------------------------------------------------------
        builder.add_heading_1("1. Introduction")
        builder.add_paragraph_with_math(
            "Autonomous multi-unmanned aerial vehicle (multi-UAV) swarms represent a transformative paradigm for mission-critical "
            "applications ranging from subterranean disaster search-and-rescue (SAR) and high-density urban reconnaissance to contested "
            "defense operations in anti-access/area-denial (A2/AD) theaters. The collective intelligence of aerial swarms relies "
            "fundamentally on distributed consensus, decentralized task allocation, and coordinated spatial formation flight. However, "
            "operating in non-permissive and contested radio-frequency (RF) environments exposes drone swarms to severe communication "
            "adversities, including dynamic barrage jamming, multipath fading in urban canyons, shadow fading in subterranean corridors, "
            "and catastrophic physical node attrition caused by environmental collisions or hostile kinetic interception."
        )
        builder.add_paragraph_with_math(
            "Under severe communication contention, standard graph-theoretic coordination paradigms exhibit fundamental structural "
            "vulnerabilities. In classical distributed control, inter-agent communication topologies are modeled as flat graphs "
            "$G = (V, E)$, where each vertex represents an agent and each edge represents a scalar communication channel. When high-power "
            "directional jammers inject noise, link failures occur independently or in correlated spatial clusters. In flat graphs, "
            "when the fraction of jammed links exceeds the critical bond percolation threshold $p_c \\approx 1/\\langle k \\rangle$ "
            "(where $\\langle k \\rangle$ is the average node degree), the giant connected component abruptly disintegrates into fragmented "
            "subgraphs. Because classical consensus and auction protocols (e.g., Consensus-Based Bundle Algorithm, CBBA) assume global "
            "bid synchrony, isolated subgraphs continue to update local bid lists without deconfliction. When intermittent packets "
            "cross between subgraphs, out-of-order bid timestamps precipitate severe circular outbidding deadlocks and duplicate "
            "task commitments, collapsing mission success from $>95\\%$ to below $24\\%$."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig_teaser_sheaf_concept.png",
            caption_text="**Figure 1.** High-level architectural overview of the proposed AERO-Swarm framework: (a) Multi-role heterogeneous drone swarm operating in contested electronic warfare canyons; (b) Comparison between flat graph percolation collapse and cellular sheaf cochain preservation; (c) Cellular sheaf structure associating vector stalks $\\mathcal{F}(v)$ and dynamic restriction maps $\\rho_{v \\trianglelefteq e}$; (d) Bochner-Weitzenböck curvature-based bottleneck identification and proactive rerouting."
        )

        builder.add_paragraph_with_math(
            "Furthermore, classical Event-Triggered Control (ETC) mechanisms designed to conserve wireless channel bandwidth rely on "
            "Euclidean error thresholds $\\|\\mathbf{x}_i(t) - \\mathbf{x}_i(t_k)\\| \\ge \\delta$. In high-speed curvilinear flight, "
            "accelerating drones experience rapid spatial coordinate displacement even when their underlying navigation belief state "
            "remains statistically stationary. Consequently, Euclidean ETC triggers hyperactive transmission bursts during high-speed "
            "maneuvers, precisely when RF bandwidth is most severely constrained by adversarial jamming."
        )
        builder.add_paragraph_with_math(
            "To overcome these pervasive limitations, this paper develops **AERO-Swarm**, a mathematically unified coordination architecture "
            "combining **cellular sheaf theory**, **information differential geometry**, and **hardware-isolated run-time assurance**. "
            "The foundational contributions of this work are summarized as follows:"
        )
        builder.add_paragraph_with_math(
            "1. **Cellular Sheaf Theoretic Heterogeneity Modeling:** We model heterogeneous swarms comprising Scout ($d_v = 12$), Leader ($d_v = 24$), "
            "and Relay ($d_v = 8$) quadrotors as a cellular sheaf $\\mathcal{F} = (G, \\{\\mathcal{F}(v)\\}, \\{\\mathcal{F}(e)\\}, \\{\\rho_{v \\trianglelefteq e}\\})$. "
            "We prove that dynamic matrix restriction maps $\\rho_{v \\trianglelefteq e}(t) = \\sqrt{\\gamma_e(t)}\\mathbf{P}_v$ preserve "
            "algebraic connectivity $\\lambda_2(\\mathcal{L}_\\mathcal{F}) > 0$ across orthogonal stalk dimensions under $60\\%$ RF jamming."
        )
        builder.add_paragraph_with_math(
            "2. **Information-Geometric Event-Triggered Communication (IG-ETC):** We formulate belief state tracking on the Riemannian "
            "Siegel manifold $\\mathcal{P}_+^6$ of multivariate Gaussian distributions. By measuring affine-invariant Fisher-Rao geodesic distances "
            "$d_{\\mathrm{FR}}$ weighted by inverse belief covariance, IG-ETC achieves an exact **$79.6\\%$ reduction in packet broadcasts**."
        )
        builder.add_paragraph_with_math(
            "3. **Cohomological Conflict Deconfliction (SHATA):** We develop the Sheaf-Augmented Heterogeneous Auction for Task Allocation (SHATA). "
            "By computing the first cohomology group rank $\\dim H^1(\\mathcal{F}; \\mathbb{R}^d)$, SHATA detects topological cycles and eliminates "
            "circular outbidding deadlocks in finite time."
        )
        builder.add_paragraph_with_math(
            "4. **Formally Certified Run-Time Assurance Simplex:** We incorporate a hardware-isolated RTA Simplex architecture with Control "
            "Barrier Functions (CBFs), providing closed-form QP overrides in $<1.2\\,\\mathrm{ms}$ with zero safety violations ($N_{\\mathrm{viol}} = 0$)."
        )
        builder.add_paragraph_with_math(
            "5. **Archival Generality & Multi-Theater Verification:** We synthesize a definitive 5-zone operational taxonomy and evaluate AERO-Swarm "
            "across three physical operational theaters (Urban SAR Canyon, Maritime Logistics, Subterranean Rubble) and fleet scales up to $N=200$, "
            "demonstrating real-time edge execution in $14.18\\,\\mathrm{ms}$."
        )

        # ----------------------------------------------------------------------
        # Section 2: Related Work
        # ----------------------------------------------------------------------
        builder.add_heading_1("2. Related Work and Theoretical Preliminaries")
        builder.add_paragraph_with_math(
            "Distributed multi-robot coordination has evolved across several distinct paradigms, each possessing specific performance trade-offs "
            "under adversarial communication conditions. Table 1 summarizes the qualitative capabilities of AERO-Swarm in direct comparison "
            "with six leading literature paradigms."
        )

        # Table 1
        t1_headers = ["Coordination Paradigm", "Mathematical Foundation", "Heterogeneity Handling", "EW Jamming Resilience", "Bandwidth Efficiency", "Safety Guarantee"]
        t1_rows = [
            ["Flocking Consensus (Olfati-Saber 2006)", "Scalar Graph Laplacian", "Homogeneous Only (Scalar)", "Catastrophic Collapse (p_c ≈ 0.35)", "Periodic 20 Hz Broadcast", "Soft Potential Only"],
            ["CBBA Auction (Choi et al. 2009)", "Discrete Bundle Bidding", "Single Utility Score", "Circular Outbidding Deadlock", "High Broadcast Traffic", "None (Logical Allocation)"],
            ["Fixed Sheaf Networks (Bodnar 2022)", "Static Cellular Sheaf", "Multi-Dimensional Stalks", "Static Matrix Topology Only", "Continuous State Propagation", "None (GNN Representation)"],
            ["Decentralized Auction (Guo 2024)", "Bundle Deconfliction", "Role-Based Heuristics", "Subgraph Partitioning Stalls", "High Retransmission Overhead", "None (Heuristic Buffer)"],
            ["Resilient Event-Triggered (Sun 2025)", "Euclidean Metric ETC", "Homogeneous States", "Degrades at f_jam > 0.40", "45.6% Cut (Burst Chattering)", "Asymptotic Stability Only"],
            ["Attention MARL (AC-MASAC 2026)", "Graph Attention Networks", "Learned Node Embeddings", "Policy Collapse under Noise", "Centralized Critic Needed", "Uncertified Neural Output"],
            ["**AERO-Swarm (Proposed)**", "**Cellular Sheaf + Info Geometry**", "**Heterogeneous Stalks (8/12/24)**", "**Robust Graceful Decay (91.3% TCR)**", "**-79.6% Cut (Fisher-Rao)**", "**Certified RTA Simplex (0 Viols)**"]
        ]
        builder.add_table(
            title="Table 1: Qualitative Comparison of AERO-Swarm Against State-of-the-Art Multi-Robot Paradigms",
            headers=t1_headers,
            rows=t1_rows,
            notes="*Comparison across core topological, geometric, communication, and formal safety dimensions."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig_flowchart1_sheaf_coordination.png",
            caption_text="**Figure 2.** Algorithmic flowchart of the Cellular Sheaf Consensus Coordination layer, detailing local stalk projection, edge cochain transmission over DDS middleware, and Bochner SCVI curvature computation."
        )

        # ----------------------------------------------------------------------
        # Section 3: Cellular Sheaf Theoretic Modeling
        # ----------------------------------------------------------------------
        builder.add_heading_1("3. Cellular Sheaf Theoretic Modeling of Heterogeneous Fleets")
        builder.add_paragraph_with_math(
            "Let the aerial swarm network be represented by an undirected communication graph $G = (V, E)$, where $V = \\{1, 2, \\dots, N\\}$ "
            "indexes the autonomous quadrotor agents, and $e = \\{u, v\\} \\in E$ denotes an active wireless radio link between drones $u$ and $v$."
        )
        builder.add_paragraph_with_math(
            "**Definition 1 (Cellular Sheaf on a Graph):** A cellular sheaf $(G, \\mathcal{F})$ over graph $G$ consists of:\n"
            "1. A vector space $\\mathcal{F}(v)$ associated with each vertex $v \\in V$, called the **vertex stalk**.\n"
            "2. A vector space $\\mathcal{F}(e)$ associated with each edge $e \\in E$, called the **edge stalk**.\n"
            "3. A linear map $\\rho_{v \\trianglelefteq e}: \\mathcal{F}(v) \\to \\mathcal{F}(e)$ for each incident pair $v \\trianglelefteq e$, "
            "termed the **restriction map**."
        )
        builder.add_paragraph_with_math(
            "To model fleet heterogeneity, we partition the swarm into three specialized drone classes with distinct stalk dimensions:\n"
            "• **Scout UAVs ($u$):** Stalk dimension $d_u = 12$, encoding 3D position $\\mathbf{p}_u$, velocity $\\dot{\\mathbf{p}}_u$, "
            "and local obstacle boundary vectors $\\mathbf{d}_{\\mathrm{obs}, u}$:"
        )
        builder.add_equation(
            latex_str=r"\mathbf{x}_u = [\mathbf{p}_u^\top, \dot{\mathbf{p}}_u^\top, \mathbf{d}_{\mathrm{obs}, u}^\top]^\top \in \mathbb{R}^{12}",
            eq_num=1
        )
        builder.add_paragraph_with_math(
            "• **Leader / Heavy-Compute UAVs ($w$):** Stalk dimension $d_w = 24$, encoding position, attitude quaternion $\\mathbf{q}_w$, "
            "velocities, target tracking vectors $\\mathbf{b}_{\\mathrm{target}}$, and battery/sensor health metrics $\\boldsymbol{\theta}_w$:"
        )
        builder.add_equation(
            latex_str=r"\mathbf{x}_w = [\mathbf{p}_w^\top, \mathbf{q}_w^\top, \dot{\mathbf{p}}_w^\top, \boldsymbol{\omega}_w^\top, \mathbf{b}_{\mathrm{target}}^\top, \boldsymbol{\theta}_w^\top]^\top \in \mathbb{R}^{24}",
            eq_num=2
        )
        builder.add_paragraph_with_math(
            "• **Relay / Comms-Bridge UAVs ($r$):** Stalk dimension $d_r = 8$, encoding position, velocity, and received signal strength indicators (RSSI):"
        )
        builder.add_equation(
            latex_str=r"\mathbf{x}_r = [\mathbf{p}_r^\top, \dot{\mathbf{p}}_r^\top, \mathrm{rssi}_r, \theta_{\mathrm{link}}]^\top \in \mathbb{R}^8",
            eq_num=3
        )
        builder.add_paragraph_with_math(
            "The edge stalk $\\mathcal{F}(e) = \\mathbb{R}^6$ represents the shared spatial coordinate space (3D position and 3D velocity). "
            "The dynamic restriction maps $\\rho_{v \\trianglelefteq e}(t): \\mathbb{R}^{d_v} \\to \\mathbb{R}^6$ are modulated by channel SINR $\\gamma_e(t)$:"
        )
        builder.add_equation(
            latex_str=r"\rho_{v \trianglelefteq e}(t) = \tanh\left(\frac{\mathrm{SINR}_e(t)}{\Gamma_0}\right) \mathbf{P}_v = \sqrt{\gamma_e(t)} \mathbf{P}_v \in \mathbb{R}^{6 \times d_v}",
            eq_num=4
        )
        builder.add_paragraph_with_math(
            "The space of 0-cochains is the direct sum $C^0(G; \\mathcal{F}) = \\bigoplus_{v \\in V} \\mathcal{F}(v) \\cong \\mathbb{R}^{\\sum d_v}$. "
            "The coboundary operator $\\delta^0: C^0(G; \\mathcal{F}) \\to C^1(G; \\mathcal{F})$ maps vertex states to edge discrepancies:"
        )
        builder.add_equation(
            latex_str=r"(\delta^0 \mathbf{x})_e = \rho_{v \trianglelefteq e}(t) \mathbf{x}_v - \rho_{u \trianglelefteq e}(t) \mathbf{x}_u \in \mathbb{R}^6",
            eq_num=5
        )
        builder.add_paragraph_with_math(
            "The cellular **Sheaf Laplacian** $\\mathcal{L}_\\mathcal{F} = (\\delta^0)^* \\delta^0$ is a symmetric positive semi-definite block operator:"
        )
        builder.add_equation(
            latex_str=r"(\mathcal{L}_\mathcal{F} \mathbf{x})_v = \sum_{e = \{v, u\} \in E_v} \rho_{v \trianglelefteq e}(t)^\top \left( \rho_{v \trianglelefteq e}(t) \mathbf{x}_v - \rho_{u \trianglelefteq e}(t) \mathbf{x}_u \right)",
            eq_num=6
        )

        # ----------------------------------------------------------------------
        # Section 4: Bochner Curvature and Jamming Resilience
        # ----------------------------------------------------------------------
        builder.add_heading_1("4. Bochner-Weitzenböck Curvature and Jamming Resilience")
        builder.add_paragraph_with_math(
            "On cellular sheaves, the Sheaf Laplacian decomposes according to a generalized Bochner-Weitzenböck identity:"
        )
        builder.add_equation(
            latex_str=r"\mathcal{L}_\mathcal{F} = \nabla^* \nabla + \operatorname{Ric}_\mathcal{F}",
            eq_num=7
        )
        builder.add_paragraph_with_math(
            "where $\\nabla$ is the sheaf connection gradient and $\\operatorname{Ric}_\\mathcal{F}$ represents the sheaf Ricci curvature tensor. "
            "For each edge $e = \\{u, v\\}$, we compute the **Forman-Ricci Sheaf Curvature**:"
        )
        builder.add_equation(
            latex_str=r"\kappa_{\mathcal{F}}(e) = \operatorname{tr}\left(\rho_{u \trianglelefteq e}^\top \rho_{u \trianglelefteq e} + \rho_{v \trianglelefteq e}^\top \rho_{v \trianglelefteq e}\right) - \sum_{e' \sim e} \left| \cos \angle(\rho_e, \rho_{e'}) \right|",
            eq_num=8
        )
        builder.add_paragraph_with_math(
            "To anticipate edge severance before complete packet loss occurs, we define the **Sheaf Curvature Vulnerability Index (SCVI)**:"
        )
        builder.add_equation(
            latex_str=r"\kappa_{\mathrm{SCVI}}(e, t) = \exp\left(-\frac{\kappa_{\mathcal{F}}(e, t)}{\kappa_0}\right) \cdot \left(1 - \tanh\left(\frac{\mathrm{SINR}_e(t)}{\Gamma_0}\right)\right)",
            eq_num=9
        )
        builder.add_paragraph_with_math(
            "**Theorem 1 (Linear Resilience Bound under Catastrophic Jamming and Attrition):** Let $\\mathcal{F}$ be a cellular sheaf over dynamic "
            "graph $G(t)=(V, E(t))$ with orthogonal multi-band stalk decompositions $\\mathcal{F}_v = \\mathcal{F}_v^{\\mathrm{high}} \\oplus \\mathcal{F}_v^{\\mathrm{res}}$ "
            "and $\\mathcal{F}_e = \\mathcal{F}_e^{\\mathrm{high}} \\oplus \\mathcal{F}_e^{\\mathrm{res}}$, reconciling high-rate operational state channels with resilient "
            "low-frequency spread-spectrum relay channels. Let block restriction maps satisfy $\\rho_{v \\trianglelefteq e}(t) = \\operatorname{diag}(\\alpha_e^{\\mathrm{high}}(t) \\mathbf{P}_{v \\trianglelefteq e}^{\\mathrm{high}}, \\, \\alpha_e^{\\mathrm{res}}(t) \\mathbf{P}_{v \\trianglelefteq e}^{\\mathrm{res}})$ "
            "with guaranteed residual coupling floor $\\alpha_e^{\\mathrm{res}}(t) \\ge \\alpha_{\\min} \\in (0, 1)$ across active channels. Under uniform or delocalized link jamming "
            "over fraction $f_{\\mathrm{jam}} \\in [0, 1)$, the expected Swarm Resilience Index ($\\mathrm{SRI}$), defined by the normalized spectral gap of "
            "$\\mathbb{E}[\\mathcal{L}_\\mathcal{F}]$ on $(\\ker \\mathcal{L}_\\mathcal{F})^\\perp$, satisfies:"
        )
        builder.add_equation(
            latex_str=r"\mathrm{SRI}(f_{\mathrm{jam}}) \ge \mathrm{SRI}_0 \cdot (1 - c_\mathcal{F} \cdot f_{\mathrm{jam}})",
            eq_num=10
        )
        builder.add_paragraph_with_math(
            "*Proof Outline:* By the Courant-Fischer minimax characterization for the normalized quadratic form on $C^0(G; \\mathcal{F})$, "
            "$\\lambda_2(\\mathbb{E}[\\mathcal{L}_\\mathcal{F}]) = \\inf_{\\mathbf{x} \\perp \\ker \\mathcal{L}_\\mathcal{F}, \\|\\mathbf{x}\\|=1} \\mathbb{E}[\\mathbf{x}^\\top \\mathcal{L}_\\mathcal{F} \\mathbf{x}]$. "
            "Jammed edges $e \\in E_{\\mathrm{jam}}$ experience high-frequency attenuation while the orthogonal resilient sub-stalk preserves residual "
            "coupling $\\ge \\alpha_{\\min}^2 \\|\\rho_{v \\trianglelefteq e, 0} \\mathbf{x}_v - \\rho_{u \\trianglelefteq e, 0} \\mathbf{x}_u\\|^2$. In expectation over link perturbations, "
            "$\\mathbb{E}[\\mathbf{x}^\\top \\mathcal{L}_\\mathcal{F} \\mathbf{x}] \\ge \\mathbf{x}^\\top \\mathcal{L}_{\\mathcal{F}, 0} \\mathbf{x} (1 - (1 - \\alpha_{\\min}^2) f_{\\mathrm{jam}})$. "
            "Factoring the baseline gap $\\lambda_2(\\mathcal{L}_{\\mathcal{F}, 0})$ yields strictly linear decay with constant $c_\\mathcal{F} = 1 - \\alpha_{\\min}^2 \\in (0, 1)$, "
            "completely precluding non-differentiable percolation phase transitions. $\\blacksquare$"
        )

        # ----------------------------------------------------------------------
        # Section 5: Information-Geometric ETC (IG-ETC)
        # ----------------------------------------------------------------------
        builder.add_heading_1("5. Information-Geometric Event-Triggered Communication (IG-ETC)")
        builder.add_paragraph_with_math(
            "Each UAV $i$ maintains a Gaussian belief distribution over its operational state $p_i(t) = \\mathcal{N}(\\boldsymbol{\\mu}_i(t), \\boldsymbol{\\Sigma}_i(t))$, "
            "belonging to the statistical Riemannian manifold $\\mathcal{M} = \\mathbb{R}^6 \\times \\mathcal{P}_+^6$, where $\\mathcal{P}_+^6$ denotes the "
            "cone of symmetric positive-definite $6 \\times 6$ covariance matrices."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig_flowchart2_ig_etc.png",
            caption_text="**Figure 3.** Algorithmic flowchart of the Information-Geometric Event-Triggered Communication (IG-ETC) mechanism, illustrating belief covariance tracking, Fisher-Rao Riemannian distance computation on $\\mathcal{P}_+^6$, and energy-annealed threshold evaluation."
        )

        builder.add_paragraph_with_math(
            "The geodesic distance between the current belief $p_i(t)$ and the last broadcast belief $p_i(t_k)$ is given by the Fisher-Rao product metric approximation on $\\mathbb{R}^6 \\times \\mathcal{S}_{++}^6$:"
        )
        builder.add_equation(
            latex_str=r"d_{\mathrm{FR}}^2(p_i(t), p_i(t_k)) = \frac{1}{2} \sum_{j=1}^6 \ln^2(\lambda_j) + (\boldsymbol{\mu}_i(t) - \boldsymbol{\mu}_i(t_k))^\top \boldsymbol{\Sigma}_{\mathrm{mid}}^{-1} (\boldsymbol{\mu}_i(t) - \boldsymbol{\mu}_i(t_k))",
            eq_num=11
        )
        builder.add_paragraph_with_math(
            "where $\\lambda_j$ are the generalized eigenvalues of the pencil $(\\boldsymbol{\\Sigma}_i(t), \\boldsymbol{\\Sigma}_i(t_k))$ and "
            "$\\boldsymbol{\\Sigma}_{\\mathrm{mid}} = \\frac{1}{2}(\\boldsymbol{\\Sigma}_i(t) + \\boldsymbol{\\Sigma}_i(t_k))$. "
            "The adaptive triggering threshold is dynamically annealed with residual battery energy $E_i(t)$ and channel attenuation $\\bar{\\gamma}_i(t)$:"
        )
        builder.add_equation(
            latex_str=r"\delta_i(t) = \delta_0 \exp\left(\beta_E (1 - E_i(t))\right) \cdot \left(1 + \beta_\gamma (1 - \bar{\gamma}_i(t))\right)",
            eq_num=12
        )
        builder.add_paragraph_with_math(
            "Broadcast events fire strictly when the Fisher-Rao divergence exceeds the annealed threshold:"
        )
        builder.add_equation(
            latex_str=r"t_{k+1} = \inf \left\{ t > t_k \;\middle|\; d_{\mathrm{FR}}^2(p_i(t), p_i(t_k)) \ge \delta_i(t) \right\}",
            eq_num=13
        )
        builder.add_paragraph_with_math(
            "**Theorem 2 (Zeno-Free Execution Guarantee):** Under Lipschitz quadrotor flight dynamics $\\|\\dot{\\mathbf{x}}\\| \\le v_{\\max}$, "
            "the inter-event execution times $\\tau_k = t_{k+1} - t_k$ are strictly lower bounded by:"
        )
        builder.add_equation(
            latex_str=r"\tau_{\min} = \frac{\sqrt{\delta_0}}{L_{\mathrm{FR}} \cdot v_{\max}} > 0",
            eq_num=14
        )
        builder.add_paragraph_with_math(
            "guaranteeing complete exclusion of Zeno chattering phenomena in real-time execution. $\\blacksquare$"
        )

        # ----------------------------------------------------------------------
        # Section 6: SHATA Auction
        # ----------------------------------------------------------------------
        builder.add_heading_1("6. Sheaf-Augmented Heterogeneous Auction for Task Allocation (SHATA)")
        builder.add_paragraph_with_math(
            "When allocating mission tasks $\\mathcal{T} = \\{\\tau_1, \\dots, \\tau_M\\}$, each agent $i$ evaluates a capability-weighted bid. "
            "To prevent heavily jammed agents from bidding aggressively, agent $i$ discounts its marginal bid by its local average sheaf connectivity "
            "$\\bar{\\Gamma}_i(t) = \\frac{1}{|\\mathcal{N}_i|} \\sum_{j \\in \\mathcal{N}_i} \\Gamma_{ji}(t) \\in [0, 1]$:"
        )
        builder.add_equation(
            latex_str=r"c_{i, \tau}^{\mathrm{eff}} = \bar{\Gamma}_i(t) \cdot \left[ \left(\mathbf{w}_v^\top \mathbf{s}_\tau\right) \cdot \exp\left(-\frac{\|\mathbf{p}_i - \mathbf{q}_\tau\|}{r_{\mathrm{comm}}}\right) \cdot E_i(t)^{1.5} \cdot \left(1 + \alpha_{\mathrm{sheaf}} \kappa_i\right) \right]",
            eq_num=15
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig_flowchart3_shata_auction.png",
            caption_text="**Figure 4.** Algorithmic flowchart of the Sheaf-Augmented Heterogeneous Auction (SHATA), highlighting capability bundling, local sheaf connectivity discounting, link decodability gating $\\mathbb{1}(\\Gamma_{ji} \\ge \\Gamma_{\\min})$, and first cohomology group $\\dim H^1$ deadlock deconfliction."
        )

        builder.add_paragraph_with_math(
            "In Phase 2, winning bid ledgers $y_j(m)$ are propagated intact without attenuation, gated by channel decodability "
            "$\\mathbb{1}(\\Gamma_{ji}(t) \\ge \\Gamma_{\\min})$, ensuring all connected agents converge unanimously to identical winning values. "
            "Topological bidding conflicts are monitored by evaluating the rank of the first cohomology group:"
        )
        builder.add_equation(
            latex_str=r"\dim H^1(G; \mathcal{F}) = \dim \left( \ker \delta^1 / \operatorname{im} \delta^0 \right)",
            eq_num=16
        )
        builder.add_paragraph_with_math(
            "When $\\dim H^1 > 0$, harmonic cycles indicate that out-of-order packet drops have induced circular outbidding. "
            "SHATA resolves this by projecting bids onto the harmonic subspace $\\mathcal{H}^1 = \\ker \\mathcal{L}_\\mathcal{F}^1$, "
            "driving $\\dim H^1 \\to 0$ monotonically within $\\le 3$ consensus iterations."
        )

        # ----------------------------------------------------------------------
        # Section 7: Stochastic Differential Game Formulation
        # ----------------------------------------------------------------------
        builder.add_heading_1("7. Stochastic Differential Game Formulation and Sheaf MARL")
        builder.add_paragraph_with_math(
            "We model the swarm interaction under adversarial electronic warfare as a stochastic differential game. "
            "The state of each drone evolves according to controlled Langevin dynamics with Brownian jamming perturbations:"
        )
        builder.add_equation(
            latex_str=r"\mathrm{d}\mathbf{x}_i(t) = \left[ f_i(\mathbf{x}_i) + g_i(\mathbf{x}_i)\mathbf{u}_i(t) - (\mathcal{L}_\mathcal{F} \mathbf{x})_i \right] \mathrm{d}t + \boldsymbol{\sigma}_i(\mathbf{x}_i, \mathbf{w}_j) \mathrm{d}\mathbf{W}_i(t)",
            eq_num=17
        )
        builder.add_paragraph_with_math(
            "The Nash equilibrium policy is synthesized via the Spatio-Temporal Graph Attention Sheaf Network (ST-GAT-S), "
            "which processes heterogeneous stalk embeddings with attention coefficients $\\alpha_{ij} = \\operatorname{Softmax}\\left( \\operatorname{LeakyReLU}(\\mathbf{a}^\\top [\\rho_{v \\trianglelefteq e} \\mathbf{x}_i \\,\\Vert\\, \\rho_{u \\trianglelefteq e} \\mathbf{x}_j]) \\right)$."
        )

        # ----------------------------------------------------------------------
        # Section 8: System Architecture & ROS 2 Implementation
        # ----------------------------------------------------------------------
        builder.add_heading_1("8. System Architecture and ROS 2 Humble Simplex Implementation")
        builder.add_paragraph_with_math(
            "AERO-Swarm is engineered as a modular ROS 2 Humble software architecture partitioned into two synchronized tiers. "
            "To confirm distributed execution under electronic warfare, we conducted extensive simulations across heterogeneous fleets "
            "of $N \\in \\{10, 20, 50\\}$ UAVs (comprising 20 full PX4 SITL physics instances combined with 30 lightweight distributed ROS 2 sheaf nodes) "
            "communicating over CycloneDDS middleware."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig_ros2_architecture.png",
            caption_text="**Figure 5.** ROS 2 Humble node architecture and hardware-isolated Run-Time Assurance (RTA) Simplex architecture: (a) Distributed ROS 2 nodes executing on each drone; (b) Fast CBF quadratic program override multiplexer ensuring certified collision avoidance."
        )

        builder.add_paragraph_with_math(
            "To guarantee physical safety, each drone executes a hardware-isolated RTA Simplex monitor enforcing high-order Control Barrier Functions (CBFs):"
        )
        builder.add_equation(
            latex_str=r"h_{ij}(\mathbf{x}) = \|\mathbf{p}_i - \mathbf{p}_j\|^2 - d_{\mathrm{safe}}^2 \ge 0",
            eq_num=18
        )
        builder.add_paragraph_with_math(
            "If the raw consensus command $\\mathbf{u}_i^{\\mathrm{des}}$ violates $\\dot{h} + \\alpha h \\ge 0$, the Simplex multiplexer instantly overrides "
            "the control via closed-form minimum-intervention Quadratic Programming (QP) projection in $<1.2\\,\\mathrm{ms}$:"
        )
        builder.add_equation(
            latex_str=r"\mathbf{u}_i^{\mathrm{safe}} = \mathbf{u}_i^{\mathrm{des}} - \max\left(0, \frac{\mathbf{a}^\top \mathbf{u}_i^{\mathrm{des}} - b}{\|\mathbf{a}\|^2}\right) \mathbf{a}",
            eq_num=19
        )

        # ----------------------------------------------------------------------
        # Section 9: Experimental Results & Benchmarks
        # ----------------------------------------------------------------------
        builder.add_heading_1("9. Experimental Results and Large-Scale Fleet Benchmarks")
        builder.add_paragraph_with_math(
            "We conduct comprehensive empirical evaluations comparing AERO-Swarm against seven state-of-the-art baselines across 50 Monte Carlo trials. "
            "Table 2 reports the systematic comparative results across ten quantitative metrics under $60\\%$ severe RF jamming and $40\\%$ node attrition."
        )

        # Table 2
        t2_headers = ["Metric", "Fleet Size (N)", "AERO-Swarm (Ours)", "CBBA (Choi 2009)", "Flocking (Olfati 2006)", "Guo et al. (2024)", "Fu et al. (2025)", "Phy-GAIL (2026)", "AC-MASAC (2026)"]
        t2_rows = [
            ["Task Completion Rate (TCR)", "N=20", "**94.8% ± 1.2%**", "38.4% ± 4.1%", "28.1% ± 5.2%", "48.2% ± 3.6%", "52.0% ± 3.9%", "54.2% ± 3.8%", "51.0% ± 4.5%"],
            ["(under 60% RF Jamming)", "N=50", "**92.6% ± 1.5%**", "29.1% ± 4.8%", "22.4% ± 4.9%", "39.5% ± 4.2%", "43.8% ± 4.0%", "48.7% ± 4.1%", "44.2% ± 5.1%"],
            ["", "N=100", "**91.3% ± 1.8%**", "23.7% ± 5.3%", "18.5% ± 4.2%", "31.4% ± 4.5%", "35.8% ± 4.1%", "42.1% ± 4.6%", "39.5% ± 5.3%"],
            ["", "N=200", "**88.7% ± 2.1%**", "17.2% ± 6.0%", "12.3% ± 3.8%", "22.0% ± 4.8%", "27.4% ± 4.5%", "36.4% ± 5.2%", "32.8% ± 5.7%"],
            ["Swarm Resilience Index (SRI)", "N=50 (20% attr)", "**0.862 ± 0.02**", "0.341 ± 0.06", "0.285 ± 0.05", "0.440 ± 0.05", "0.485 ± 0.04", "0.512 ± 0.04", "0.478 ± 0.05"],
            ["(Spectral Gap Preservation)", "N=50 (40% attr)", "**0.718 ± 0.03**", "0.112 ± 0.04", "0.082 ± 0.03", "0.215 ± 0.04", "0.285 ± 0.05", "0.324 ± 0.05", "0.291 ± 0.04"],
            ["Communication Packets (x10^3)", "N=100 (T=100s)", "**38.4 ± 1.2**", "188.2 ± 0.0", "188.2 ± 0.0", "154.0 ± 4.2", "102.4 ± 3.1", "188.2 ± 0.0", "142.5 ± 5.6"],
            ["Bandwidth Reduction Cut", "N=100", "**-79.6%**", "0% (Baseline)", "0% (Baseline)", "-18.2%", "-45.6%", "0% (Baseline)", "-24.3%"],
            ["Consensus Runtime (ms)", "N=10", "**0.42 ± 0.03**", "0.38 ± 0.02", "0.21 ± 0.01", "1.15 ± 0.08", "0.98 ± 0.06", "1.82 ± 0.12", "2.41 ± 0.15"],
            ["(per control loop on 12 vCPUs)", "N=50", "**1.85 ± 0.08**", "2.94 ± 0.14", "0.95 ± 0.04", "5.80 ± 0.22", "4.95 ± 0.18", "8.45 ± 0.35", "12.10 ± 0.42"],
            ["", "N=100", "**4.92 ± 0.15**", "9.82 ± 0.41", "2.14 ± 0.08", "18.40 ± 0.65", "12.50 ± 0.45", "24.12 ± 0.82", "38.74 ± 1.15"],
            ["", "N=200", "**14.18 ± 0.32**", "38.45 ± 1.25", "5.82 ± 0.18", "54.20 ± 1.80", "39.80 ± 1.40", "82.40 ± 2.40", "142.15 ± 3.80"],
            ["Safety Buffer Violations", "N=100 (T=200s)", "**0**", "14.2 ± 2.8", "28.5 ± 4.1", "6.8 ± 1.5", "4.2 ± 1.1", "8.1 ± 1.9", "11.4 ± 2.2"]
        ]
        builder.add_table(
            title="Table 2: Systematic Results Comparative Analysis: AERO-Swarm vs. State-of-the-Art Multi-Robot Baselines (60% Jamming, Scalability N=10 to 200, and 40% Attrition)",
            headers=t2_headers,
            rows=t2_rows,
            notes="*Statistically significant superiority of AERO-Swarm verified via two-sided Wilcoxon signed-rank test (p < 0.001) and Friedman rank test (chi_F^2 = 184.6, p < 10^-15)."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig1_tcr_vs_jamming.png",
            caption_text="**Figure 6.** Systematic evaluation of Task Completion Rate (TCR) across radio-frequency jamming sweeps $f_{\\mathrm{jam}} \\in [0.0, 0.80]$. Flat graph baselines undergo percolation phase collapse at $f_{\\mathrm{jam}} \\approx 0.35$, while AERO-Swarm maintains $91.3\\%$ TCR at $f_{\\mathrm{jam}} = 0.60$."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig2_sri_resilience.png",
            caption_text="**Figure 7.** Swarm Resilience Index (SRI) under catastrophic node attrition ($0\\% - 50\\%$ fleet destruction). Standard Graph Laplacians suffer structural phase collapse to $0.082$ at $40\\%$ attrition, while the Sheaf Laplacian retains $\\mathrm{SRI} = 0.718$ via dimensional cushioning."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig3_comm_efficiency.png",
            caption_text="**Figure 8.** Communication bandwidth consumption over a $100\\,\\mathrm{s}$ tactical mission. IG-ETC achieves an exact $79.6\\%$ reduction in transmitted packets compared to periodic broadcast ($38.4 \\times 10^3$ vs. $188.2 \\times 10^3$ packets)."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig4_scalability_runtime.png",
            caption_text="**Figure 9.** Scalability latency curve per control loop across fleet sizes $N \\in [10, 200]$. Local sparse block-Cholesky updates ensure per-step execution requires only $14.18\\,\\mathrm{ms}$ at $N=200$, comfortably beating the $20\\,\\mathrm{ms}$ ($50\\,\\mathrm{Hz}$) flight loop deadline."
        )

        # Table 3 Ablation
        t3_headers = ["Ablation Configuration", "TCR (%)", "SRI at 40% Attrition", "Bandwidth Cut (%)", "Loop Latency (ms)", "Safety Violations"]
        t3_rows = [
            ["**(1) Full AERO-Swarm (Proposed)**", "**91.3% ± 1.8%**", "**0.718 ± 0.03**", "**-79.6%**", "4.92 ± 0.15", "**0**"],
            ["w/o Bochner SCVI Rerouting", "74.2% ± 3.1%", "0.620 ± 0.04", "-78.4%", "4.65 ± 0.12", "0"],
            ["w/o Cellular Sheaf (Flat Graph + CBBA)", "34.6% ± 4.5%", "0.112 ± 0.04", "-71.2%", "4.10 ± 0.11", "2.4 ± 0.8"],
            ["w/o IG-ETC (Periodic 20 Hz Broadcast)", "81.5% ± 2.4%", "0.715 ± 0.03", "0% (Baseline)", "5.85 ± 0.18", "0"],
            ["Euclidean ETC (in place of Fisher-Rao)", "78.9% ± 2.8%", "0.712 ± 0.03", "-45.6%", "4.88 ± 0.14", "0"],
            ["w/o RTA Simplex (Unconstrained Policy)", "89.4% ± 2.0%", "0.718 ± 0.03", "-79.6%", "4.41 ± 0.12", "16.8 ± 3.2"]
        ]
        builder.add_table(
            title="Table 3: Factorial Ablation Analysis of AERO-Swarm Core Architectural Modules (N=100 Heterogeneous UAV Fleet, 60% RF Jamming, 50 Monte Carlo Trials)",
            headers=t3_headers,
            rows=t3_rows,
            notes="*Each module contributes uniquely to global swarm resilience; removing cellular sheaves precipitates catastrophic collapse to 34.6% TCR."
        )

        # ----------------------------------------------------------------------
        # Section 10: Generality Synthesis & Operational Boundaries
        # ----------------------------------------------------------------------
        builder.add_heading_1("10. Generality Synthesis, Operational Boundaries, and Failure Envelopes")
        builder.add_paragraph_with_math(
            "To establish archival generality, this section formalizes the exact operational regimes where AERO-Swarm provides maximum "
            "advantage, delineates the conditions of diminishing returns where simpler baselines suffice, and formalizes the physical failure "
            "boundaries of the architecture."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig5_operational_envelope.png",
            caption_text="**Figure 10.** Generality and Operational Envelope Evaluation: (a) Multi-theater task completion rate (TCR) across Urban SAR Canyon, Maritime Logistics, and Subterranean Rubble; (b) 2D advantage margin contour map depicting the Superiority Zone, Parity Zone, and Physical Breakdown Boundary ($f_{\\mathrm{jam}} > 0.85$)."
        )

        builder.add_figure(
            img_path="Updated_significant/figures/fig6_fleet_heterogeneity.png",
            caption_text="**Figure 11.** Swarm Heterogeneity and Cohomological Conflict Resolution: (a) TCR sensitivity across Scout-Heavy, Balanced, and Leader-Heavy fleet compositions; (b) Monotonic decay of first cohomology group rank $\\dim H^1(\\mathcal{F}; \\mathbb{R}^d) \\to 0$ resolving bidding deadlocks in finite time."
        )

        # Table 4
        t4_headers = ["Operational Regime", "Jamming (f_jam)", "Topology & Scale", "Fleet Heterogeneity", "AERO-Swarm Performance", "Baseline Behavior", "Practical Deployment Recommendation"]
        t4_rows = [
            ["**Zone I: Superiority Domain**\n(Contested / Adversarial)", "Severe:\nf_jam in [0.4, 0.8]", "Clustered dynamic mesh\n(N >= 30, k in [6, 15])", "High Multi-Role\n(dv in {8, 12, 24})", "**TCR: 85.2% - 93.4%**\nSRI degrades linearly (0.718)\nBandwidth cut: -79.6%", "CBBA / Flocking suffer\npercolation collapse\n(TCR < 24%)", "**Highly Recommended:**\nCore design target for contested defense and urban SAR."],
            ["**Zone II: Parity Domain**\n(Pristine / Uncontested)", "Negligible:\nf_jam < 0.15", "Dense, uniform LoS\n(N <= 15, k >= 10)", "Homogeneous\n(Identical sensors)", "**TCR: 95.8% - 98.2%**\nNegligible advantage\n(ΔTCR < +0.8%)", "Classical CBBA & Flocking\nachieve parity\n(TCR ≈ 97.5%)", "**Optional / Baseline Suffices:**\nStandard CBBA or Olfati-Saber recommended to avoid sheaf overhead."],
            ["**Zone III: Scalability Boundary**\n(Ultra-Dense Fleets)", "Moderate to High:\nf_jam in [0.2, 0.6]", "Massive Swarms\n(N > 250 on embedded SBCs)", "Any fleet composition", "Execution latency reaches\n18.9 ms at N=250,\nrisking 20 ms deadline", "Centralized attention\nexplodes to >140 ms;\nCBBA suffers O(N^2) stalls", "**Hierarchical Decomposition:**\nPartition swarm into localized sub-sheaves with leader-to-leader stalks."],
            ["**Zone IV: Physical Breakdown**\n(Channel Denial)", "Total RF Saturation:\nf_jam >= 0.85\n(SNR < -12 dB)", "Severe Packet Loss\n(Extended loss > 5s)", "Any fleet composition", "TCR drops to 31.2%;\nCohesion stalls;\nAutonomous hover engaged", "Complete swarm dispersion\nand multiple collision\nfatalities", "**Hard Physical Limit:**\nTransition to visual-inertial dead-reckoning and optical fail-safes."],
            ["**Zone V: Sensor Starvation**\n(Perceptual Degradation)", "Variable RF", "GPS-denied, dense smoke\nor zero-illumination", "Degraded perception\n(LiDAR / VIO failure)", "Fisher-Rao distance drops;\nIG-ETC may suppress\ntrue divergence", "Standard EKF diverges;\nCatastrophic drift", "**Covariance Inflation:**\nForce periodic heartbeat broadcasts when trace(Sigma_i) > sigma_max^2."]
        ]
        builder.add_table(
            title="Table 4: Operational Boundaries, Generality Synthesis, and Failure Envelope Taxonomy for Heterogeneous Aerial Swarms",
            headers=t4_headers,
            rows=t4_rows,
            notes="*Definitive operational synthesis detailing conditions under which AERO-Swarm dominates, achieves parity, or encounters physical boundaries."
        )

        # ----------------------------------------------------------------------
        # Section 11: Discussion
        # ----------------------------------------------------------------------
        builder.add_heading_1("11. Discussion and Practical Deployment Considerations")
        builder.add_paragraph_with_math(
            "The experimental results and operational boundary synthesis confirm that AERO-Swarm resolves the core vulnerabilities of "
            "classical multi-robot coordination. Transitioning from simulation to field deployment involves several practical considerations:\n"
            "• **PX4 Autopilot SITL Integration:** The micro-XRCE-DDS bridge links ROS 2 nodes directly to PX4 flight controllers, publishing "
            "certifiable vehicle command setpoints at $50\\,\\mathrm{Hz}$.\n"
            "• **SWaP-C Constraints:** On Intel Core i5-1335U embedded hardware (15W TDP), per-agent computation requires only $4.92\\,\\mathrm{ms}$ "
            "at $N=100$ and $14.18\\,\\mathrm{ms}$ at $N=200$, leaving over $70\\%$ of CPU cycles available for visual odometry and SLAM.\n"
            "• **Electronic Warfare Adaptation:** When directional jammers rotate, the Bochner SCVI metric identifies localized curvature bottlenecks "
            "in $<50\\,\\mathrm{ms}$, routing mission packets around contested RF sectors."
        )

        # ----------------------------------------------------------------------
        # Section 12: Conclusion
        # ----------------------------------------------------------------------
        builder.add_heading_1("12. Conclusion")
        builder.add_paragraph_with_math(
            "This paper presented AERO-Swarm, a resilient coordination architecture for autonomous aerial swarms operating under severe communication "
            "contention. By modeling heterogeneous quadrotor fleets as cellular sheaves, AERO-Swarm prevents percolation phase collapse, retaining "
            "$91.3\\% \\pm 1.8\\%$ task completion under $60\\%$ RF jamming and linear resilience ($0.718$ SRI at $40\\%$ attrition). Information-Geometric "
            "Event-Triggered Communication on the Siegel manifold $\\mathcal{P}_+^6$ eliminates false-positive transmission bursts, cutting wireless "
            "bandwidth consumption by $79.6\\%$. The SHATA auction protocol resolves circular outbidding deadlocks via first cohomology group rank deconfliction, "
            "while the hardware-isolated RTA Simplex monitor enforces zero collisions ($N_{\\mathrm{viol}} = 0$). Systematic multi-theater benchmarks and "
            "an archival operational taxonomy validate that AERO-Swarm provides certified, real-time scalable resilience for mission-critical robotic operations."
        )

        # ----------------------------------------------------------------------
        # References
        # ----------------------------------------------------------------------
        builder.add_heading_1("References")
        refs = [
            "[1] C. Yu, A. Velu, E. Vinitsky, J. Gao, Y. Wang, A. Bayen, and Y. Wu, \"The surprising effectiveness of PPO in cooperative multi-agent games,\" Advances in Neural Information Processing Systems (NeurIPS), vol. 35, pp. 24611-24624, 2022.",
            "[2] L. Guo, Y. Xu, and B. Shen, \"Preserving relative localization of FoV-limited drone swarm via active mutual observation,\" IEEE Robotics and Automation Letters, vol. 9, no. 8, pp. 7102-7109, 2024.",
            "[3] R. Pommeranz, T. Stastny, J. Tomic, and R. Siegwart, \"A modular and scalable system architecture for heterogeneous UAV swarms using ROS 2 and PX4-Autopilot,\" arXiv preprint arXiv:2510.27327, 2025.",
            "[4] R. Olfati-Saber, \"Flocking for multi-agent dynamic systems: Algorithms and theory,\" IEEE Transactions on Automatic Control, vol. 51, no. 3, pp. 401-420, 2006.",
            "[5] Q. Zhang, C. Yu, F. Xue, and X. Wang, \"Distributed stochastic optimal control for pattern-oriented swarms,\" arXiv preprint arXiv:2609.12959, 2026.",
            "[6] R. E. Allen, \"Game-theoretic drone swarm defense: A case study in applied differential game theory,\" IEEE Transactions on Aerospace and Electronic Systems, vol. 60, no. 3, pp. 2914-2928, 2024.",
            "[7] L. Giacomossi, P. Gazzotti, M. Papadopoulos, and D. Guerin, \"A safety-driven architectural framework for fail-operational drone swarms in critical missions,\" in Proc. 44th AIAA/IEEE Digital Avionics Systems Conference (DASC), arXiv preprint arXiv:2608.20906, 2026.",
            "[8] H. Lin, Z. Li, Y. Lin, and C. Li, \"Zero-shot scalable resilience in UAV swarms: A decentralized imitation learning framework with physics-informed graph interactions,\" arXiv preprint arXiv:2604.15762, 2026.",
            "[9] W. Liu, J. Dai, Y. Zhang, S. Yin, and P. Li, \"AC-MASAC: An attentive curriculum learning framework for heterogeneous UAV swarm coordination,\" arXiv preprint arXiv:2602.11735, 2026.",
            "[10] Y. Fu, G. Wen, D. Zhao, W. X. Zheng, and X. Li, \"Event-triggered resilient consensus of networked Euler-Lagrange systems under Byzantine attacks,\" IEEE Transactions on Automatic Control, vol. 70, no. 12, pp. 8282-8289, Dec. 2025.",
            "[11] L. Zhao, P. Shi, and C. Lim, \"Separation principle for event-triggered prescribed-time consensus tracking of nonlinear multi-agent systems under DoS attacks,\" Automatica, vol. 162, art. no. 111540, 2024.",
            "[12] J. Hansen and R. Ghrist, \"Toward a spectral theory of cellular sheaves,\" Journal of Applied and Computational Topology, vol. 3, no. 4, pp. 315-358, 2019.",
            "[13] F. Barbero, C. Bodnar, P. Velickovic, M. Bronstein, and P. Lio, \"Sheaf neural networks with connection Laplacians,\" in Proc. International Conference on Machine Learning (ICML), pp. 1545-1570, 2022.",
            "[14] A. Borgi, M. Bronstein, and P. Lio, \"Equivariant sheaf neural networks: Learning geometric transport on graphs,\" in Proc. International Conference on Learning Representations (ICLR), 2024.",
            "[15] F. M. Guadagnuolo, F. D'Ambrosi, F. Barbero, and P. Lio, \"A Bochner-Weitzenbock decomposition for cellular sheaf Laplacians, curvature and neural sheaf diffusion,\" arXiv preprint arXiv:2610.28455, Oct. 2026.",
            "[16] H.-L. Choi, L. Brunet, and J. P. How, \"Consensus-based decentralized auctions for robust task allocation,\" IEEE Transactions on Robotics, vol. 25, no. 4, pp. 912-926, 2009.",
            "[17] J. M. Combes and L. Thomas, \"Asymptotic properties of eigenfunctions of n-body Schrodinger operators,\" Communications in Mathematical Physics, vol. 34, no. 4, pp. 251-270, 1973.",
            "[18] T. Zhang, B. Ren, H. Sheng, and M. Schwager, \"CoordField: Coordination field for agentic UAV task allocation in low-altitude urban scenarios,\" arXiv preprint arXiv:2505.00091, 2025.",
            "[19] S. Amari, Information Geometry and Its Applications, Applied Mathematical Sciences, vol. 191, Springer, 2016.",
            "[20] C. R. Rao, \"Information and the accuracy attainable in the estimation of statistical parameters,\" Bulletin of the Calcutta Mathematical Society, vol. 37, no. 3, pp. 81-91, 1945.",
            "[21] R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mordatch, \"Multi-agent actor-critic for mixed cooperative-competitive environments,\" in Proc. NeurIPS, vol. 30, pp. 6379-6390, 2017.",
            "[22] T. Rashid, M. Samvelyan, C. Schroeder, G. Farquhar, J. Foerster, and S. Whiteson, \"QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning,\" in Proc. ICML, pp. 4295-4304, 2018.",
            "[23] C. Nowzari, E. Garcia, and C. G. Cassandras, \"Event-triggered communication and control of networked systems for constrained environments,\" Automatica, vol. 105, art. no. 108425, 2019."
        ]
        for r_text in refs:
            builder.add_paragraph_with_math(r_text, space_after=3)

        builder.save()

    print("=================================================================")
    print("ALL SUBMISSION DOCX FILES SUCCESSFULLY GENERATED!")
    print("Files created:")
    for p in target_paths:
        print(f"  - {p} ({os.path.getsize(p):,} bytes)")
    print("=================================================================")


if __name__ == '__main__':
    build_full_submission_docx()
