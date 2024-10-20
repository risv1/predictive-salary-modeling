#!/bin/bash

docker exec spark-spark-1 test -f /app/output
if [ $? -ne 0 ]; then
    echo "Output file not found in container"
    exit 1
fi

echo "Copying processed data..."

docker cp spark-spark-1:/app/data.csv ./data/data.csv
if [ $? -ne 0 ]; then
    echo "Failed to copy data file"
    exit 1
fi

echo "Processing completed successfully"