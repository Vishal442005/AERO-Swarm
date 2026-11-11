"""
Strict Body-Text Citation Audit for Figures, Tables, and Algorithms
Distinguishes between:
  - Caption/Header appearances (e.g., "Figure 7. Systematic evaluation...")
  - Genuine Body-Text prose citations (e.g., "As shown in Figure 7, ...", "Table 3 contrasts...", "Algorithm 1 executes...")
"""

import re
import docx

def audit_body_citations():
    doc = docx.Document("final_RAS_submission.docx")

    body_paragraphs = []
    captions = []

    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if not txt:
            continue
        # Identify captions: Figure X., Table Y:
        if re.match(r"^(Figure|Fig\.)\s+\d+\.", txt):
            captions.append((i, txt))
        elif re.match(r"^Table\s+\d+:", txt):
            captions.append((i, txt))
        else:
            body_paragraphs.append((i, txt))

    # Also collect table cell prose (excluding Algorithm titles if any, and Table headers)
    # Algorithm boxes are tables containing "Algorithm X:" in first line
    algo_titles = []
    for t_idx, t in enumerate(doc.tables):
        cell0 = t.cell(0, 0).text.strip()
        if cell0.startswith("Algorithm "):
            first_line = cell0.split("\n")[0].strip()
            algo_titles.append((t_idx, first_line))
            # Check remaining steps of algorithm for citations too
            for line in cell0.split("\n")[1:]:
                body_paragraphs.append((f"T{t_idx}", line.strip()))
        else:
            # Skip highlights/abstract tables when checking body citations? Wait - highlights/abstract shouldn't be sole citations anyway, or maybe prose inside sections
            if "RESEARCH HIGHLIGHTS" in cell0 or "ABSTRACT" in cell0:
                continue
            for r in t.rows:
                for c in r.cells:
                    for p in c.paragraphs:
                        if p.text.strip():
                            body_paragraphs.append((f"T{t_idx}", p.text.strip()))

    body_text_only = "\n".join([txt for _, txt in body_paragraphs])

    print("=" * 75)
    print("STRICT BODY-TEXT CITATION AUDIT (EXCLUDING CAPTIONS & TITLES)")
    print("=" * 75)

    # 1. Figures 1 to 15
    print("\n[1] FIGURES (1 to 15):")
    missing_figs = []
    for f in range(1, 16):
        # Count occurrences in body_paragraphs
        matches = re.findall(rf"(?:Figure|Fig\.)\s*{f}\b", body_text_only)
        has_caption = any(re.match(rf"^Figure\s+{f}\.", c[1]) for c in captions)
        status = "[OK]" if len(matches) > 0 else "[MISSING BODY CITATION]"
        if len(matches) == 0:
            missing_figs.append(f)
        print(f"  Figure {f:2d}: Caption={has_caption} | Body Citations={len(matches)} -> {status}")

    # 2. Tables 1 to 5
    print("\n[2] TABLES (1 to 5):")
    missing_tables = []
    for t in range(1, 6):
        matches = re.findall(rf"Table\s*{t}\b", body_text_only)
        has_caption = any(re.match(rf"^Table\s+{t}:", c[1]) for c in captions)
        status = "[OK]" if len(matches) > 0 else "[MISSING BODY CITATION]"
        if len(matches) == 0:
            missing_tables.append(t)
        print(f"  Table  {t:2d}: Caption={has_caption} | Body Citations={len(matches)} -> {status}")

    # 3. Algorithms
    print("\n[3] ALGORITHMS:")
    print(f"  Found {len(algo_titles)} Algorithm box(es):")
    for idx, title in algo_titles:
        print(f"    Box {idx}: {title}")

    missing_algos = []
    for a in range(1, len(algo_titles) + 1):
        matches = re.findall(rf"Algorithm\s*{a}\b", body_text_only)
        status = "[OK]" if len(matches) > 0 else "[MISSING BODY CITATION]"
        if len(matches) == 0:
            missing_algos.append(a)
        print(f"  Algorithm {a}: Body Citations={len(matches)} -> {status}")

    print("\n" + "=" * 75)
    print(f"SUMMARY: Missing Figures={missing_figs}, Missing Tables={missing_tables}, Missing Algos={missing_algos}")
    print("=" * 75)

if __name__ == "__main__":
    audit_body_citations()
