#!/bin/bash
# docker/python/entrypoint.sh

# Execute the function with timeout
timeout "${FUNCTION_TIMEOUT:-30}" python -c '
import sys
import json
import os
sys.path.append("/app/function")
from main import handler

try:
    input_json = os.environ.get("FUNCTION_INPUT", "{}")
    input_data = json.loads(input_json)
    result = handler(input_data)
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
'

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
