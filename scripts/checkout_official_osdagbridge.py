#!/usr/bin/env python3
"""Fetch the official OsdagBridge desktop source at a reproducible commit.

The upstream source is kept in its own repository. This script checks it out
under vendor/OsdagBridge-Desktop without mixing upstream files into the QA repo.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

UPSTREAM_URL = "https://github.com/osdagbridge/OsdagBridge-Desktop.git"
PINNED_COMMIT = "f62ceba7f3324431c76d92184ef61da9cd265731"
DEFAULT_DESTINATION = Path("vendor/OsdagBridge-Desktop")


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    parser.add_argument("--commit", default=PINNED_COMMIT,
                        help="Upstream commit SHA to check out (default: pinned, tested source revision).")
    args = parser.parse_args()
    destination = args.destination.resolve()

    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(
            f"Refusing to overwrite non-empty checkout: {destination}\n"
            "Move it aside or choose another --destination."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        run(["git", "clone", "--no-checkout", UPSTREAM_URL, str(destination)])
    else:
        run(["git", "clone", "--no-checkout", UPSTREAM_URL, str(destination)])

    run(["git", "fetch", "--depth", "1", "origin", args.commit], cwd=destination)
    run(["git", "checkout", "--detach", "FETCH_HEAD"], cwd=destination)
    actual = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=destination, text=True
    ).strip()
    if actual != args.commit:
        raise SystemExit(f"Commit verification failed: expected {args.commit}, got {actual}")
    print(f"Official OsdagBridge desktop source checked out at {actual}")
    print(f"Location: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
