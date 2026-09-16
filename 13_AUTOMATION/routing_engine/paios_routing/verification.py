"""Route verification (Phase 10 §20): requested route vs actual execution.

Never silently report requested routing as actual routing. Outcomes:
MATCHED | PARTIAL | FAILED | SUBSTITUTED | UNAVAILABLE.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

OUTCOMES = ("MATCHED", "PARTIAL", "FAILED", "SUBSTITUTED", "UNAVAILABLE")


@dataclass
class RouteMatch:
    outcome: str
    requested_model: Optional[str]
    actual_model: Optional[str]
    requested_tools: list
    actual_tools: list
    detail: str = ""
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.outcome not in OUTCOMES:
            raise ValueError(f"invalid outcome: {self.outcome}")

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class RouteVerifier:
    """Compares what was requested with what the runtime actually did."""

    @staticmethod
    def verify(requested_model: Optional[str], actual_model: Optional[str],
               requested_tools: list, actual_tools: list) -> RouteMatch:
        requested_tools = list(requested_tools or [])
        actual_tools = list(actual_tools or [])

        if actual_model is None and not actual_tools:
            return RouteMatch("UNAVAILABLE", requested_model, None,
                              requested_tools, [],
                              detail="runtime reports nothing executed")

        model_ok = (requested_model == actual_model)
        tools_ok = set(requested_tools) == set(actual_tools)

        # A different model or tool set actually ran: explicit substitution.
        if (requested_model is not None and actual_model is not None
                and not model_ok) or (requested_tools and not tools_ok
                                      and set(actual_tools) - set(requested_tools)):
            return RouteMatch("SUBSTITUTED", requested_model, actual_model,
                              requested_tools, actual_tools,
                              detail="runtime substituted a different candidate; "
                                     "recorded, never silent")

        if model_ok and tools_ok:
            return RouteMatch("MATCHED", requested_model, actual_model,
                              requested_tools, actual_tools,
                              detail="actual execution matches requested route")

        if requested_model is None and requested_tools == actual_tools:
            return RouteMatch("MATCHED", None, actual_model, requested_tools,
                              actual_tools, detail="no model requested; tools matched")

        # Partial: a strict subset of requested tools ran, or the model could
        # not be confirmed while requested tools did execute.
        if (requested_tools and set(actual_tools) and set(actual_tools) < set(requested_tools)) or \
                (requested_model is not None and actual_model is None and actual_tools):
            return RouteMatch("PARTIAL", requested_model, actual_model,
                              requested_tools, actual_tools,
                              detail="subset of the requested route executed")

        return RouteMatch("FAILED", requested_model, actual_model,
                          requested_tools, actual_tools,
                          detail="execution did not satisfy the requested route")
