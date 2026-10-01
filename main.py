"""
Win11 After Boot - Entry Point
"""

import sys
import os

# Đảm bảo có thể chạy từ bất kỳ thư mục nào
if getattr(sys, "frozen", False):
    # Đang chạy từ PyInstaller bundle
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)

from app.ui.main_window import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
