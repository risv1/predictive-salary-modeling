#!/bin/bash
set -e 

check_container_health() {
    local container=$1
    local status=$(docker inspect -f '{{.State.Status}}' $container 2>/dev/null)
    if [ "$status" != "running" ]; then
        return 1
    fi
    return 0
}

wait_for_containers() {
    local containers=("nodemanager" "resourcemanager" "namenode" "datanode" "historyserver" "spark-spark-worker-1" "spark-spark-1")
    
    for container in "${containers[@]}"; do
        echo "Waiting for $container..."
        while ! check_container_health $container; do
            sleep 2
        done
        echo "$container is ready"
    done
}

echo "Starting Hadoop services..."
cd services/hadoop
docker compose up -d

echo "Starting Spark services..."
cd ../spark
docker compose up -d

wait_for_containers

echo "Copying data processing script..."
if [ ! -f "./load_data.py" ]; then
    echo "Error: load_data.py not found"
    exit 1
fi

docker exec spark-spark-1 rm -rf /app/output || true

docker exec -it spark-spark-1 mkdir /app/output
docker exec -it spark-spark-1 chmod -R 777 /app/output

docker cp ./load_data.py spark-spark-1:/app/load_data.py

echo "Running Spark job..."
docker exec spark-spark-1 spark-submit /app/load_data.py
if [ $? -ne 0 ]; then
    echo "Spark job failed"
    exit 1
fi

echo "Spark job completed successfully"
