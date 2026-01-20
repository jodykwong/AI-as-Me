"""Event tracker and logger."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import threading
import atexit


class EventTracker:
    """Track and log events in JSON Lines format."""

    def __init__(self, logs_dir: Path, buffer_size: int = 10):
        """Initialize event tracker.

        Args:
            logs_dir: Directory for log files
            buffer_size: Number of entries to buffer before writing
        """
        self.logs_dir = logs_dir
        self.logs_dir.mkdir(exist_ok=True)

        # Current log file
        self.log_file = logs_dir / f"events-{datetime.now().strftime('%Y%m%d')}.jsonl"
        self._lock = threading.Lock()
        self._buffer: List[str] = []
        self._buffer_size = buffer_size

        # Flush buffer on exit
        atexit.register(self._flush)

    def _flush(self) -> None:
        """Flush buffer to file."""
        with self._lock:
            if self._buffer:
                with open(self.log_file, "a") as f:
                    f.write("\n".join(self._buffer) + "\n")
                self._buffer.clear()

    def log(
        self, level: str, module: str, event: str, data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log an event.

        Args:
            level: Log level (info, warning, error)
            module: Module name
            event: Event name
            data: Additional event data
        """
        entry = {
            "ts": datetime.now().isoformat(),
            "level": level,
            "module": module,
            "event": event,
        }

        if data:
            entry["data"] = data

        # Buffer entries (thread-safe)
        with self._lock:
            self._buffer.append(json.dumps(entry))
            if len(self._buffer) >= self._buffer_size:
                self._flush()

    def info(self, module: str, event: str, data: Optional[Dict[str, Any]] = None):
        """Log info event."""
        self.log("info", module, event, data)

    def warning(self, module: str, event: str, data: Optional[Dict[str, Any]] = None):
        """Log warning event."""
        self.log("warning", module, event, data)

    def error(self, module: str, event: str, data: Optional[Dict[str, Any]] = None):
        """Log error event."""
        self.log("error", module, event, data)

    def rotate_if_needed(self, max_size_mb: int = 10):
        """Rotate log file if it exceeds max size.

        Args:
            max_size_mb: Maximum file size in MB
        """
        if not self.log_file.exists():
            return

        size_mb = self.log_file.stat().st_size / (1024 * 1024)

        if size_mb > max_size_mb:
            # Rotate: rename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            rotated = self.log_file.with_suffix(f".{timestamp}.jsonl")
            self.log_file.rename(rotated)

            # Create new log file
            self.log_file = (
                self.logs_dir / f"events-{datetime.now().strftime('%Y%m%d')}.jsonl"
            )

    def cleanup_old_logs(self, days: int = 7):
        """Delete logs older than specified days.

        Args:
            days: Number of days to keep
        """
        cutoff = datetime.now().timestamp() - (days * 86400)

        for log_file in self.logs_dir.glob("*.jsonl"):
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
