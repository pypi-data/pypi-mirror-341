import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from rich.progress import Progress
from typing import List, Tuple

from .config import load_config
from .i18n import _

def create_placeholder(path: str):
    config = load_config()
    if config["placeholder"]:
        try:
            Path(path).touch(exist_ok=True)
        except Exception as e:
            print(_("error").format(f"Create placeholder failed: {str(e)}"))

def download_single(url: str, path: str, progress: Progress, task_id: int):
    create_placeholder(path)
    config = load_config()
    
    headers = {}
    if config["cookies"]:
        headers["Cookie"] = config["cookies"]
    
    try:
        response = requests.get(
            url,
            stream=True,
            headers=headers,
            timeout=config["timeout"]
        )
        response.raise_for_status()
        
        total_size = int(response.headers.get("content-length", 0))
        progress.update(task_id, total=total_size, description=_("downloading").format(os.path.basename(path)))
        
        downloaded = 0
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress.update(task_id, advance=len(chunk))
        
        progress.update(task_id, description=_("complete").format(os.path.basename(path)))
    except Exception as e:
        progress.update(task_id, description=_("error").format(str(e)))
        if Path(path).exists():
            Path(path).unlink()

def download_manager(urls: List[Tuple[str, str]], max_workers: int = None):
    config = load_config()
    max_workers = max_workers or config["max_workers"]
    max_workers = min(max_workers, config["max_downloads"])
    
    with Progress() as progress:
        tasks = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for url, path in urls:
                task_id = progress.add_task("", total=None)
                future = executor.submit(
                    download_single,
                    url,
                    path,
                    progress,
                    task_id
                )
                futures.append(future)
                tasks[future] = task_id
            
            for future in as_completed(futures):
                task_id = tasks[future]
                try:
                    future.result()
                except Exception as e:
                    progress.update(task_id, description=_("error").format(str(e)))