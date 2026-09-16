"""PAIOS portable orchestration engine — V1+ Phase 9.

Implements the contracts in:
- 03_PROTOCOLS/AIOS_ORCHESTRATION_PROTOCOL.md
- 03_PROTOCOLS/AIOS_WORKER_STATE_SCHEMA_V1.md
- 03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md (authority containment only)
- 11_STATE/AIOS_CHECKPOINT_SCHEMA_V1.md (logical checkpoint integration)

This engine is runtime-independent (Python stdlib only). Runtime-specific
execution lives behind the Executor adapter interface (executor.py).
Worker/task records are operational state, never canonical project knowledge.
"""

__version__ = "1.0.0"

import sys
from pathlib import Path

# Optional integration with the Phase 8 memory/context engine.
_MEMORY_ENGINE = Path(__file__).resolve().parents[1] / "memory_engine"
if _MEMORY_ENGINE.is_dir() and str(_MEMORY_ENGINE) not in sys.path:
    sys.path.insert(0, str(_MEMORY_ENGINE))

from .tasks import TaskContract, validate_task_contract  # noqa: E402
from .states import (  # noqa: E402
    STATES, TRANSITIONS, InvalidTransition, can_transition, terminal,
)
from .ledger import WorkerLedger, WorkerRecord  # noqa: E402
from .events import EventLog  # noqa: E402
from .delegation import (  # noqa: E402
    Delegation, delegate, SCOPE_ESCALATION_REJECTED, AUTHORITY_ESCALATION_REJECTED,
    scope_contains)
from .deps import DependencyGraph, DependencyCycle  # noqa: E402
from .parallel import ParallelRunner  # noqa: E402
from .supervision import Supervisor, SupervisionError  # noqa: E402
from .acceptance import ParentAcceptor, AcceptanceResult  # noqa: E402
from .dispatcher import Dispatcher, DispatchDecision  # noqa: E402
from .executor import (  # noqa: E402
    Executor, ExecutorCapabilities, InlineExecutor, PORTABLE_OPERATIONS)
from .orchestrator import Orchestrator  # noqa: E402
from .states import InvalidTransition, STATES  # noqa: E402
