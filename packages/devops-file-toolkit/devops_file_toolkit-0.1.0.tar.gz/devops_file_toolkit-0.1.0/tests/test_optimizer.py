from docker_optimizer.optimizer import analyze_dockerfile

def test_detect_latest_tag(tmp_path):
    dockerfile = tmp_path / "sample/Dockerfile"
    dockerfile.write_text("FROM python:latest")
    issues = analyze_dockerfile(str(dockerfile))
    assert any("latest" in issue["message"] for issue in issues)

def test_detect_add_usage(tmp_path):
    dockerfile = tmp_path / "sample/Dockerfile"
    dockerfile.write_text("FROM ubuntu\nADD . /app")
    issues = analyze_dockerfile(str(dockerfile))
    assert any("ADD" in issue["message"] for issue in issues)
