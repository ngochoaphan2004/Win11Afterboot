"""
Installer - Chạy file cài đặt sau khi tải xong (hỗ trợ .exe và .msi, tự động xử lý quyền Admin)
"""

import subprocess
import threading
import os
import ctypes
from ctypes import wintypes
from pathlib import Path
from typing import Callable, Optional


def is_admin() -> bool:
    """Kiểm tra tiến trình hiện tại có quyền Administrator hay không"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


class SHELLEXECUTEINFOW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("fMask", wintypes.ULONG),
        ("hwnd", wintypes.HWND),
        ("lpVerb", wintypes.LPCWSTR),
        ("lpFile", wintypes.LPCWSTR),
        ("lpParameters", wintypes.LPCWSTR),
        ("lpDirectory", wintypes.LPCWSTR),
        ("nShow", ctypes.c_int),
        ("hInstApp", wintypes.HINSTANCE),
        ("lpIDList", wintypes.LPVOID),
        ("lpClass", wintypes.LPCWSTR),
        ("hkeyClass", wintypes.HKEY),
        ("dwHotKey", wintypes.DWORD),
        ("hIconOrMonitor", wintypes.HANDLE),
        ("hProcess", wintypes.HANDLE),
    ]


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

    def _run_elevated(self, executable: str, args: list[str]) -> int:
        """Chạy lệnh với quyền Administrator thông qua Windows UAC (ShellExecuteExW)"""
        SEE_MASK_NOCLOSEPROCESS = 0x00000040
        SEE_MASK_NOASYNC = 0x00000100
        SW_HIDE = 0
        INFINITE = 0xFFFFFFFF

        params_str = " ".join(f'"{a}"' if " " in a else a for a in args)

        sei = SHELLEXECUTEINFOW()
        sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFOW)
        sei.fMask = SEE_MASK_NOCLOSEPROCESS | SEE_MASK_NOASYNC
        sei.hwnd = None
        sei.lpVerb = "runas"
        sei.lpFile = executable
        sei.lpParameters = params_str
        sei.lpDirectory = None
        sei.nShow = SW_HIDE
        sei.hInstApp = None

        success = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))
        if not success or not sei.hProcess:
            raise PermissionError("Người dùng đã từ chối cấp quyền Administrator (UAC)")

        ctypes.windll.kernel32.WaitForSingleObject(sei.hProcess, INFINITE)
        exit_code = wintypes.DWORD()
        ctypes.windll.kernel32.GetExitCodeProcess(sei.hProcess, ctypes.byref(exit_code))
        ctypes.windll.kernel32.CloseHandle(sei.hProcess)
        return exit_code.value

    def _run_installer(self, app_id: str, file_path: Path, install_args: list[str]) -> bool:
        try:
            if self.on_start:
                self.on_start(app_id)

            if not file_path.exists():
                raise FileNotFoundError(f"File không tồn tại: {file_path}")

            is_msi = file_path.suffix.lower() == ".msi"

            if is_msi:
                target_exe = "msiexec.exe"
                full_args = ["/i", str(file_path)] + install_args
            else:
                target_exe = str(file_path)
                full_args = install_args

            # Nếu app đã chạy với quyền Admin -> subprocess kế thừa quyền Admin trực tiếp
            if is_admin():
                cmd = [target_exe] + full_args
                result = subprocess.run(
                    cmd,
                    capture_output=False,
                    timeout=600,  # 10 phút timeout
                )
                returncode = result.returncode
            else:
                # Chưa có quyền Admin -> Yêu cầu UAC qua ShellExecuteExW
                try:
                    returncode = self._run_elevated(target_exe, full_args)
                except PermissionError:
                    raise PermissionError("Cần quyền Administrator để hoàn tất cài đặt (UAC bị từ chối)")

            if returncode in (0, 3010):  # 3010 = thành công, cần reboot
                if self.on_complete:
                    self.on_complete(app_id, returncode == 3010)
                return True
            elif returncode == 1603:
                raise RuntimeError("Lỗi 1603: Không đủ quyền Administrator để cài đặt. Hãy khởi chạy ứng dụng với quyền 'Run as administrator'")
            else:
                raise RuntimeError(f"Installer trả về mã lỗi: {returncode}")

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
