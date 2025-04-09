#!/bin/bash
# docker/javascript/entrypoint.sh

# Copy the function code
cp /function_code.js /app/function/index.js

# Execute the function with timeout
timeout "${FUNCTION_TIMEOUT:-30}" node -e "
const fs = require('fs');
const path = require('path');
const functionPath = path.join('/app/function', 'index.js');
const handler = require(functionPath);

// Get input from environment variable or use empty object
const inputData = JSON.parse(process.env.FUNCTION_INPUT || '{}');

// Call the handler function and print the result
Promise.resolve(handler(inputData))
  .then(result => {
    console.log(JSON.stringify(result));
  })
  .catch(error => {
    console.error(JSON.stringify({ error: error.message }));
    process.exit(1);
  });
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
