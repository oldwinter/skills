#!/usr/bin/env python3
"""Portable entrypoint; the target defaults to the caller's working directory."""

from skills_doctor.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
