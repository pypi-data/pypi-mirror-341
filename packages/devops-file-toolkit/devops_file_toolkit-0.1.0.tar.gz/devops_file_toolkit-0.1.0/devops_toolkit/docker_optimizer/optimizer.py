# docker_optimizer/optimizer.py
import os
from dockerfile_parse import DockerfileParser

def analyze_dockerfile(path):
    dfp = DockerfileParser(path=path)
    issues = []

    def add_issue(message, level="warning"):
        issues.append({"type": level, "message": message})

    # Rule 1: Avoid latest tag
    if dfp.baseimage and dfp.baseimage.endswith(":latest"):
        add_issue("Avoid using the 'latest' tag in base image.")

    # Rule 2: COPY should come before RUN
    commands = [cmd["instruction"] for cmd in dfp.structure]
    if "COPY" in commands and "RUN" in commands and commands.index("COPY") > commands.index("RUN"):
        add_issue("Consider moving 'COPY' before 'RUN' for better layer caching.")

    # Rule 3: Dockerfile should end with newline
    if not dfp.content.strip().endswith("\n"):
        add_issue("Dockerfile should end with a newline.", "info")

    # Rule 4: Avoid using ADD unless necessary
    if any(cmd["instruction"] == "ADD" for cmd in dfp.structure):
        add_issue("Avoid using 'ADD' unless needed for remote URLs or archive extraction.", "info")

    # Rule 5: Check for apt-get update without cleanup
    for cmd in dfp.structure:
        if cmd["instruction"] == "RUN" and "apt-get update" in cmd["value"]:
            if not any(x in cmd["value"] for x in ["rm -rf /var/lib/apt/lists", "--no-install-recommends"]):
                add_issue("Clean up apt cache after apt-get update to reduce image size.")

    # Rule 6: Recommend multistage builds
    if any("build-essential" in cmd["value"] or "gcc" in cmd["value"] for cmd in dfp.structure if cmd["instruction"] == "RUN"):
        add_issue("Consider using multistage builds to reduce image size.", "info")

    # Rule 7: Suggest Alpine or slim images
    if dfp.baseimage and any(x in dfp.baseimage for x in ["python", "node"]):
        if not any(x in dfp.baseimage for x in ["alpine", "slim"]):
            add_issue("Consider using Alpine or slim base images where possible.", "info")

    # Rule 8: Check for .dockerignore file
    dockerignore_path = os.path.join(os.path.dirname(path), ".dockerignore")
    if not os.path.exists(dockerignore_path):
        add_issue(".dockerignore file not found. You should add one to avoid sending unnecessary files to Docker context.", "info")

    return issues
