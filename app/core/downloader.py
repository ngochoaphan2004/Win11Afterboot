"""
Downloader - Tải file với theo dõi tiến trình, hỗ trợ multi-threading
"""

import os
import threading
import requests
import time
from pathlib import Path
from typing import Callable, Optional


DOWNLOAD_DIR = Path.home() / "Downloads" / "Win11AfterBoot"


def get_download_dir() -> Path:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return DOWNLOAD_DIR


class DownloadTask:
    """Đại diện cho một tác vụ tải file"""

    def __init__(
        self,
        app_id: str,
        name: str,
        url: str,
        filename: str,
        on_progress: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ):
        self.app_id = app_id
        self.name = name
        self.url = url
        self.filename = filename
        self.on_progress = on_progress
        self.on_complete = on_complete
        self.on_error = on_error

        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.speed_bps = 0
        self.status = "pending"  # pending, downloading, completed, error, cancelled
        self._thread: Optional[threading.Thread] = None
        self._cancel_event = threading.Event()
        self.file_path: Optional[Path] = None

    def start(self):
        self._thread = threading.Thread(target=self._download, daemon=True)
        self._thread.start()

    def cancel(self):
        self._cancel_event.set()
        self.status = "cancelled"

    def _download(self):
        self.status = "downloading"
        download_dir = get_download_dir()
        self.file_path = download_dir / self.filename

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            with requests.get(self.url, stream=True, headers=headers, timeout=30, allow_redirects=True) as r:
                r.raise_for_status()

                # Lấy kích thước file
                content_length = r.headers.get("content-length")
                self.total_bytes = int(content_length) if content_length else 0

                # Lấy tên file từ Content-Disposition nếu có
                content_disposition = r.headers.get("content-disposition", "")
                if "filename=" in content_disposition:
                    fname = content_disposition.split("filename=")[-1].strip('"').strip("'")
                    if fname:
                        self.file_path = download_dir / fname

                with open(self.file_path, "wb") as f:
                    start_time = time.time()
                    last_update_time = start_time
                    last_bytes = 0

                    for chunk in r.iter_content(chunk_size=65536):
                        if self._cancel_event.is_set():
                            return

                        if chunk:
                            f.write(chunk)
                            self.downloaded_bytes += len(chunk)

                            # Tính tốc độ tải mỗi 0.5 giây
                            now = time.time()
                            if now - last_update_time >= 0.5:
                                elapsed = now - last_update_time
                                bytes_in_interval = self.downloaded_bytes - last_bytes
                                self.speed_bps = bytes_in_interval / elapsed
                                last_update_time = now
                                last_bytes = self.downloaded_bytes

                            # Callback progress
                            if self.on_progress:
                                progress = (
                                    self.downloaded_bytes / self.total_bytes
                                    if self.total_bytes > 0
                                    else 0
                                )
                                self.on_progress(
                                    self.app_id,
                                    progress,
                                    self.downloaded_bytes,
                                    self.total_bytes,
                                    self.speed_bps,
                                )

            self.status = "completed"
            if self.on_complete:
                self.on_complete(self.app_id, self.file_path)

        except requests.exceptions.RequestException as e:
            self.status = "error"
            if self.on_error:
                self.on_error(self.app_id, str(e))
        except Exception as e:
            self.status = "error"
            if self.on_error:
                self.on_error(self.app_id, f"Lỗi không xác định: {str(e)}")


class DownloadManager:
    """Quản lý nhiều tác vụ tải file đồng thời"""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.tasks: dict[str, DownloadTask] = {}
        self._lock = threading.Lock()

    def add_task(self, task: DownloadTask):
        with self._lock:
            self.tasks[task.app_id] = task

    def start_all(self):
        """Bắt đầu tải tất cả task theo batch"""
        pending = [t for t in self.tasks.values() if t.status == "pending"]

        # Tải theo nhóm max_concurrent
        semaphore = threading.Semaphore(self.max_concurrent)

        def run_with_semaphore(task: DownloadTask):
            semaphore.acquire()
            try:
                task._download()
            finally:
                semaphore.release()

        threads = []
        for task in pending:
            t = threading.Thread(target=run_with_semaphore, args=(task,), daemon=True)
            threads.append(t)
            t.start()

        return threads

    def cancel_all(self):
        for task in self.tasks.values():
            task.cancel()

    def get_task(self, app_id: str) -> Optional[DownloadTask]:
        return self.tasks.get(app_id)

    def clear(self):
        self.tasks.clear()


def format_bytes(bytes_val: float) -> str:
    """Định dạng bytes thành chuỗi dễ đọc"""
    if bytes_val < 1024:
        return f"{bytes_val:.0f} B"
    elif bytes_val < 1024 ** 2:
        return f"{bytes_val / 1024:.1f} KB"
    elif bytes_val < 1024 ** 3:
        return f"{bytes_val / 1024 ** 2:.1f} MB"
    else:
        return f"{bytes_val / 1024 ** 3:.2f} GB"


def format_speed(bps: float) -> str:
    """Định dạng tốc độ tải"""
    return f"{format_bytes(bps)}/s"
