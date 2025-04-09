# backend/executor.py
import docker
import os
import json
import tempfile
import logging
from asyncio import create_subprocess_exec, subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class FunctionExecutor:
    def __init__(self):
        self.client = docker.from_env()

        # Ensure Docker images are built
        self._ensure_images()

    def _ensure_images(self):
        """Make sure the required Docker images exist, build them if not."""
        required_images = {
            "lambda-python-runtime": os.path.join("docker", "python"),
            "lambda-js-runtime": os.path.join("docker", "javascript")
        }

        for image_name, dockerfile_path in required_images.items():
            try:
                self.client.images.get(image_name)
                logger.info(f"Image {image_name} already exists")
            except docker.errors.ImageNotFound:
                logger.info(f"Building image {image_name}...")
                # Get the absolute path to the Dockerfile directory
                base_path = Path(__file__).parent.parent
                dockerfile_abs_path = base_path / dockerfile_path

                # Build the image
                _, logs = self.client.images.build(
                    path=str(dockerfile_abs_path),
                    tag=image_name,
                    rm=True
                )
                for log in logs:
                    if 'stream' in log:
                        logger.info(log['stream'].strip())

    async def execute_function(self, function_code, language, timeout, input_data=None):
        """Execute the function in a container and return the result."""
        if language.lower() not in ["python", "javascript"]:
            raise ValueError(f"Unsupported language: {language}")

        # Set defaults
        image_name = "lambda-python-runtime" if language.lower() == "python" else "lambda-js-runtime"
        file_extension = ".py" if language.lower() == "python" else ".js"

        # Create a temporary file for the function code
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            temp_file.write(function_code.encode())
            temp_file_path = temp_file.name

        try:
            # Prepare input data
            input_json = json.dumps(input_data or {})

            # Run the container
            container = self.client.containers.run(
                image=image_name,
                environment={
                    "FUNCTION_TIMEOUT": str(timeout),
                    "FUNCTION_INPUT": input_json
                },
                volumes={
                    temp_file_path: {
                        "bind": "/function_code" + file_extension,
                        "mode": "ro"
                    }
                },
                detach=True
            )

            # Wait for the container to finish
            result = container.wait(timeout=timeout + 5)
            logs = container.logs().decode('utf-8')

            # Cleanup
            container.remove()

            # Parse the output
            exit_code = result["StatusCode"]
            if exit_code != 0:
                if "Function execution timed out" in logs:
                    return {"error": "Function execution timed out"}
                return {"error": f"Function execution failed with exit code {exit_code}", "logs": logs}

            try:
                return json.loads(logs)
            except json.JSONDecodeError:
                return {"result": logs}

        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
