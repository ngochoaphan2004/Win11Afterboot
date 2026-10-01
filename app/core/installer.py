"""
Installer - Chạy file cài đặt sau khi tải xong
"""

import subprocess
import threading
import os
from pathlib import Path
from typing import Callable, Optional


class InstallerRunner:
    """Chạy file installer với các tham số im lặng"""

    def __init__(
        self,
        on_start: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
    ):
        self.on_start = on_start
        self.on_complete = on_complete
        self.on_error = on_error

    def run(self, app_id: str, file_path: Path, install_args: list[str]):
        """Chạy installer trong thread riêng"""
        thread = threading.Thread(
            target=self._run_installer,
            args=(app_id, file_path, install_args),
            daemon=True,
        )
        thread.start()
        return thread

    def run_sync(self, app_id: str, file_path: Path, install_args: list[str]) -> bool:
        """Chạy installer đồng bộ, trả về True nếu thành công"""
        return self._run_installer(app_id, file_path, install_args)

    def _run_installer(self, app_id: str, file_path: Path, install_args: list[str]) -> bool:
        try:
            if self.on_start:
                self.on_start(app_id)

            if not file_path.exists():
                raise FileNotFoundError(f"File không tồn tại: {file_path}")

            cmd = [str(file_path)] + install_args

            # Chạy installer với quyền admin (UAC sẽ hiện lên nếu cần)
            result = subprocess.run(
                cmd,
                capture_output=False,
                timeout=600,  # 10 phút timeout
            )

            if result.returncode in (0, 3010):  # 3010 = cần reboot
                if self.on_complete:
                    self.on_complete(app_id, result.returncode == 3010)
                return True
            else:
                raise RuntimeError(f"Installer trả về mã lỗi: {result.returncode}")

        except subprocess.TimeoutExpired:
            if self.on_error:
                self.on_error(app_id, "Cài đặt quá thời gian (10 phút)")
            return False
        except PermissionError:
            if self.on_error:
                self.on_error(app_id, "Không đủ quyền. Thử chạy lại với quyền Administrator")
            return False
        except Exception as e:
            if self.on_error:
                self.on_error(app_id, str(e))
            return False

    def open_installer_manually(self, file_path: Path):
        """Mở file installer để người dùng cài thủ công"""
        os.startfile(str(file_path))
