"""
System Settings - Chỉnh các cài đặt hệ thống Windows
"""

import winreg
import subprocess
import ctypes
from typing import Tuple


INTL_KEY = r"Control Panel\International"


def get_current_date_formats() -> dict:
    """Đọc format ngày tháng hiện tại từ Registry"""
    result = {}
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, INTL_KEY, 0, winreg.KEY_READ) as key:
            for name in ("sShortDate", "sLongDate", "sDate", "iDate"):
                try:
                    value, _ = winreg.QueryValueEx(key, name)
                    result[name] = value
                except FileNotFoundError:
                    result[name] = ""
    except Exception as e:
        result["error"] = str(e)
    return result


def set_date_format(short_date: str = "dd/MM/yyyy", long_date: str = "dddd, dd MMMM yyyy") -> Tuple[bool, str]:
    """
    Đặt format ngày tháng trong Registry.
    Trả về (success: bool, message: str)
    """
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, INTL_KEY, 0,
            winreg.KEY_SET_VALUE | winreg.KEY_READ
        ) as key:
            winreg.SetValueEx(key, "sShortDate", 0, winreg.REG_SZ, short_date)
            winreg.SetValueEx(key, "sLongDate",  0, winreg.REG_SZ, long_date)
            # iDate=1 → dd/MM/yyyy order; sDate=/ → separator
            winreg.SetValueEx(key, "sDate",  0, winreg.REG_SZ, "/")
            winreg.SetValueEx(key, "iDate",  0, winreg.REG_SZ, "1")

        # Thông báo Windows cập nhật ngay (broadcast WM_SETTINGCHANGE)
        _broadcast_settings_change()
        return True, "Đã đặt format ngày thành công!"

    except PermissionError:
        return False, "Không đủ quyền ghi Registry. Thử chạy lại với Administrator."
    except Exception as e:
        return False, f"Lỗi: {e}"


def _broadcast_settings_change():
    """Gửi thông báo WM_SETTINGCHANGE để Windows áp dụng ngay không cần reboot"""
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_long()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0,
        "intl", SMTO_ABORTIFHUNG, 5000,
        ctypes.byref(result)
    )


def open_region_settings():
    """Mở cửa sổ Region Settings của Windows"""
    subprocess.Popen(["control", "intl.cpl"])
