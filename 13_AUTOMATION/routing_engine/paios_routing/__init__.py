"""PAIOS portable model/tool routing layer — V1+ Phase 10.

Implements the decision chain:
  Task -> Requirements -> Capability Profile -> Candidates -> Evidence Filter
       -> Constraint Filter -> Route -> Execute -> Verify -> Record

Vendor-neutral by construction: no model, provider, agent, or MCP server is
canonical. Unknown metrics stay UNKNOWN (None); nothing is invented.
Runtime adapters decide what is actually executable; the router produces
desired routes and records requested-vs-actual verification honestly.
"""

from .capabilities import (  # noqa: F401
    TaskCapabilityProfile, LIFECYCLE_ORDER, LIFECYCLE_RANK,
    REASONING_LEVELS, REASONING_RANK, LATENCY_TOLERANCES, COST_CONSTRAINTS,
    PRIVACY_LEVELS,
)
from .models import ModelCandidate  # noqa: F401
from .tools import ToolCandidate, TOOL_TYPE_PREFERENCE  # noqa: F401
from .reasoning import route_reasoning, COMPLEXITY_ROUTING  # noqa: F401
from .router import (  # noqa: F401
    filter_models, rank_models, filter_tools, rank_tools,
    ModelRoute, ToolRoute, FALLBACK_REASONS, route_models, route_tools,
)
from .fallback import FallbackChain, FallbackTriggered  # noqa: F401
from .verification import RouteVerifier, RouteMatch  # noqa: F401
from .decisions import RoutingDecision, DecisionStore  # noqa: F401
