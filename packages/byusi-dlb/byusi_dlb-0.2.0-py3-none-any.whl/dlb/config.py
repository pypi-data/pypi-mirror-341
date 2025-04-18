import os
import json
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    "language": "auto",
    "max_workers": 5,
    "max_downloads": 10,
    "cookies": "",
    "placeholder": False,
    "timeout": 30
}

def get_config_path() -> Path:
    return Path.home() / ".dlb.json"

def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    valid_config = DEFAULT_CONFIG.copy()
    
    if isinstance(config.get("max_workers"), int):
        valid_config["max_workers"] = max(1, config["max_workers"])
    
    if isinstance(config.get("max_downloads"), int):
        valid_config["max_downloads"] = max(1, config["max_downloads"])
    
    valid_config["cookies"] = str(config.get("cookies", ""))
    valid_config["placeholder"] = bool(config.get("placeholder"))
    valid_config["timeout"] = max(1, int(config.get("timeout", 30)))
    
    if config.get("language") in ["auto", "en_US", "zh_CN"]:
        valid_config["language"] = config["language"]
    
    return valid_config

def load_config() -> Dict[str, Any]:
    config_path = get_config_path()
    
    if not config_path.exists():
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            return validate_config(user_config)
    except Exception as e:
        print(f"Config load error: {str(e)}")
        return DEFAULT_CONFIG

def save_config(config: Dict[str, Any]):
    config_path = get_config_path()
    validated = validate_config(config)
    
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(validated, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Config save error: {str(e)}")