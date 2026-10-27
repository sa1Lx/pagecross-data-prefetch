Discard vs Permit page-cross prefetching at the L1D using ChampSim from CS683 PA2.

Changes from PA2:
- ip_stride_permit is ip_stride with the four-line page-boundary check removed.
- Degree variants change only PREFETCH_DEGREE to 8, 16 or 32.
- Free translation uses the existing NO_TRANSLATION_PENALTY_FOR_PREFETCHES option, enabled only while building d16free_discard and d16free_permit.
- Copied prefetchers omit comments, diagnostic prints and the tracker sanity assertion; stride logic is unchanged. Runner progress messages and completed-run skipping are removed. The parser writes summary.csv without printing a table.

Based on the CS683 PA2 ChampSim. Build with GCC 7: bash build_all.sh (from this folder).

Run from the PA2 checkout:
```bash
./build_all.sh
OUT_DIR=results/final/normal ./run_all.sh ../traces_final 50000000 100000000 d16
python3 parse_results.py results/final/normal
```

Run lengths:
- PA2 traces: 25M warm-up + 25M simulated instructions.
- SPEC screening: 25M + 25M.
- Final set: 50M + 100M.

Traces: the three PA2 traces (Trace1.gz, Trace2.gz, Trace3.gz), and DPC-3 SPEC CPU 2017 traces from https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/.

Only summary CSVs are included: results/pa2/ (degree 3, 8, 16, 32 on the PA2 traces), results/spec17_screening_1/ and results/spec17_screening_2/ (12 SPEC CPU 2017 traces, degree 3 and 16), and results/final/normal/ and results/final/free_translation/ (final set, degree 16). No traces, binaries or raw simulation outputs are included.

CS683_project_results.xlsx: all runs (Raw sheet) and the tables and charts used in the report, with short observations.
