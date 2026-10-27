#!/bin/bash
TRACE_DIR=${1:-../traces}
WARM=${2:-25000000}
SIM=${3:-25000000}
TAG=${4:-}
JOBS=${JOBS:-$(nproc)}

if [ -z "$TAG" ]; then
  DISCARD=bin/hashed_perceptron-no-ip_stride-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-baseline
  PERMIT=bin/hashed_perceptron-no-ip_stride_permit-no-no-no-no-no-lru-lru-lru-lru-lru-lru-lru-lru-1core-permit
  OUT=results
else
  DISCARD=$(ls bin/*-1core-${TAG}_discard)
  PERMIT=$(ls bin/*-1core-${TAG}_permit)
  OUT=results/$TAG
fi

OUT=${OUT_DIR:-$OUT}
mkdir -p "$OUT"
shopt -s nullglob
for t in "$TRACE_DIR"/*.xz "$TRACE_DIR"/*.gz; do
  name=$(basename "$t"); name=${name%.xz}; name=${name%.gz}; name=${name%.champsimtrace}
  for mode in discard permit; do
    bin=$DISCARD; [ "$mode" = permit ] && bin=$PERMIT
    out=$OUT/${name}__${mode}.txt
    while [ "$(jobs -rp | wc -l)" -ge "$JOBS" ]; do sleep 5; done
    nohup "$bin" -warmup_instructions "$WARM" -simulation_instructions "$SIM" -traces "$t" > "$out" 2>&1 &
  done
done
wait
