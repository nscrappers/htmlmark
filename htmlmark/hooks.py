"""Lightweight hook/event system for profiling and observability."""

from typing import Callable, Dict, List, Any


_registry: Dict[str, List[Callable]] = {}


def register(event: str, callback: Callable) -> None:
    """Register a callback for the given event name."""
    _registry.setdefault(event, []).append(callback)


def unregister(event: str, callback: Callable) -> None:
    """Remove a previously registered callback."""
    if event in _registry:
        try:
            _registry[event].remove(callback)
        except ValueError:
            pass


def emit(event: str, payload: Any = None) -> None:
    """Invoke all callbacks registered for the given event."""
    for cb in _registry.get(event, []):
        cb(payload)


def clear(event: str = None) -> None:
    """Clear callbacks for a specific event, or all events if None."""
    if event is None:
        _registry.clear()
    else:
        _registry.pop(event, None)


def registered_events() -> List[str]:
    """Return a list of event names that have at least one listener."""
    return [e for e, cbs in _registry.items() if cbs]


# Built-in event names used by profile_runner
EVENT_PIPELINE_START = "pipeline:start"
EVENT_PIPELINE_END = "pipeline:end"
EVENT_STEP_START = "step:start"
EVENT_STEP_END = "step:end"
