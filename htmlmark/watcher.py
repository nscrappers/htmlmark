"""File watcher that triggers pipeline re-runs when source HTML files change."""

import os
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional


@dataclass
class WatchedFile:
    path: str
    last_mtime: float = 0.0
    callback: Optional[Callable[[str], None]] = None


@dataclass
class FileWatcher:
    interval: float = 1.0
    _watched: Dict[str, WatchedFile] = field(default_factory=dict)
    _running: bool = False

    def watch(self, path: str, callback: Callable[[str], None]) -> None:
        """Register a file path and callback to invoke on change."""
        mtime = _safe_mtime(path)
        self._watched[path] = WatchedFile(path=path, last_mtime=mtime, callback=callback)

    def unwatch(self, path: str) -> bool:
        """Remove a file from the watch list. Returns True if it existed."""
        if path in self._watched:
            del self._watched[path]
            return True
        return False

    def check_once(self) -> list:
        """Check all watched files for changes. Returns list of changed paths."""
        changed = []
        for path, entry in self._watched.items():
            current = _safe_mtime(path)
            if current != entry.last_mtime:
                entry.last_mtime = current
                changed.append(path)
                if entry.callback:
                    entry.callback(path)
        return changed

    def run_loop(self, iterations: Optional[int] = None) -> None:
        """Run the watch loop. If iterations is set, stop after that many cycles."""
        self._running = True
        count = 0
        while self._running:
            self.check_once()
            time.sleep(self.interval)
            count += 1
            if iterations is not None and count >= iterations:
                break
        self._running = False

    def stop(self) -> None:
        self._running = False

    @property
    def watched_paths(self) -> list:
        return list(self._watched.keys())


def _safe_mtime(path: str) -> float:
    """Return mtime of path, or 0.0 if file does not exist."""
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0
