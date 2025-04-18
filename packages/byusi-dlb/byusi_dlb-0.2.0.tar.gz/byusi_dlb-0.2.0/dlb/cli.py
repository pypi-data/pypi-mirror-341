import argparse
import os
from typing import List

from .core import download_manager
from .config import load_config, save_config
from .i18n import _, reload_translations

def parse_urls(urls: List[str], output_dir: str) -> List[Tuple[str, str]]:
    return [
        (url, os.path.join(output_dir, os.path.basename(url)))
        for url in urls
    ]

def main():
    reload_translations()
    config = load_config()
    
    parser = argparse.ArgumentParser(
        description=_("cli_description"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "urls",
        nargs="+",
        help=_("urls_help")
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        help=_("output_help")
    )
    parser.add_argument(
        "-j",
        type=int,
        default=config["max_workers"],
        help=_("threads_help")
    )
    parser.add_argument(
        "--cookie",
        help=_("cookie_help")
    )
    parser.add_argument(
        "--set-config",
        action="store_true",
        help=_("set_config_help")
    )
    
    args = parser.parse_args()
    
    if args.set_config:
        new_config = {
            "max_workers": args.j,
            "cookies": args.cookie or config["cookies"],
            "language": config["language"]
        }
        save_config(new_config)
        print(_("config_saved"))
        return
    
    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)
    
    url_path_list = parse_urls(args.urls, args.output)
    download_manager(url_path_list, args.j)

if __name__ == "__main__":
    main()