# DevOps Toolkit 🛠️

A Python-based command-line tool that helps optimize Dockerfiles and lint Kubernetes YAML files for best practices and security.

## Features

- 🐳 Dockerfile Analyzer:
  - Detects common anti-patterns like using `latest`, missing `.dockerignore`, etc.
- ☸️ Kubernetes YAML Linter:
  - Validates schema and checks for best practices like probes, securityContext, etc.
- ✅ JSON output for automation
- 🎯 Easy to run from CLI

## Installation

```bash
pip install .
