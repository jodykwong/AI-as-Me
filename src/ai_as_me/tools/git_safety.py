"""Git safety net for code modifications."""
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional


class GitSafetyNet:
    """Auto-backup before code changes, rollback on failure."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self._backup_commit: Optional[str] = None
    
    def _run_git(self, *args) -> tuple[bool, str]:
        """Run git command."""
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout.strip()
        except Exception as e:
            return False, str(e)
    
    def is_repo(self) -> bool:
        """Check if path is a git repo."""
        return (self.repo_path / ".git").exists()
    
    def backup(self, message: str = None) -> bool:
        """Create backup commit before changes.
        
        Returns:
            True if backup created
        """
        if not self.is_repo():
            return False
        
        # Get current HEAD
        ok, head = self._run_git("rev-parse", "HEAD")
        if ok:
            self._backup_commit = head
        
        # Stage and commit any pending changes
        self._run_git("add", "-A")
        
        msg = message or f"[AI-as-Me backup] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ok, _ = self._run_git("commit", "-m", msg, "--allow-empty")
        
        return True
    
    def rollback(self) -> bool:
        """Rollback to backup point.
        
        Returns:
            True if rollback successful
        """
        if not self._backup_commit:
            return False
        
        ok, _ = self._run_git("reset", "--hard", self._backup_commit)
        return ok
    
    def get_diff(self) -> str:
        """Get diff since backup."""
        if not self._backup_commit:
            return ""
        
        ok, diff = self._run_git("diff", self._backup_commit, "HEAD")
        return diff if ok else ""


class SafeFileWriter:
    """Context manager for safe file modifications."""
    
    def __init__(self, repo_path: Path, backup_msg: str = None):
        self.git = GitSafetyNet(repo_path)
        self.backup_msg = backup_msg
        self._success = False
    
    def __enter__(self):
        self.git.backup(self.backup_msg)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Error occurred, rollback
            print(f"⚠️ Error detected, rolling back: {exc_val}")
            self.git.rollback()
            return False
        return True
    
    def mark_success(self):
        """Mark operation as successful (no rollback needed)."""
        self._success = True


if __name__ == "__main__":
    # Test
    git = GitSafetyNet(Path.cwd())
    print(f"Is repo: {git.is_repo()}")
