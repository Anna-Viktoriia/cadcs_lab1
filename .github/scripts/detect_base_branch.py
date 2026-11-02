import json
import os
import sys
from pathlib import Path


def _required_string(value, description):
    if not isinstance(value, str) or not value:
        raise ValueError(f"GitHub event is missing {description}")
    return value


def get_branch_decision(event_name, event):
    repository = event.get("repository")
    if not isinstance(repository, dict):
        raise ValueError("GitHub event is missing repository metadata")

    default_branch = _required_string(
        repository.get("default_branch"), "repository.default_branch"
    )

    if event_name == "push":
        ref = _required_string(event.get("ref"), "push ref")
        if not ref.startswith("refs/heads/"):
            return False, default_branch, ref
        branch = ref.removeprefix("refs/heads/")
    elif event_name == "pull_request":
        pull_request = event.get("pull_request")
        base = pull_request.get("base") if isinstance(pull_request, dict) else None
        branch = _required_string(
            base.get("ref") if isinstance(base, dict) else None,
            "pull_request.base.ref",
        )
    else:
        raise ValueError(f"Unsupported GitHub event: {event_name}")

    return branch == default_branch, default_branch, branch


def main():
    try:
        event_name = _required_string(
            os.environ.get("GITHUB_EVENT_NAME"), "GITHUB_EVENT_NAME"
        )
        event_path = Path(
            _required_string(os.environ.get("GITHUB_EVENT_PATH"), "GITHUB_EVENT_PATH")
        )
        output_path = Path(
            _required_string(os.environ.get("GITHUB_OUTPUT"), "GITHUB_OUTPUT")
        )
        event = json.loads(event_path.read_text(encoding="utf-8"))
        if not isinstance(event, dict):
            raise ValueError("GitHub event payload must be a JSON object")

        should_run, default_branch, event_branch = get_branch_decision(
            event_name, event
        )
        with output_path.open("a", encoding="utf-8", newline="\n") as output:
            output.write(f"run_ci={'true' if should_run else 'false'}\n")
        print(
            f"Repository base branch: {default_branch}; "
            f"event branch: {event_branch}; run CI: {should_run}"
        )
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Base-branch scan failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
