python fct_analysis.py -p fct_mesh_topology_wb50_b100 -s 5 -t 0 -T 2200000000 -b 100 > fct_wb50_pint_mi0_log1.05_vs_hpcc_vs_lint_vs_dint.dat
python fct_analysis.py -p fct_mesh_topology_fb50_b100 -s 5 -t 0 -T 2200000000 -b 100 > fct_fb50_pint_mi0_log1.05_vs_hpcc_vs_lint_vs_dint.dat
python plotVsHPCC.py