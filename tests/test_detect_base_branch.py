import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


SCANNER = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "scripts"
    / "detect_base_branch.py"
)


@pytest.mark.parametrize(
    ("event_name", "event", "expected"),
    [
        (
            "push",
            {
                "repository": {"default_branch": "main"},
                "ref": "refs/heads/main",
            },
            "run_ci=true\n",
        ),
        (
            "push",
            {
                "repository": {"default_branch": "main"},
                "ref": "refs/heads/feature/example",
            },
            "run_ci=false\n",
        ),
        (
            "pull_request",
            {
                "repository": {"default_branch": "main"},
                "pull_request": {"base": {"ref": "main"}},
            },
            "run_ci=true\n",
        ),
        (
            "pull_request",
            {
                "repository": {"default_branch": "main"},
                "pull_request": {"base": {"ref": "develop"}},
            },
            "run_ci=false\n",
        ),
    ],
)
def test_scanner_detects_default_branch(tmp_path, event_name, event, expected):
    event_path = tmp_path / "event.json"
    output_path = tmp_path / "github-output.txt"
    event_path.write_text(json.dumps(event), encoding="utf-8")
    env = os.environ.copy()
    env.update(
        {
            "GITHUB_EVENT_NAME": event_name,
            "GITHUB_EVENT_PATH": str(event_path),
            "GITHUB_OUTPUT": str(output_path),
        }
    )

    result = subprocess.run(
        [sys.executable, str(SCANNER)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output_path.read_text(encoding="utf-8") == expected


def test_scanner_fails_when_default_branch_is_missing(tmp_path):
    event_path = tmp_path / "event.json"
    output_path = tmp_path / "github-output.txt"
    event_path.write_text(
        json.dumps({"repository": {}, "ref": "refs/heads/main"}),
        encoding="utf-8",
    )
    env = os.environ.copy()
    env.update(
        {
            "GITHUB_EVENT_NAME": "push",
            "GITHUB_EVENT_PATH": str(event_path),
            "GITHUB_OUTPUT": str(output_path),
        }
    )

    result = subprocess.run(
        [sys.executable, str(SCANNER)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode == 1
    assert "repository.default_branch" in result.stderr
