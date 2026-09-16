"""Task dependency model (prompt §10 / OR-05).

C depends on A + B: C is READY only when all dependencies are COMPLETE.
Dependency failure propagates: a task whose dependency FAILED/CANCELLED/STOPPED
becomes BLOCKED with a concrete blocker, never runnable.
"""

from __future__ import annotations

from .states import terminal


class DependencyCycle(Exception):
    pass


class DependencyGraph:
    def __init__(self):
        self._deps: dict[str, set] = {}      # task -> required predecessor tasks

    def declare(self, task_id: str, depends_on: list) -> None:
        deps = set(depends_on)
        deps.discard(task_id)
        if self._would_cycle(task_id, deps):
            raise DependencyCycle(f"dependency cycle involving {task_id}")
        self._deps.setdefault(task_id, set()).update(deps)

    def _would_cycle(self, task_id: str, deps: set) -> bool:
        seen = set()

        def reaches(node: str, target: str) -> bool:
            if node == target:
                return True
            if node in seen:
                return False
            seen.add(node)
            return any(reaches(d, target) for d in self._deps.get(node, ()))

        return any(reaches(d, task_id) for d in deps)

    def dependencies(self, task_id: str) -> set:
        return set(self._deps.get(task_id, ()))

    def readiness(self, task_id: str, states: dict) -> str:
        """Return READY | BLOCKED | POISONED given {task_id: state}."""
        deps = self._deps.get(task_id)
        if not deps:
            return "READY"
        states = {k: (v if isinstance(v, str) else v.state) for k, v in states.items()}
        for d in deps:
            s = states.get(d)
            if s == "COMPLETE":
                continue
            if s in ("FAILED", "CANCELLED", "STOPPED"):
                return "POISONED"       # dependency failure propagates
            return "BLOCKED"            # PENDING/RUNNING/BLOCKED/UNKNOWN
        return "READY"

    def blocker_for(self, task_id: str, states: dict) -> str:
        deps = sorted(self._deps.get(task_id, ()))
        states = {k: (v if isinstance(v, str) else v.state) for k, v in states.items()}
        unsatisfied = [d for d in deps if states.get(d) != "COMPLETE"]
        poisoned = [d for d in unsatisfied if states.get(d) in ("FAILED", "CANCELLED", "STOPPED")]
        if poisoned:
            return f"dependency failure: {', '.join(poisoned)}"
        return f"waiting on dependencies: {', '.join(unsatisfied)}" if unsatisfied else ""
