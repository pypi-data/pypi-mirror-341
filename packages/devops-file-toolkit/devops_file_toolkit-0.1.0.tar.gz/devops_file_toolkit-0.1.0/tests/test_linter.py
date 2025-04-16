from k8s_linter.linter import lint_k8s_yaml

def test_missing_api_version(tmp_path):
    yaml_file = tmp_path / "sample/sample.yaml"
    yaml_file.write_text("kind: Pod\nmetadata:\n  name: test")
    issues = lint_k8s_yaml(str(yaml_file))
    assert any("apiVersion" in issue["message"] for issue in issues)

def test_run_as_root_detected(tmp_path):
    yaml_file = tmp_path / "sample/sample.yaml"
    yaml_file.write_text("""\napiVersion: v1\nkind: Pod\nmetadata:\n  name: test\nspec:\n  containers:\n    - name: web\n      image: nginx\n  securityContext:\n    runAsUser: 0\n""")
    issues = lint_k8s_yaml(str(yaml_file))
    assert any("runAsUser" in issue["message"] for issue in issues)