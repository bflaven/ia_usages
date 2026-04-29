"""
Utility: load config.yaml and workflow_paths.yaml.
Single entry point for all config access.
"""

import os
import yaml
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = _PROJECT_ROOT / "config" / "config.yaml"
_PATHS_PATH = _PROJECT_ROOT / "config" / "workflow_paths.yaml"


def _load_dotenv() -> None:
    """Load .env from project root into os.environ if python-dotenv is available."""
    env_path = _PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path, override=False)  # override=False: shell env wins
    except ImportError:
        # python-dotenv not installed — read the file manually
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value


def load_config() -> dict:
    _load_dotenv()
    with open(_CONFIG_PATH) as f:
        return yaml.safe_load(f)


def load_paths() -> dict:
    with open(_PATHS_PATH) as f:
        return yaml.safe_load(f)


def get_corpus_dir(use_case: str = None) -> Path:
    cfg = load_config()
    paths = load_paths()
    uc = use_case or cfg["active_use_case"]
    return _PROJECT_ROOT / paths["use_cases"][uc]["corpus_dir"]


def get_index_dir(use_case: str = None) -> Path:
    cfg = load_config()
    paths = load_paths()
    uc = use_case or cfg["active_use_case"]
    return _PROJECT_ROOT / paths["use_cases"][uc]["index_dir"]


def get_checkpoint_dir(use_case: str = None) -> Path:
    cfg = load_config()
    paths = load_paths()
    uc = use_case or cfg["active_use_case"]
    return _PROJECT_ROOT / paths["use_cases"][uc]["checkpoint_dir"]


def get_logs_dir() -> Path:
    paths = load_paths()
    return _PROJECT_ROOT / paths["logs_dir"]
