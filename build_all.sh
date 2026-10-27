#!/bin/bash
set -e
./build_champsim.sh ip_stride lru baseline
./build_champsim.sh ip_stride_permit lru permit
./build_champsim.sh ip_stride lru d3_discard
./build_champsim.sh ip_stride_permit lru d3_permit
for D in 8 16 32; do
  ./build_champsim.sh ip_stride_d${D} lru d${D}_discard
  ./build_champsim.sh ip_stride_permit_d${D} lru d${D}_permit
done
sed -i '30s|^//#define NO_TRANSLATION_PENALTY_FOR_PREFETCHES|#define NO_TRANSLATION_PENALTY_FOR_PREFETCHES|' src/cache.cc
status=0
{
  ./build_champsim.sh ip_stride_d16 lru d16free_discard &&
  ./build_champsim.sh ip_stride_permit_d16 lru d16free_permit
} || status=$?
sed -i '30s|^#define NO_TRANSLATION_PENALTY_FOR_PREFETCHES|//#define NO_TRANSLATION_PENALTY_FOR_PREFETCHES|' src/cache.cc
exit "$status"
