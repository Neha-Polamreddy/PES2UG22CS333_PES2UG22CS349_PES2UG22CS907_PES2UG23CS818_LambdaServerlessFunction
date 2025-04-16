#!/bin/bash

# Copy the user function code to index.js (required name)
cp /function_code.js /app/function/index.js

# Run the function with timeout
timeout "${FUNCTION_TIMEOUT:-30}" node -e "
const input = JSON.parse('${FUNCTION_INPUT:-{}}');
const { handler } = require('/app/function/index.js');
(async () => {
  const result = await handler(input);
  console.log(JSON.stringify(result));
})();
"

# Capture exit code
exit_code=$?

# Handle timeout
if [ $exit_code -eq 124 ]; then
  echo '{\"error\": \"Function execution timed out\"}'
  exit 1
fi

# Handle other errors
if [ $exit_code -ne 0 ]; then
  echo '{\"error\": \"Function execution failed with exit code '$exit_code'\"}'
  exit $exit_code
fi
