"""
Main Window — Light mode default, tuple-based colors, WSL pre-install for Docker
"""

import os
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
from typing import Dict
import customtkinter as ctk

from .styles import (
    BG_PRIMARY, BG_SECONDARY, BG_CARD,
    ACCENT, ACCENT_HOVER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    BORDER, SUCCESS, ERROR, WARNING,
    BTN_PRIMARY, BTN_PRIMARY_HOVER,
    BTN_SECONDARY, BTN_SECONDARY_HOVER,
    PROGRESS_BG, PROGRESS_FILL, SCROLLBAR,
    DIVIDER, FONTS, SIZES, PADDING,
)
from .app_card import AppCard, ProgressRow
from .settings_panel import SettingsPanel
from ..core.app_registry import APPS
from ..core.downloader import DownloadTask, DownloadManager
from ..core.installer import InstallerRunner


class MainWindow(ctk.CTk):
    """Cửa sổ chính"""

    def __init__(self):
        super().__init__()

        # ── Light mode là default ──────────────────────────────────────────
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self._dark_mode = False
        self._cards: Dict[str, AppCard] = {}
        self._progress_rows: Dict[str, ProgressRow] = {}
        self._download_manager = DownloadManager(max_concurrent=2)
        self._installer = InstallerRunner(
            on_start=self._on_install_start,
            on_complete=self._on_install_complete,
            on_error=self._on_install_error,
        )
        self._is_running = False

        self._setup_window()
        self._build_ui()

    # =========================================================================
    # Window setup
    # =========================================================================

    def _setup_window(self):
        self.title("🚀 Win11 After Boot")
        w, h = SIZES["window_width"], SIZES["window_height"]
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(860, 560)
        self.configure(fg_color=BG_PRIMARY)

    # =========================================================================
    # Build UI
    # =========================================================================

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)   # row 1 = scroll area
        self._build_header()      # row 0
        self._build_scroll_body() # row 1
        self._build_footer()      # row 2

    # ─── Header ──────────────────────────────────────────────────────────────

    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color=BG_SECONDARY,
            corner_radius=0,
            height=SIZES["header_height"],
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Title
        tf = ctk.CTkFrame(header, fg_color="transparent")
        tf.grid(row=0, column=0, padx=PADDING["xl"],
                pady=PADDING["md"], sticky="w")

        ctk.CTkLabel(
            tf,
            text="🚀 Win11 After Boot",
            font=FONTS["title"],
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        ctk.CTkLabel(
            tf,
            text="  —  Cài đặt tiện ích nhanh sau cài Windows",
            font=FONTS["subtitle"],
            text_color=TEXT_MUTED,
        ).pack(side="left")

        # Theme switch (Light = OFF, Dark = ON)
        ctrl = ctk.CTkFrame(header, fg_color="transparent")
        ctrl.grid(row=0, column=2, padx=PADDING["xl"],
                  pady=PADDING["md"], sticky="e")

        self.theme_switch = ctk.CTkSwitch(
            ctrl,
            text="☀️ Light",
            font=FONTS["body"],
            text_color=TEXT_SECONDARY,
            command=self._toggle_theme,
            fg_color=BORDER,
            progress_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
        )
        # Không gọi .select() → switch off = light (default)
        self.theme_switch.pack(side="left")

    # ─── Scroll body ─────────────────────────────────────────────────────────

    def _build_scroll_body(self):
        self.scroll_body = ctk.CTkScrollableFrame(
            self,
            fg_color=BG_PRIMARY,
            corner_radius=0,
            scrollbar_fg_color=BG_SECONDARY,
            scrollbar_button_color=SCROLLBAR,
            scrollbar_button_hover_color=ACCENT,
        )
        self.scroll_body.grid(row=1, column=0, sticky="nsew")
        self.scroll_body.grid_columnconfigure(0, weight=1)

        self._build_toolbar(self.scroll_body,    grid_row=0)
        self._build_cards_section(self.scroll_body, grid_row=1)
        self._build_divider(self.scroll_body,    grid_row=2,
                            label="⚙️  Cài đặt hệ thống")
        # Settings panel (không có 'theme' param)
        self.settings_panel = SettingsPanel(self.scroll_body)
        self.settings_panel.grid(row=3, column=0, sticky="ew",
                                  padx=PADDING["xl"],
                                  pady=(0, PADDING["md"]))
        self._build_divider(self.scroll_body,    grid_row=4,
                            label="📊  Tiến trình tải & cài đặt")
        self._build_progress_section(self.scroll_body, grid_row=5)
        # Bottom spacer
        ctk.CTkFrame(self.scroll_body, fg_color="transparent",
                     height=PADDING["lg"]).grid(row=6, column=0)

    def _build_divider(self, parent, grid_row: int, label: str = ""):
        div = ctk.CTkFrame(parent, fg_color="transparent")
        div.grid(row=grid_row, column=0, sticky="ew",
                 padx=PADDING["xl"],
                 pady=(PADDING["md"], PADDING["xs"]))
        div.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            div, text=label,
            font=FONTS["subheading"], text_color=TEXT_SECONDARY,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkFrame(
            div, height=1,
            fg_color=DIVIDER, corner_radius=0,
        ).grid(row=0, column=1, sticky="ew",
               padx=(PADDING["md"], 0), pady=6)

    # ─── Toolbar ──────────────────────────────────────────────────────────────

    def _build_toolbar(self, parent, grid_row: int):
        tb = ctk.CTkFrame(parent, fg_color="transparent")
        tb.grid(row=grid_row, column=0, sticky="ew",
                padx=PADDING["xl"],
                pady=(PADDING["lg"], PADDING["xs"]))
        tb.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            tb,
            text="Chọn phần mềm muốn tải và cài đặt:",
            font=FONTS["heading"], text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        bf = ctk.CTkFrame(tb, fg_color="transparent")
        bf.grid(row=0, column=2, sticky="e")

        for text, cmd, primary in [
            ("✅ Chọn tất cả", self._select_all,   False),
            ("⬜ Bỏ chọn",     self._deselect_all,  False),
            ("⬇️  Tải & Cài", self._start_download, True),
        ]:
            btn = ctk.CTkButton(
                bf,
                text=text,
                font=FONTS["button" if primary else "button_small"],
                height=SIZES["button_height_small"],
                width=150 if primary else 120,
                fg_color=BTN_PRIMARY if primary else BTN_SECONDARY,
                hover_color=BTN_PRIMARY_HOVER if primary else BTN_SECONDARY_HOVER,
                text_color="#ffffff" if primary else TEXT_PRIMARY,
                corner_radius=8,
                command=cmd,
            )
            btn.pack(side="left", padx=(0, PADDING["sm"]))
            if primary:
                self.install_btn = btn

    # ─── App cards ────────────────────────────────────────────────────────────

    def _build_cards_section(self, parent, grid_row: int):
        cc = ctk.CTkFrame(parent, fg_color="transparent")
        cc.grid(row=grid_row, column=0, sticky="ew",
                padx=PADDING["lg"], pady=(PADDING["xs"], 0))

        cols = 4
        for i, app in enumerate(APPS):
            r, c = i // cols, i % cols
            card = AppCard(cc, app_data=app, on_toggle=self._on_card_toggle)
            card.grid(row=r, column=c,
                      padx=PADDING["sm"], pady=PADDING["sm"],
                      sticky="nsew")
            cc.grid_columnconfigure(c, weight=1)
            self._cards[app["id"]] = card

    # ─── Progress section ─────────────────────────────────────────────────────

    def _build_progress_section(self, parent, grid_row: int):
        pw = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=12)
        pw.grid(row=grid_row, column=0, sticky="ew",
                padx=PADDING["xl"], pady=(0, PADDING["sm"]))
        pw.grid_columnconfigure(0, weight=1)

        bar = ctk.CTkFrame(pw, fg_color="transparent")
        bar.grid(row=0, column=0, sticky="ew",
                 padx=PADDING["lg"], pady=(PADDING["md"], PADDING["xs"]))
        bar.grid_columnconfigure(0, weight=1)

        self.open_folder_btn = ctk.CTkButton(
            bar, text="📁 Mở thư mục tải",
            font=FONTS["button_small"], height=26, width=140,
            fg_color=BTN_SECONDARY, hover_color=BTN_SECONDARY_HOVER,
            text_color=TEXT_PRIMARY, corner_radius=6,
            command=self._open_folder,
        )
        self.open_folder_btn.grid(row=0, column=1, sticky="e",
                                   padx=(PADDING["sm"], 0))

        self.cancel_btn = ctk.CTkButton(
            bar, text="⛔ Hủy",
            font=FONTS["button_small"], height=26, width=80,
            fg_color=ERROR, hover_color="#c0392b",
            text_color="#ffffff", corner_radius=6,
            command=self._cancel_all, state="disabled",
        )
        self.cancel_btn.grid(row=0, column=2, sticky="e",
                              padx=(PADDING["sm"], 0))

        self.progress_container = ctk.CTkFrame(pw, fg_color="transparent")
        self.progress_container.grid(row=1, column=0, sticky="ew",
                                      padx=PADDING["lg"],
                                      pady=(0, PADDING["md"]))
        self.progress_container.grid_columnconfigure(0, weight=1)

        self.progress_placeholder = ctk.CTkLabel(
            self.progress_container,
            text="Chọn phần mềm ở trên và nhấn 「Tải & Cài đặt」 để bắt đầu",
            font=FONTS["body"], text_color=TEXT_MUTED,
        )
        self.progress_placeholder.grid(row=0, column=0, pady=PADDING["md"])

    # ─── Footer ───────────────────────────────────────────────────────────────

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color=BG_SECONDARY,
                               height=28, corner_radius=0)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)

        ctk.CTkLabel(
            footer,
            text="Win11 After Boot  •  Tải từ nguồn chính thức  •  Made with ❤️",
            font=FONTS["small"], text_color=TEXT_MUTED,
        ).pack(side="left", padx=PADDING["xl"])

        self.count_label = ctk.CTkLabel(
            footer, text="0 phần mềm được chọn",
            font=FONTS["small"], text_color=TEXT_MUTED,
        )
        self.count_label.pack(side="right", padx=PADDING["xl"])

    # =========================================================================
    # Events
    # =========================================================================

    def _on_card_toggle(self, app_id: str, selected: bool):
        n = sum(1 for c in self._cards.values() if c.is_selected())
        self.count_label.configure(text=f"{n} phần mềm được chọn")

    def _select_all(self):
        for c in self._cards.values():
            c.set_selected(True)
        self._on_card_toggle("", True)

    def _deselect_all(self):
        for c in self._cards.values():
            c.set_selected(False)
        self._on_card_toggle("", False)

    def _toggle_theme(self):
        """Switch giữa light và dark — CTK tự cập nhật toàn bộ màu qua tuples"""
        self._dark_mode = not self._dark_mode
        if self._dark_mode:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="🌙 Dark")
        else:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="☀️ Light")

    # ─── Download & Install ───────────────────────────────────────────────────

    def _start_download(self):
        selected = [app for app in APPS if self._cards[app["id"]].is_selected()]

        if not selected:
            messagebox.showwarning(
                "Chưa chọn phần mềm",
                "Vui lòng chọn ít nhất một phần mềm để tải và cài đặt!",
            )
            return
        if self._is_running:
            messagebox.showinfo("Đang xử lý", "Đang tải hoặc cài đặt, vui lòng chờ...")
            return

        self._is_running = True
        self.install_btn.configure(state="disabled", text="⏳ Đang xử lý...")
        self.cancel_btn.configure(state="normal")
        self.progress_placeholder.grid_remove()

        for row in self._progress_rows.values():
            row.destroy()
        self._progress_rows.clear()
        self._download_manager.clear()

        for i, app in enumerate(selected):
            row = ProgressRow(self.progress_container, app_data=app)
            row.grid(row=i, column=0, sticky="ew", pady=2)
            self._progress_rows[app["id"]] = row

        # Scroll xuống progress
        self.after(150, lambda: self.scroll_body._parent_canvas.yview_moveto(1.0))

        # Tạo download tasks
        for app in selected:
            url, filename = app["url"], app["filename"]
            if app.get("has_version_select"):
                ver = self._cards[app["id"]].get_version()
                url = url.replace("{version}", ver)
                filename = filename.replace("{version}", ver)
            task = DownloadTask(
                app_id=app["id"], name=app["name"],
                url=url, filename=filename,
                on_progress=self._on_dl_progress,
                on_complete=self._on_dl_complete,
                on_error=self._on_dl_error,
            )
            self._download_manager.add_task(task)

        threading.Thread(
            target=self._run_all, args=(selected,), daemon=True
        ).start()

    def _run_all(self, selected):
        """Tải song song → cài tuần tự (chạy WSL trước Docker)"""
        threads = self._download_manager.start_all()
        for t in threads:
            t.join()

        for app in selected:
            task = self._download_manager.get_task(app["id"])
            if not (task and task.status == "completed" and task.file_path):
                continue

            app_id = app["id"]

            # ── WSL pre-install (Docker hoặc app nào có requires_wsl) ─────
            if app.get("requires_wsl"):
                self.after(0, lambda a=app_id: self._set_row_status(a, "wsl"))
                try:
                    subprocess.run(
                        ["wsl", "--install", "--no-launch"],
                        timeout=180,
                        capture_output=True,
                    )
                except Exception:
                    pass  # WSL có thể đã cài → bỏ qua lỗi

            self.after(0, lambda a=app_id: self._set_row_status(a, "installing"))
            self._installer.run_sync(
                app_id=app_id,
                file_path=task.file_path,
                install_args=app.get("install_args", []),
            )

        self.after(0, self._on_all_done)

    def _set_row_status(self, app_id: str, status: str):
        row = self._progress_rows.get(app_id)
        if not row:
            return
        if status == "wsl":
            row.set_status_wsl()
        elif status == "installing":
            row.set_status_installing()

    # ─── Callbacks (background → UI thread) ──────────────────────────────────

    def _on_dl_progress(self, app_id, progress, downloaded, total, speed):
        self.after(0, lambda: self._update_row_progress(
            app_id, progress, downloaded, total, speed))

    def _update_row_progress(self, app_id, progress, downloaded, total, speed):
        row = self._progress_rows.get(app_id)
        if row:
            row.set_status_downloading()
            row.update_progress(progress, downloaded, total, speed)

    def _on_dl_complete(self, app_id, file_path):
        self.after(0, lambda: self._progress_rows.get(app_id) and
                   self._progress_rows[app_id].update_progress(1.0, 0, 0, 0))

    def _on_dl_error(self, app_id, message):
        self.after(0, lambda: self._progress_rows.get(app_id) and
                   self._progress_rows[app_id].set_status_error(f"Tải thất bại: {message}"))

    def _on_install_start(self, app_id):
        self.after(0, lambda: self._set_row_status(app_id, "installing"))

    def _on_install_complete(self, app_id, needs_reboot):
        def update():
            row = self._progress_rows.get(app_id)
            if row:
                row.set_status_complete()
                if needs_reboot:
                    row.status_label.configure(
                        text="✅ Hoàn thành (cần khởi động lại)")
        self.after(0, update)

    def _on_install_error(self, app_id, message):
        self.after(0, lambda: self._progress_rows.get(app_id) and
                   self._progress_rows[app_id].set_status_error(
                       f"Cài đặt thất bại: {message}"))

    def _on_all_done(self):
        self._is_running = False
        self.install_btn.configure(state="normal", text="⬇️  Tải & Cài")
        self.cancel_btn.configure(state="disabled")
        messagebox.showinfo(
            "✅ Hoàn thành!",
            "Đã tải và cài đặt xong tất cả phần mềm được chọn.\n\n"
            "Một số phần mềm có thể yêu cầu khởi động lại máy tính.",
        )

    def _cancel_all(self):
        if messagebox.askyesno("Xác nhận hủy",
                               "Bạn muốn hủy tất cả quá trình đang chạy?"):
            self._download_manager.cancel_all()
            for row in self._progress_rows.values():
                row.set_status_cancelled()
            self._is_running = False
            self.install_btn.configure(state="normal", text="⬇️  Tải & Cài")
            self.cancel_btn.configure(state="disabled")

    def _open_folder(self):
        from ..core.downloader import get_download_dir
        os.startfile(str(get_download_dir()))
