# PARAMETERS
log_dir=~/data/ycsb

should_load=0
should_run=0
while [ $# -gt 0 ]; do
    case "$1" in
    "load") should_load=1;;
    "run") should_run=1;;
    esac
    shift
done


if [ $should_load == 1 ]; then
    docker exec -it roach0 \
        ./cockroach workload init ycsb \
        --drop \
        postgresql://root@roach1:26257?sslmode=disable
fi

if [ $should_run == 1 ]; then
    docker exec -it roach0 \
        ./cockroach workload run ycsb \
        postgresql://root@roach1:26257,roach2:26257,roach3:26257?sslmode=disable \
        --workload=A \
        --max-ops=1000000 \
        --duration=10m \
        --max-rate=0 \
        --display-every=1s \
        --tolerate-errors \
        # > ${log_dir}/raw.log 2> >(tee ${log_dir}/runtime.log >&2)
fi

