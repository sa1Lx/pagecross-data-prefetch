# Page-cross prefetching at the L1D (CS683 course project)

Sailesh Kumar Sahoo, 24B1208

The question: when an L1D prefetcher is allowed to prefetch into the next 4 KB page (Permit) instead of stopping at the page boundary (Discard), does it gain or lose because of the predictions, or because of the address translation it needs?

This repo is the CS683 PA2 ChampSim with my changes. Checkpoint I uses the IP-stride L1D prefetcher.

## What I changed

The simulator source (src/, inc/) is unchanged from PA2. I only added files:

- `prefetcher/ip_stride_permit.l1d_pref`: PA2's `ip_stride.l1d_pref` with the 4-line page boundary check removed. This is Permit. The original `ip_stride.l1d_pref` is Discard.
- `prefetcher/ip_stride_d{8,16,32}.l1d_pref` and `prefetcher/ip_stride_permit_d{8,16,32}.l1d_pref`: the same two prefetchers with only `PREFETCH_DEGREE` changed (PA2 uses 3).
- `build_all.sh`: builds every binary I used.
- `run_all.sh`: runs Discard and Permit on every trace in a folder, in parallel.
- `parse_results.py`: reads the ChampSim outputs of a folder and writes `summary.csv`.
- `results/`: summary.csv of every experiment. Raw outputs and traces are not included.
- `CS683_project_results.xlsx`: all runs, plus the tables and charts used in the report.

Free translation runs use PA2's existing option `NO_TRANSLATION_PENALTY_FOR_PREFETCHES` (line 30 of `src/cache.cc`). `build_all.sh` turns it on only while building the two `d16free` binaries, then turns it off again.

## Build

GCC 7 (same as PA2), Ubuntu or WSL.

    bash build_all.sh

Binaries go to `bin/`. Their names end with the tag used below: `baseline`, `permit`, `d3_discard`, `d3_permit`, `d8_...`, `d16_...`, `d32_...`, `d16free_...`.

## Run

    bash run_all.sh <trace folder> <warmup instr> <sim instr> [tag]

Without a tag it runs `baseline` (Discard) and `permit` at degree 3 into `results/`. With a tag it runs `<tag>_discard` and `<tag>_permit` into `results/<tag>/`. Set `OUT_DIR` to change the output folder. Example, the final runs:

    OUT_DIR=results/final/normal bash run_all.sh ../traces_final 50000000 100000000 d16
    python3 parse_results.py results/final/normal

## Traces

- The 3 traces given with PA2.
- SPEC CPU 2017 traces from DPC-3: https://dpc3.compas.cs.stonybrook.edu/champsim-traces/speccpu/

## Results folders

| Folder | Traces | Degree | Warm-up + simulated |
|---|---|---|---|
| results/pa2/ | PA2 Trace1-3 | 3, 8, 16, 32 | 25M + 25M |
| results/spec17_screening_1/, _2/ | 12 SPEC CPU 2017 | 3, 16 | 25M + 25M |
| results/final/normal/ | 6 SPEC CPU 2017 | 16 | 50M + 100M |
| results/final/free_translation/ | same 6 | 16 | 50M + 100M |

## Main results (Checkpoint I)

- PA2 traces: Permit does not change IPC (geomean speedup 1.000).
- SPEC CPU 2017 final set: Permit gains up to 9.1% (mcf-1554B), geomean 1.025. Where it loses, the loss is below 0.2%.
- Where Permit hurts, there are 8 to 17 extra useless prefetches per extra useful one. Where it helps, about 1 or less.
- Free translation adds 4.4% on mcf-1554B and changes almost nothing elsewhere. Page walks and STLB pollution cost nothing visible here. Translation latency does.

## Next (Checkpoint II)

- A small translation buffer at the L1D for prefetches (current and next page), compared against the free translation result.
- Port Berti and repeat Discard vs Permit.
