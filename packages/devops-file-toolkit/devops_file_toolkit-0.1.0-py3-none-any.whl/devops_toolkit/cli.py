import argparse
import json
from devops_toolkit.docker_optimizer.optimizer import analyze_dockerfile
from devops_toolkit.k8s_linter.linter import lint_k8s_yaml


def main():
    parser = argparse.ArgumentParser(description="DevOps Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    docker_parser = subparsers.add_parser("optimize-docker", help="Analyze and optimize a Dockerfile")
    docker_parser.add_argument("path", help="Path to Dockerfile")
    docker_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    yaml_parser = subparsers.add_parser("lint-yaml", help="Lint a Kubernetes YAML file")
    yaml_parser.add_argument("path", help="Path to YAML file")
    yaml_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if args.command == "optimize-docker":
        issues = analyze_dockerfile(args.path)
        if args.json:
            print(json.dumps(issues, indent=2))
        else:
            print("Dockerfile Analysis:")
            for issue in issues:
                print(f"- [{issue['type'].upper()}] {issue['message']}")

    elif args.command == "lint-yaml":
        issues = lint_k8s_yaml(args.path)
        if args.json:
            print(json.dumps(issues, indent=2))
        else:
            print("YAML Lint Results:")
            for issue in issues:
                print(f"- [{issue['type'].upper()}] {issue['message']}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
