"""Shared small utilities for the routing package."""

from __future__ import annotations

from datetime import datetime, timezone

SENSITIVITY_ORDER = ("PUBLIC", "INTERNAL", "PERSONAL", "SENSITIVE")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sensitivity_rank(level: str) -> int:
    return SENSITIVITY_ORDER.index(level)
