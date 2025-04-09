#!/bin/bash
# docker/python/entrypoint.sh

# Copy the function code
cp /function_code.py /app/function/main.py

# Execute the function with timeout
timeout "${FUNCTION_TIMEOUT:-30}" python -c "
import sys
import json
sys.path.append('/app/function')
from main import handler

# Get input from environment variable or use empty object
input_data = json.loads('${FUNCTION_INPUT:-{}}')

# Call the handler function and print the result
result = handler(input_data)
print(json.dumps(result))
"

# Capture exit code
exit_code=$?

# If timeout, return specific error
if [ $exit_code -eq 124 ]; then
  echo '{"error": "Function execution timed out"}'
  exit 1
fi

# Return other errors
if [ $exit_code -ne 0 ]; then
  echo '{"error": "Function execution failed with exit code '$exit_code'"}'
  exit $exit_code
fi

