#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 namespace"
    exit 0
fi

namespace=$1
attempts=30
waittime=10

echo "Smoke test start"

for i in $(seq $attempts); do

    echo "Waiting $waittime s for containers to be running"
    sleep $waittime

    waiting=$(kubectl get pods -n $namespace -o=jsonpath='{.items[*].status.containerStatuses[*].state.waiting.reason}' | wc -w)
    echo "Number of containers waiting: $waiting"

    if [ $waiting -eq 0 ]; then
        echo "Smoke test succeeded"
        exit 0
    elif [ $i -eq $attempts ]; then
        echo "Smoke test failed"
        echo "Containers still waiting:"
        kubectl get pods -n $namespace -o=jsonpath='{range .items[*].status.containerStatuses[?(.state.waiting)]}{.state.waiting.message}{"\n"}{end}'
        exit 1
    fi

done
