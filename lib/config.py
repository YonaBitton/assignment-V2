from __future__ import annotations

from typing import Any, Dict

import yaml

from lib.paths import PROJECT_ROOT


def load_config(config_name: str = "base") -> Dict[str, Any]:
    """Charge un fichier de configuration YAML.

    Args:
        config_name: Nom du fichier (sans extension). Par défaut "base".

    Returns:
        Dictionnaire contenant la configuration.

    Raises:
        FileNotFoundError: Si le fichier de config n'existe pas.
    """
    config_path = PROJECT_ROOT / "configs" / f"{config_name}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {config_path}")

    with open(config_path, encoding="utf-8") as f:
        config: Dict[str, Any] = yaml.safe_load(f)

    return config


def get_config() -> Dict[str, Any]:
    """Retourne la configuration par défaut (singleton pattern simplifié)."""
    return load_config("base")
