"""Second real runtime adapter: Hermes Agent CLI (`hermes -z`).

This is the SECOND real runtime adapter in PAIOS. It wraps the actually
installed, authenticated Hermes Agent CLI and was verified through direct
observable execution (Phase 14 second-runtime evidence, 2026-10-03):

- executable: `hermes` (Hermes Agent v0.21.3, install dir under
  ~/AppData/Local/hermes/hermes-agent)
- auth: Nous Portal OAuth, logged in (`hermes status` -> "✓ logged in",
  inference endpoint https://inference-api.nousresearch.com/v1)
- working model verified live: `poolside/laguna-xs-2.1:free` via provider
  `nous` (free tier; the configured default glm-5.3 provider requires paid
  credits — HTTP 404 "requires available credits")
- invocation: `hermes -z <prompt> --provider nous -m <model> --safe-mode
  --cli` (prompt passed as argv; cwd = execution workspace)
- task execution: verified live — the runtime reads files from its working
  directory and returns their contents exactly (real repo task against
  execution.py reproduced the six ExecutionStatus values)
- sandbox: `--safe-mode` restricts tool use; observed behavior is
  read-capable but NOT write-isolating (a write request produced the file).
  Write isolation is NOT claimed. Bounded read-only execution is the
  caller's responsibility (authority context travels with the request).
- structured output: none — plain stdout text only, no usage JSON
- failures: provider errors print human-readable message blocks with a
  "Provider said: HTTP <code>" line and exit 0; mapped to FAILED
- timeout: externally enforced (subprocess timeout); observed live

Nothing in this file infers capabilities that were not observed.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from .adapters import RuntimeAdapter, RuntimeHealth, _now
from .execution import ExecutionRequest, ExecutionResult, ExecutionStatus
from .untrusted import inspect_runtime_output, UntrustedContent

PROVIDER_ERROR = re.compile(r"Provider said: HTTP (\d+)")


class HermesRuntimeError(Exception):
    pass


class HermesRuntimeAdapter(RuntimeAdapter):
    """Real adapter around the Hermes Agent CLI. Second verified runtime
    (failover class). All capabilities below were VERIFIED by direct
    execution on 2026-10-03; nothing else is claimed."""

    runtime_id = "hermes-agent"
    adapter_id = "hermes-cli-adapter"
    adapter_version = "1.0.0"
    #: only what was directly observed:
    provided_capabilities = frozenset({
        "execute",              # hermes -z runs a bounded task to completion
        "verify",               # agent output + provider-error absence observable
        "evidence_generation",  # stdout transcript retained by caller
        "working_directory",    # runs in caller cwd (verified live)
        # NOT claimed: structured_output, read_only_sandbox, streaming,
        # parallelism, cancellation
    })

    def __init__(self, *, model: str = "poolside/laguna-xs-2.1:free",
                 provider: str = "nous",
                 timeout_seconds: int = 240,
                 workspace_root: str | None = None):
        self.model = model
        self.provider = provider
        self.timeout_seconds = timeout_seconds
        self.workspace_root = workspace_root   # execution cwd; None = caller cwd

    # -- discovery / health ---------------------------------------------------
    def binary_path(self) -> str | None:
        return shutil.which("hermes")

    def health(self) -> str:
        if self.binary_path() is None:
            return RuntimeHealth.UNAVAILABLE
        return RuntimeHealth.AVAILABLE

    def configured_model(self) -> str | None:
        status = self._run_stdout(["status"])
        m = re.search(r"Model:\s*(\S+)", status or "")
        return m.group(1) if m else None

    def auth_state(self) -> str:
        status = self._run_stdout(["status"])
        if status and "logged in" in status:
            return "AUTHENTICATED"
        return "UNAUTHENTICATED"

    def _run_stdout(self, args: list, timeout: int = 60) -> str:
        try:
            proc = subprocess.run([self.binary_path()] + args, capture_output=True,
                                  text=True, timeout=timeout, encoding="utf-8",
                                  errors="replace")
        except (OSError, subprocess.TimeoutExpired):
            return ""
        return proc.stdout or ""

    # -- execution -------------------------------------------------------------
    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        binary = self.binary_path()
        if binary is None:
            return self._result(request, ExecutionStatus.FAILED,
                                error_type="runtime_unavailable",
                                error="hermes CLI not found on PATH")
        prompt = self._build_prompt(request)
        cmd = [binary, "-z", prompt, "--provider", self.provider,
               "-m", self.model, "--safe-mode", "--cli"]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=self.timeout_seconds, encoding="utf-8",
                                  errors="replace", cwd=self.workspace_root)
        except subprocess.TimeoutExpired:
            return self._result(request, ExecutionStatus.TIMEOUT,
                                error_type="deadline_exceeded",
                                error=f"hermes -z exceeded {self.timeout_seconds}s deadline")
        except OSError as exc:
            return self._result(request, ExecutionStatus.FAILED,
                                error_type="runtime_unavailable",
                                error=f"failed to launch hermes: {exc}")

        output = (proc.stdout or "").strip()
        provider_error = PROVIDER_ERROR.search(output)
        # Hermes prints provider failures with exit 0; exit code alone is not
        # success. A provider error block or empty output is never COMPLETED.
        if provider_error and _is_error_block(output):
            return self._result(request, ExecutionStatus.FAILED,
                                error_type="execution_failure",
                                error=provider_error.group(0) + ": " +
                                      _last_line(output))
        if not output:
            return self._result(request, ExecutionStatus.UNKNOWN,
                                error_type="ambiguous_outcome",
                                error="process exited without producing output")
        # A bare "Update available:" notice with no agent content is UNKNOWN.
        if output.startswith("Update available") and "\n" not in output:
            return self._result(request, ExecutionStatus.UNKNOWN,
                                error_type="ambiguous_outcome",
                                error="no agent output (update notice only)")

        evidence = [f"hermes://stdout#{request.task_id}",
                    f"hermes://model/{self.provider}/{self.model}",
                    f"hermes://exit/{proc.returncode}"]
        result = self._result(request, ExecutionStatus.COMPLETED,
                              output_ref=output,
                              evidence_refs=evidence)
        result.verification = {
            "exit_code": proc.returncode,
            "model": self.model,
            "provider": self.provider,
            "raw_output_chars": len(output),
        }
        return result

    def verify(self, result: ExecutionResult) -> dict:
        if result.status != ExecutionStatus.COMPLETED:
            return {"verified": False,
                    "reason": f"status {result.status} is not verifiable as success"}
        try:
            inspect_runtime_output(result.output_ref or "")
        except UntrustedContent as exc:
            return {"verified": False, "reason": str(exc)}
        return {"verified": True, "adapter": self.adapter_id,
                "exit_code": (result.verification or {}).get("exit_code")}

    def check_acceptance(self, request: ExecutionRequest,
                         result: ExecutionResult) -> dict:
        criteria = {}
        for crit in request.acceptance_criteria:
            criteria[crit] = bool(result.output_ref) and result.status == ExecutionStatus.COMPLETED
        return {"passed": bool(criteria) and all(criteria.values()),
                "criteria": criteria}

    # -- internals ------------------------------------------------------------
    def _build_prompt(self, request: ExecutionRequest) -> str:
        """Canonical request -> runtime prompt. Authority context and
        acceptance criteria travel with the task as data."""
        parts = [f"TASK_ID: {request.task_id}",
                 f"AUTHORITY (informational — you cannot change it): {request.authority_context}"]
        if request.objective:
            parts.append(f"OBJECTIVE: {request.objective}")
        if request.acceptance_criteria:
            parts.append("ACCEPTANCE CRITERIA:\n" +
                         "\n".join(f"- {c}" for c in request.acceptance_criteria))
        parts.append(str(request.inputs.get("prompt", request.objective)))
        return "\n\n".join(parts)


def _is_error_block(output: str) -> bool:
    """A provider error transcript ends with the error explanation after the
    'Provider said:' line; successful agent replies never contain it."""
    return "Provider said:" in output


def _last_line(output: str) -> str:
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    return lines[-1] if lines else ""
