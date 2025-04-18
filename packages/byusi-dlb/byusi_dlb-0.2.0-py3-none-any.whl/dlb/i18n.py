import json
import locale
from pathlib import Path
from typing import Dict
from .config import load_config

LOCALE_DIR = Path(__file__).parent / "locales"

TRANSLATIONS = {
    "en_US": {},
    "zh_CN": {}
}

def load_translations() -> Dict[str, str]:
    config = load_config()
    lang = config["language"]
    
    if lang == "auto":
        try:
            sys_lang, _ = locale.getdefaultlocale()
            lang = "zh_CN" if sys_lang and "zh" in sys_lang else "en_US"
        except:
            lang = "en_US"
    
    file_path = LOCALE_DIR / f"{lang}.json"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return {**TRANSLATIONS["en_US"], **json.load(f)}
    except:
        return TRANSLATIONS["en_US"]

def reload_translations():
    global _translations
    _translations = load_translations()

_translations = load_translations()

def _(text: str) -> str:
    return _translations.get(text, text)