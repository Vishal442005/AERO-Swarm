import os
import re
import pandas as pd

def verify_all():
    print("=================================================================")
    print("AERO-Swarm Publication & Archival Consistency Verification Suite")
    print("=================================================================")
    
    errors = []
    warnings = []
    
    # 1. Check Data CSVs
    csv_dir = "Updated_significant/results_data"
    required_csvs = [
        "scenario1_progressive_jamming.csv",
        "scenario2_catastrophic_attrition.csv",
        "scenario3_scalability.csv",
        "scenario5_comm_protocols.csv",
        "scenario6_operational_envelope.csv",
        "scenario7_fleet_heterogeneity.csv",
        "ros2_extended_simulation_metrics.csv",
        "stress_test_extreme_conditions.csv"
    ]
    
    for f in required_csvs:
        p = os.path.join(csv_dir, f)
        if not os.path.exists(p):
            errors.append(f"Missing CSV: {p}")
        else:
            df = pd.read_csv(p)
            if df.empty:
                errors.append(f"CSV is empty: {p}")
            if f != "stress_test_extreme_conditions.csv" and df.isnull().values.any():
                errors.append(f"CSV contains unexpected NaN/null values: {p}")
            print(f"[OK] CSV verified: {f} ({len(df)} rows, columns: {list(df.columns)})")

    # 2. Key values check in CSVs
    s1 = pd.read_csv(os.path.join(csv_dir, "scenario1_progressive_jamming.csv"))
    # Check row jamming_fraction = 0.6
    row_06 = s1[s1['jamming_fraction'] == 0.6]
    if not row_06.empty:
        tcr_aero = row_06['AERO_TCR_mean'].values[0]
        if abs(tcr_aero - 91.3) > 0.1:
            errors.append(f"Scenario 1 jamming_fraction=0.6 AERO TCR is {tcr_aero}, expected 91.3")
        else:
            print(f"[OK] Scenario 1 jamming_fraction=0.6 AERO TCR matches: {tcr_aero}%")
            
    s2 = pd.read_csv(os.path.join(csv_dir, "scenario2_catastrophic_attrition.csv"))
    row_04 = s2[s2['attrition_rate'] == 0.4]
    if not row_04.empty:
        sri_sheaf = row_04['sheaf_sri_mean'].values[0]
        sri_graph = row_04['flat_sri_mean'].values[0]
        if abs(sri_sheaf - 0.718) > 0.005:
            errors.append(f"Scenario 2 attrition_rate=0.4 Sheaf SRI is {sri_sheaf}, expected 0.718")
        else:
            print(f"[OK] Scenario 2 attrition_rate=0.4 Sheaf SRI matches: {sri_sheaf}")
        if abs(sri_graph - 0.082) > 0.005:
            errors.append(f"Scenario 2 attrition_rate=0.4 Graph SRI is {sri_graph}, expected 0.082")
        else:
            print(f"[OK] Scenario 2 attrition_rate=0.4 Graph SRI matches: {sri_graph} (Phase Collapse below 0.1)")

    s3 = pd.read_csv(os.path.join(csv_dir, "scenario3_scalability.csv"))
    row_200 = s3[s3['swarm_size_N'] == 200]
    if not row_200.empty:
        lat = row_200['AERO_latency_ms'].values[0]
        if abs(lat - 14.18) > 0.05:
            errors.append(f"Scenario 3 N=200 Latency is {lat}, expected 14.18 ms")
        else:
            print(f"[OK] Scenario 3 N=200 Latency matches: {lat} ms")

    s5 = pd.read_csv(os.path.join(csv_dir, "scenario5_comm_protocols.csv"))
    last_row = s5.iloc[-1]
    p_aero = last_row['AERO_packets_k']
    p_per = last_row['Periodic_packets_k']
    reduction = (1.0 - p_aero / p_per) * 100
    if abs(reduction - 79.596) > 0.1:
        errors.append(f"Bandwidth reduction is {reduction:.2f}%, expected 79.6%")
    else:
        print(f"[OK] Bandwidth reduction matches: {reduction:.1f}% ({p_aero}k vs {p_per}k packets)")

    # 3. Check Manuscript LaTeX
    tex_path = "Updated_significant/manuscript/main.tex"
    if not os.path.exists(tex_path):
        errors.append(f"Missing LaTeX file: {tex_path}")
    else:
        with open(tex_path, 'r', encoding='utf-8') as f:
            tex_content = f.read()
        
        # Check for target keywords and numbers
        targets = [
            ("91.3", "TCR 91.3%"),
            ("0.718", "SRI 0.718"),
            ("79.6\\%", "Bandwidth reduction 79.6%"),
            ("14.18", "Latency 14.18 ms"),
            ("0.42", "Latency 0.42 ms at N=10"),
            ("4.92", "Latency 4.92 ms at N=100"),
            ("Generality Synthesis", "Generality Synthesis section"),
            ("fig5_operational_envelope", "Figure 5 referenced"),
            ("fig6_fleet_heterogeneity", "Figure 6 referenced"),
            ("Urban SAR Canyon", "Urban SAR Canyon referenced"),
            ("Maritime Logistics", "Maritime Logistics referenced"),
            ("Subterranean Rubble", "Subterranean Rubble referenced"),
            ("percolation threshold", "Percolation threshold referenced"),
            ("Riemannian", "Riemannian geometry on positive definite matrices referenced"),
            ("Cohomological", "Cohomological conflict resolution referenced")
        ]
        
        for tgt, desc in targets:
            if tgt in tex_content:
                print(f"[OK] LaTeX contains {desc}")
            else:
                warnings.append(f"LaTeX missing exact token for {desc}: '{tgt}'")

    # 4. Check Figure files
    fig_dir = "Updated_significant/figures"
    required_figs = [
        "fig1_tcr_vs_jamming.png",
        "fig2_sri_resilience.png",
        "fig3_comm_efficiency.png",
        "fig4_scalability_runtime.png",
        "fig5_operational_envelope.png",
        "fig6_fleet_heterogeneity.png",
        "fig_teaser_sheaf_concept.png",
        "fig_ros2_architecture.png",
        "fig_flowchart1_sheaf_coordination.png",
        "fig_flowchart2_ig_etc.png",
        "fig_flowchart3_shata_auction.png",
        "aero_swarm_mission_replay.gif"
    ]
    for fig in required_figs:
        p = os.path.join(fig_dir, fig)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            errors.append(f"Figure file missing or zero size: {p}")
        else:
            print(f"[OK] Figure verified: {fig} ({os.path.getsize(p):,} bytes)")

    # 5. Check Tables
    table_dir = "Updated_significant/tables"
    required_tables = [
        "table1_qualitative_comparison.md",
        "table2_systematic_benchmarks.md",
        "table3_factorial_ablation.md",
        "table4_operational_boundaries_synthesis.md",
        "table_comprehensive_parameter_comparison.md",
        "table_comprehensive_parameter_comparison.tex"
    ]
    for tab in required_tables:
        p = os.path.join(table_dir, tab)
        if not os.path.exists(p):
            errors.append(f"Table file missing: {p}")
        else:
            print(f"[OK] Table verified: {tab}")

    print("\n----------------- SUMMARY -----------------")
    print(f"Total Errors: {len(errors)}")
    print(f"Total Warnings: {len(warnings)}")
    if errors:
        for e in errors:
            print(f"  [ERROR] {e}")
    if warnings:
        for w in warnings:
            print(f"  [WARNING] {w}")
            
    if not errors and not warnings:
        print("ALL VERIFICATION CHECKS PASSED PERFECTLY (100% NUMERICAL & ARCHIVAL HARMONY)!")

if __name__ == '__main__':
    verify_all()
