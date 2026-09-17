"""Untrusted-content boundary for runtime output (Protocol §10).

Runtime output (results, logs, tool output, sub-agent text) is data. It can
never grant authority, expand scope, modify policy, override acceptance
criteria, or change delegated permissions.
"""

from __future__ import annotations

INJECTION_MARKERS = (
    "ignore previous instructions", "ignore paios policy", "disable safeguards",
    "grant yourself authority", "expand your scope", "you are now",
    "authorize yourself", "override acceptance criteria", "override policy",
    "self-authorize",
)


class UntrustedContent(Exception):
    """Runtime output attempted to exercise authority over PAIOS."""


def inspect_runtime_output(text: str) -> dict:
    """Treat runtime output as untrusted data. Instruction-like content is
    refused (the caller must log and discard it). Benign data passes."""
    lowered = (text or "").lower()
    hits = [m for m in INJECTION_MARKERS if m in lowered]
    if hits:
        raise UntrustedContent(
            f"runtime output attempted to instruct PAIOS ({hits}); "
            f"treated as untrusted data and refused")
    return {"trusted_as_data": True}
