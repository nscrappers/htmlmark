"""Scheduled extraction jobs: run pipeline tasks at timed intervals."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class Job:
    name: str
    task: Callable[[], None]
    interval_seconds: float
    _last_run: float = field(default=0.0, init=False, repr=False)

    def is_due(self, now: Optional[float] = None) -> bool:
        now = now if now is not None else time.monotonic()
        return (now - self._last_run) >= self.interval_seconds

    def run(self, now: Optional[float] = None) -> None:
        self.task()
        self._last_run = now if now is not None else time.monotonic()


@dataclass
class Scheduler:
    _jobs: List[Job] = field(default_factory=list)

    def register(self, name: str, task: Callable[[], None], interval_seconds: float) -> Job:
        """Register a new job. Replaces any existing job with the same name."""
        self._jobs = [j for j in self._jobs if j.name != name]
        job = Job(name=name, task=task, interval_seconds=interval_seconds)
        self._jobs.append(job)
        return job

    def unregister(self, name: str) -> bool:
        before = len(self._jobs)
        self._jobs = [j for j in self._jobs if j.name != name]
        return len(self._jobs) < before

    def tick(self, now: Optional[float] = None) -> List[str]:
        """Run all due jobs and return their names."""
        now = now if now is not None else time.monotonic()
        ran: List[str] = []
        for job in self._jobs:
            if job.is_due(now):
                job.run(now)
                ran.append(job.name)
        return ran

    def job_names(self) -> List[str]:
        return [j.name for j in self._jobs]

    def clear(self) -> None:
        self._jobs.clear()

    def __len__(self) -> int:
        return len(self._jobs)
