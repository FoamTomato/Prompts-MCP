from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    skills_root: Path
    port: int
    base_url_prefix: str
    log_level: str

    @classmethod
    def from_env(cls) -> Settings:
        skills_root = Path(os.environ.get("SKILLS_ROOT", "./skills")).resolve()
        port = int(os.environ.get("PORT", "8080"))
        base_url_prefix = os.environ.get("BASE_URL_PREFIX", "").rstrip("/")
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        return cls(
            skills_root=skills_root,
            port=port,
            base_url_prefix=base_url_prefix,
            log_level=log_level,
        )
