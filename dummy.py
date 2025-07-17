"""file_placement_agent.py

Agent that scans a repository and detects files that are likely misplaced
according to common project-structure conventions (routes/, components/,
utils/, models/, etc.).  It combines:

1. Directory heuristics / static analysis (quick pre-filter).
2. LLM reasoning for nuanced judgement and suggestions.

It produces a structured JSON report with, for each inspected file:
- is_misplaced: bool
- suggested_path: Optional[str]
- reasoning: str
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import os
import json

from agent.code_debug_agent import CodeDebugAgent
from tools.git.git import GitRepository  # type: ignore

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover – runtime will install deps
    OpenAI = None  # type: ignore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Lightweight heuristics map folder keyword to human readable purpose
FOLDER_PURPOSE = {
    "routes": "API endpoints / route handlers",
    "controllers": "controller layer",
    "components": "UI pieces / frontend components",
    "views": "templated views",
    "utils": "utility helpers",
    "helpers": "utility helpers",
    "models": "data models / ORM schemas",
    "schemas": "data schemas",
    "services": "business-logic services",
}

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")

class FilePlacementAgent:
    """High-level facade class."""

    def __init__(self, *, repo_url: str | None = None, repo_path: str | None = None, branch: str = "main", openai_api_key: str | None = None):
        if not repo_url and not repo_path:
            raise ValueError("repo_url or repo_path required")

        self._temp_git: GitRepository | None = None
        if repo_url:
            # clone via GitRepository into tmp dir
            self._temp_git = GitRepository(repo_url, branch=branch)
            self._temp_git.clone()
            repo_path = self._temp_git.temp_dir

        self.repo_root = Path(repo_path).resolve()
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise EnvironmentError("OPENAI_API_KEY not provided")
        if OpenAI is None:
            raise RuntimeError("openai package not installed")

        self.client = OpenAI(api_key=self.openai_api_key)

        logger.info("FilePlacementAgent ready for repo %s", self.repo_root)

    # ------------------------------------------------------------------
    def run(self, *, max_files: int = 500, include_hidden: bool = False, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
        """Scan repository and return placement report."""
        cd_agent = CodeDebugAgent(repo_path=str(self.repo_root))
        data = cd_agent.traverse(max_size_bytes=100_000, include_binary=False, include_hidden=include_hidden)
        files = data["files"][:max_files]

        results: List[Dict[str, Any]] = []
        for record in files:
            path = record["path"]
            content = record["content"]
            if isinstance(content, bytes):  # skip binary here
                continue
            suspected = self._simple_heuristic(path, content)
            analysis = self._ask_llm(path, content, suspected, model)
            results.append(analysis)

        # Prepare the report for the API consumer. Trim container-specific prefixes
        # (e.g. "/app/") so that only the actual repo directory name is returned and
        # omit internal fields like the LLM model that are not relevant for the end user.
        repository_root_clean = Path(self.repo_root).name  # e.g. "repo"
        report = {
            "repository_root": repository_root_clean,
            "files_checked": len(results),
            "misplaced_count": sum(1 for r in results if r["is_misplaced"]),
            "details": results,
        }
        return report

    # ------------------------------------------------------------------
    def _simple_heuristic(self, file_path: str, content: str) -> str | None:
        """Return a possible better folder suggestion based on basic checks."""
        lower = content.lower()
        fname = Path(file_path)
        parent = fname.parts[0] if len(fname.parts) > 1 else ""

        # Very naive heuristics
        if "react" in lower or "jsx" in lower or "component" in lower:
            if parent != "components":
                return "components/"
        if "schema" in lower or "model" in lower and parent != "models":
            return "models/"
        if any(k in lower for k in ("helper", "util")) and parent != "utils":
            return "utils/"
        return None

    # ------------------------------------------------------------------
    def _ask_llm(self, file_path: str, file_content: str, heuristic: str | None, model: str) -> Dict[str, Any]:
        prompt = f"""
You are an experienced software architect. Analyse whether a source file is placed in the correct folder of a repository.

Folder conventions include:
{json.dumps(FOLDER_PURPOSE, indent=2)}

FILE PATH: {file_path}
FILE CONTENT (truncated to 8000 chars):
```
{file_content[:8000]}
```
{f'Heuristic suggests maybe {heuristic}' if heuristic else ''}

Answer in JSON with keys is_misplaced (boolean), suggested_path (string or null), reasoning (short).
"""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=400,
        )
        try:
            j = json.loads(completion.choices[0].message.content)
        except Exception:
            # fallback to plain string
            j = {
                "is_misplaced": False,
                "suggested_path": None,
                "reasoning": completion.choices[0].message.content.strip()[:1000],
            }
        j["file_path"] = file_path
        return j

    # ------------------------------------------------------------------
    def __del__(self):
        if self._temp_git is not None:
            try:
                self._temp_git.cleanup()
            except Exception:
                pass
