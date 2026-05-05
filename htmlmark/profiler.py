"""Profiling utilities for measuring extraction and pipeline performance."""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class StepTiming:
    name: str
    elapsed_ms: float


@dataclass
class ProfileReport:
    label: str
    steps: List[StepTiming] = field(default_factory=list)
    total_ms: float = 0.0

    def add_step(self, name: str, elapsed_ms: float) -> None:
        self.steps.append(StepTiming(name=name, elapsed_ms=elapsed_ms))
        self.total_ms += elapsed_ms

    def slowest_step(self) -> Optional[StepTiming]:
        if not self.steps:
            return None
        return max(self.steps, key=lambda s: s.elapsed_ms)

    def to_dict(self) -> Dict:
        return {
            "label": self.label,
            "total_ms": round(self.total_ms, 4),
            "steps": [
                {"name": s.name, "elapsed_ms": round(s.elapsed_ms, 4)}
                for s in self.steps
            ],
        }


class Profiler:
    """Context-manager-based step profiler."""

    def __init__(self, label: str) -> None:
        self.report = ProfileReport(label=label)
        self._step_name: Optional[str] = None
        self._step_start: Optional[float] = None

    def start_step(self, name: str) -> None:
        self._step_name = name
        self._step_start = time.perf_counter()

    def end_step(self) -> None:
        if self._step_name is None or self._step_start is None:
            raise RuntimeError("end_step called without a matching start_step")
        elapsed = (time.perf_counter() - self._step_start) * 1000
        self.report.add_step(self._step_name, elapsed)
        self._step_name = None
        self._step_start = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self._step_name is not None:
            self.end_step()
