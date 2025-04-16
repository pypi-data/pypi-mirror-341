# k8s_linter/linter.py
import yaml

def lint_k8s_yaml(path):
    issues = []

    def add_issue(message, level="warning"):
        issues.append({"type": level, "message": message})

    with open(path, "r") as f:
        try:
            docs = list(yaml.safe_load_all(f))
        except yaml.YAMLError as e:
            add_issue(f"YAML syntax error: {e}", "error")
            return issues

    for doc in docs:
        if not isinstance(doc, dict):
            continue

        kind = doc.get("kind", "")
        metadata = doc.get("metadata", {})
        spec = doc.get("spec", {})

        if not doc.get("apiVersion"):
            add_issue("Missing 'apiVersion' field.")
        if not kind:
            add_issue("Missing 'kind' field.")
        if not metadata.get("name"):
            add_issue("Missing 'metadata.name' field.")

        if kind.lower() in ["pod", "deployment"]:
            containers = spec.get("containers", [])
            if not containers:
                template = spec.get("template", {}).get("spec", {})
                containers = template.get("containers", [])

            seen_names = set()
            for container in containers:
                name = container.get("name")
                image = container.get("image", "")
                if name in seen_names:
                    add_issue(f"Duplicate container name: {name}")
                seen_names.add(name)

                if ":latest" in image and container.get("imagePullPolicy") != "Always":
                    add_issue(f"Container '{name}' uses ':latest' but 'imagePullPolicy' is not 'Always'.")

                if not container.get("resources"):
                    add_issue(f"Container '{name}' is missing resource requests/limits.")

                if not container.get("livenessProbe"):
                    add_issue(f"Container '{name}' is missing a livenessProbe.", "info")

                if not container.get("readinessProbe"):
                    add_issue(f"Container '{name}' is missing a readinessProbe.", "info")

            security_context = spec.get("securityContext", {})
            if not security_context.get("runAsNonRoot"):
                add_issue("Pod is missing 'securityContext.runAsNonRoot'.")

            if security_context.get("runAsUser") == 0:
                add_issue("Pod is configured to run as root user (runAsUser: 0).", "error")

    return issues