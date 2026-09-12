#!/usr/bin/env python3
"""Query a Code Wiki index without loading the complete tree into agent context."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath


START = "code-wiki:start"
END = "code-wiki:end"


def output(value: object) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n")


def root_for(value: str) -> Path:
    candidate = Path(value).expanduser().resolve()
    result = subprocess.run(["git", "-C", str(candidate), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if result.returncode != 0:
        raise ValueError("not inside a Git worktree")
    return Path(result.stdout.strip()).resolve()


def load(root: Path) -> dict:
    path = root / ".code-wiki" / "wiki.json"
    if not path.exists():
        raise LookupError("Code Wiki index is missing")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LookupError(f"Code Wiki index is invalid: {exc}") from exc
    if not _valid_index(value):
        raise LookupError("Code Wiki schema is unsupported or invalid")
    return value


def _valid_index(value: object) -> bool:
    if not isinstance(value, dict) or set(value) != {"schema_version", "generator", "repository", "tree"}:
        return False
    if value.get("schema_version") != "1.0" or value.get("generator") != {"name": "code-wiki", "version": "0.1.0"}:
        return False
    repository = value.get("repository")
    if not isinstance(repository, dict) or set(repository) != {"name", "root", "summary", "source_roots", "hash_algorithm", "tree_hash"}:
        return False
    if repository.get("root") != "." or repository.get("hash_algorithm") != "sha256":
        return False
    return _valid_directory(value.get("tree"))


def _valid_directory(node: object) -> bool:
    if not isinstance(node, dict) or set(node) != {"path", "purpose", "summary", "files", "directories"}:
        return False
    if not isinstance(node["files"], dict) or not isinstance(node["directories"], dict):
        return False
    required_file = {"path", "kind", "language", "summary", "content_hash", "documentation_hash", "documentation"}
    if any(not isinstance(entry, dict) or set(entry) != required_file for entry in node["files"].values()):
        return False
    return all(_valid_directory(child) for child in node["directories"].values())


def flatten(node: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for entry in node.get("files", {}).values():
        if isinstance(entry, dict) and isinstance(entry.get("path"), str):
            result[entry["path"]] = entry
    for child in node.get("directories", {}).values():
        if isinstance(child, dict):
            result.update(flatten(child))
    return result


def show(index: dict, requested: str) -> dict:
    pure = PurePosixPath(requested)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError("path must be repository-relative and must not contain ..")
    normalized = pure.as_posix()
    if normalized == ".":
        return {"repository": index["repository"], "node": index["tree"]}
    node = index["tree"]
    parts = pure.parts
    for position, part in enumerate(parts):
        if position == len(parts) - 1 and part in node.get("files", {}):
            return node["files"][part]
        child = node.get("directories", {}).get(part)
        if not isinstance(child, dict):
            raise LookupError(f"path is not indexed: {requested}")
        node = child
    return node


def hash_without_header(path: Path) -> str:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = None
    if text is not None:
        lines = text.splitlines(keepends=True)
        starts = [index for index, line in enumerate(lines) if START in line]
        ends = [index for index, line in enumerate(lines) if END in line]
        if len(starts) == 1 and len(ends) == 1 and starts[0] < ends[0]:
            data = "".join(lines[:starts[0]] + lines[ends[0] + 1:]).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def stale(root: Path, index: dict) -> list[dict]:
    result = []
    for relative, entry in sorted(flatten(index["tree"]).items()):
        path = root / relative
        actual = None if not path.is_file() else hash_without_header(path)
        if actual != entry.get("content_hash"):
            result.append({"path": relative, "stored_content_hash": entry.get("content_hash"), "current_content_hash": actual})
    return result


def status(index: dict) -> dict:
    counts = {"current": 0, "stale": 0, "missing": 0, "unsupported": 0, "error": 0}
    for entry in flatten(index["tree"]).values():
        state = entry.get("documentation", {}).get("status", "error")
        counts[state if state in counts else "error"] += 1
    return {
        "present": True,
        "valid": True,
        "schema_version": index["schema_version"],
        "tree_hash": index.get("repository", {}).get("tree_hash"),
        "counts": counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--json", action="store_true", required=True)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    subparsers.add_parser("status")
    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("path")
    subparsers.add_parser("stale")
    args = parser.parse_args()
    try:
        root = root_for(args.root)
        index = load(root)
        if args.operation == "status":
            output(status(index))
        elif args.operation == "show":
            output(show(index, args.path))
        else:
            entries = stale(root, index)
            output(entries)
            if entries:
                return 1
        return 0
    except LookupError as exc:
        output({"valid": False, "error": str(exc)})
        return 1
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
