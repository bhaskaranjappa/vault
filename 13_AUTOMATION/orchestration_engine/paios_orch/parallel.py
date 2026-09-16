"""Parallel execution of independent workers (prompt §9 / OR-04).

Uses concurrent.futures (stdlib). Each parallel branch gets a unique worker
identity and isolated objective/scope; results are aggregated deterministically
with per-worker failure visibility. Parent acceptance happens afterwards via
acceptance.ParentAcceptor — parallel success never implies parent success.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class BranchResult:
    worker_id: str
    ok: bool
    result=None
    error: str | None = None

    def __init__(self, worker_id: str, ok: bool, result=None, error: str | None = None):
        self.worker_id = worker_id
        self.ok = ok
        self.result = result
        self.error = error


class ParallelRunner:
    """Executes callables concurrently; the caller wires each callable to its
    executor adapter. Conflicting mutations must NOT be submitted without an
    explicit coordination mechanism — this runner does not lock shared files."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def run(self, branches: dict) -> dict:
        """branches: {branch_name: (worker_id, callable)}. Returns
        {branch_name: BranchResult} preserving per-branch failure."""
        results: dict[str, BranchResult] = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = {}
            for name, (worker_id, fn) in branches.items():
                futures[pool.submit(fn)] = (name, worker_id)
            for fut in as_completed(futures):
                name, worker_id = futures[fut]
                try:
                    results[name] = BranchResult(worker_id, True, result=fut.result())
                except Exception as exc:            # failure visibility per branch
                    results[name] = BranchResult(worker_id, False, error=f"{type(exc).__name__}: {exc}")
        return results

    @staticmethod
    def aggregate(results: dict) -> dict:
        """Deterministic aggregation summary; does not decide acceptance."""
        return {
            "total": len(results),
            "succeeded": sorted(k for k, r in results.items() if r.ok),
            "failed": sorted(k for k, r in results.items() if not r.ok),
        }
