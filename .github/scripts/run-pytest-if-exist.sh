#!/bin/bash

if [[ -d "tests" ]] && [[ $(ls tests/*.py 2>/dev/null | wc -l) -gt 0 ]]; then
    echo "Tests exist, running pytest..."
    pytest tests
else
    echo "No tests found, skipping pytest..."
fi
