"""
NotebookLM CLI integration for DYT_01.

Install the CLI first:
    pip install notebooklm-cli

The expected command is `nlm`, not `notebooklm`.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import site
import subprocess
import sys
import sysconfig
from pathlib import Path


DEFAULT_NOTEBOOK_URL = "https://notebooklm.google.com/notebook/5e64f86d-3f1b-44bd-a5c0-067fd839e3a5"
DEFAULT_NOTEBOOK_ID = "5e64f86d-3f1b-44bd-a5c0-067fd839e3a5"
PROJECT_ROOT = Path(__file__).resolve().parent
NOTEBOOK_SOURCE_FILE = PROJECT_ROOT / "notebooklm_export.md"


def resolve_nlm_command() -> str | None:
    """Find nlm even when the Python user Scripts directory is not in PATH."""
    configured = os.getenv("NOTEBOOKLM_CLI")
    candidates = [configured, shutil.which("nlm")]

    user_base = Path(site.USER_BASE)
    if sys.platform == "win32":
        candidates.append(str(user_base / "Scripts" / "nlm.exe"))
        user_scripts = sysconfig.get_path("scripts", scheme="nt_user")
        if user_scripts:
            candidates.append(str(Path(user_scripts) / "nlm.exe"))
    else:
        candidates.append(str(user_base / "bin" / "nlm"))
        user_scripts = sysconfig.get_path("scripts", scheme="posix_user")
        if user_scripts:
            candidates.append(str(Path(user_scripts) / "nlm"))

    for candidate in candidates:
        if not candidate:
            continue
        try:
            if Path(candidate).exists():
                return candidate
        except PermissionError:
            return candidate
    return shutil.which("nlm")


def extract_notebook_id(value: str | None) -> str | None:
    """Return a NotebookLM notebook id from either a raw id or notebook URL."""
    if not value:
        return None
    match = re.search(r"/notebook/([0-9a-fA-F-]+)", value)
    if match:
        return match.group(1)
    if re.fullmatch(r"[0-9a-fA-F-]{36}", value):
        return value
    return None


def safe_print(value: object = "") -> None:
    """Print safely on legacy Windows consoles."""
    text = str(value)
    try:
        print(text)
    except UnicodeEncodeError:
        encoded = text.encode(sys.stdout.encoding or "utf-8", errors="backslashreplace")
        print(encoded.decode(sys.stdout.encoding or "utf-8", errors="replace"))


class NotebookLMClient:
    def __init__(self, notebook: str | None = None):
        configured = notebook or os.getenv("NOTEBOOKLM_NOTEBOOK") or DEFAULT_NOTEBOOK_URL
        self.current_notebook = extract_notebook_id(configured)
        self.nlm_command = resolve_nlm_command()

    def is_installed(self) -> bool:
        return self.nlm_command is not None

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        if not self.nlm_command:
            raise RuntimeError("NotebookLM CLI command `nlm` is not installed")
        env = os.environ.copy()
        env.setdefault("PYTHONUTF8", "1")
        env.setdefault("PYTHONIOENCODING", "utf-8")
        env.setdefault("NO_COLOR", "1")
        return subprocess.run(
            [self.nlm_command, *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

    def login(self) -> bool:
        """Open browser login through the NotebookLM CLI."""
        if not self.is_installed():
            safe_print("ERROR: NotebookLM CLI is not installed. Run: .\\setup_notebooklm_cli.ps1")
            return False

        safe_print("Opening browser login for NotebookLM...")
        result = self._run(["login"])
        if result.returncode == 0:
            safe_print("NotebookLM login completed.")
            return True

        safe_print(f"ERROR: Login failed: {result.stderr or result.stdout}")
        return False

    def auth_status(self) -> bool:
        """Return True when nlm reports a valid auth session."""
        if not self.is_installed():
            safe_print("ERROR: NotebookLM CLI is not installed.")
            return False

        result = self._run(["auth", "status"])
        output = (result.stdout or result.stderr).strip()
        safe_print(output)
        if result.returncode == 0:
            return True
        # nlm 0.1.12 can validate successfully on legacy Windows consoles and
        # then fail while printing a Unicode check mark via Rich.
        success_markers = ("Authenticated", "Validating credentials for profile")
        return any(marker in output for marker in success_markers)

    def list_notebooks(self) -> dict[str, str]:
        """List notebooks as a title -> id mapping."""
        if not self.is_installed():
            safe_print("ERROR: NotebookLM CLI is not installed.")
            return {}

        result = self._run(["notebook", "list", "--json"])
        if result.returncode != 0:
            safe_print(f"ERROR: Cannot read notebook list: {result.stderr or result.stdout}")
            return {}

        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            safe_print(result.stdout)
            return {}

        notebooks = payload.get("notebooks", payload if isinstance(payload, list) else [])
        notebook_dict: dict[str, str] = {}
        for notebook in notebooks:
            notebook_id = notebook.get("id", "")
            title = notebook.get("title", notebook.get("name", "Untitled"))
            if notebook_id:
                notebook_dict[title] = notebook_id
                safe_print(f"{title}: {notebook_id}")
        return notebook_dict

    def use_notebook(self, notebook: str) -> bool:
        notebook_id = extract_notebook_id(notebook)
        if not notebook_id:
            safe_print(f"ERROR: Invalid notebook ID/URL: {notebook}")
            return False
        self.current_notebook = notebook_id
        safe_print(f"Using notebook: {notebook_id}")
        return True

    def add_text(self, text: str, title: str = "DYT_01 Project Context") -> bool:
        if not self.current_notebook:
            safe_print("ERROR: No notebook selected.")
            return False

        result = self._run(
            ["source", "add", self.current_notebook, "--text", text, "--title", title]
        )
        if result.returncode == 0:
            safe_print(f"Added text source: {title}")
            return True

        safe_print(f"ERROR: Failed to add text source: {result.stderr or result.stdout}")
        return False

    def add_url(self, url: str) -> bool:
        if not self.current_notebook:
            safe_print("ERROR: No notebook selected.")
            return False

        result = self._run(["source", "add", self.current_notebook, "--url", url])
        if result.returncode == 0:
            safe_print(f"Added URL: {url}")
            return True

        safe_print(f"ERROR: Failed to add URL: {result.stderr or result.stdout}")
        return False

    def sync_project_context(self) -> bool:
        """Upload the current local project context markdown into NotebookLM."""
        if not NOTEBOOK_SOURCE_FILE.exists():
            safe_print("notebooklm_export.md is missing; regenerating it...")
            subprocess.run(["python", str(PROJECT_ROOT / "update_notebooklm.py")], check=True)

        content = NOTEBOOK_SOURCE_FILE.read_text(encoding="utf-8")
        return self.add_text(content, "DYT_01 Project Context")


def quick_connect() -> str | None:
    client = NotebookLMClient()

    safe_print("=" * 60)
    safe_print("NOTEBOOKLM CLI CONNECT")
    safe_print("=" * 60)

    if not client.is_installed():
        safe_print("ERROR: Command `nlm` is not available.")
        safe_print("Run: .\\setup_notebooklm_cli.ps1")
        return None

    if not client.auth_status():
        safe_print("NotebookLM auth is missing or expired.")
        if not client.login():
            return None

    safe_print(f"Notebook target: {client.current_notebook}")
    if not client.sync_project_context():
        return None

    safe_print("=" * 60)
    safe_print(f"Notebook URL: https://notebooklm.google.com/notebook/{client.current_notebook}")
    safe_print("=" * 60)
    return client.current_notebook


if __name__ == "__main__":
    quick_connect()
