"""
App Card Widget + Progress Row — dùng CTK tuple colors
"""

import tkinter as tk
import customtkinter as ctk
from typing import Callable, Optional, Dict, Any

from .styles import (
    BG_CARD, BG_CARD_HOVER, BG_CARD_SELECTED,
    BORDER, BORDER_SELECTED,
    ACCENT, ACCENT_HOVER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    SUCCESS, ERROR, WARNING,
    PROGRESS_BG, PROGRESS_FILL,
    BTN_SECONDARY, BTN_SECONDARY_HOVER,
    FONTS, SIZES, PADDING,
)


class AppCard(ctk.CTkFrame):
    """Card hiển thị thông tin app và cho phép chọn"""

    def __init__(
        self,
        parent,
        app_data: Dict[str, Any],
        on_toggle: Optional[Callable] = None,
        **kwargs,
    ):
        self.app_data = app_data
        self.on_toggle = on_toggle
        self._selected = tk.BooleanVar(value=app_data.get("checked_default", False))
        self._version_var = tk.StringVar(value=app_data.get("default_version", ""))

        super().__init__(
            parent,
            width=SIZES["card_width"],
            height=SIZES["card_height"],
            corner_radius=SIZES["border_radius"],
            fg_color=BG_CARD_SELECTED if self._selected.get() else BG_CARD,
            border_width=2,
            border_color=BORDER_SELECTED if self._selected.get() else BORDER,
            **kwargs,
        )
        self.grid_propagate(False)
        self._build_ui()
        self._bind_click()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        app = self.app_data

        # ── Header: checkbox + icon ──────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew",
                    padx=PADDING["md"], pady=(PADDING["md"], PADDING["xs"]))
        header.grid_columnconfigure(1, weight=1)

        self.checkbox = ctk.CTkCheckBox(
            header,
            text="",
            variable=self._selected,
            width=22, height=22,
            checkbox_width=20, checkbox_height=20,
            corner_radius=5,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            border_color=BORDER,
            command=self._on_check,
        )
        self.checkbox.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text=app["icon_char"],
            font=FONTS["icon"],
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=1, sticky="e")

        # ── App name ─────────────────────────────────────────────────────
        self._name_lbl = ctk.CTkLabel(
            self,
            text=app["name"],
            font=FONTS["subheading"],
            text_color=TEXT_PRIMARY,
            anchor="w",
        )
        self._name_lbl.grid(row=1, column=0, sticky="ew",
                            padx=PADDING["md"], pady=(0, PADDING["xs"]))

        # ── Description ──────────────────────────────────────────────────
        self._desc_lbl = ctk.CTkLabel(
            self,
            text=app["description"],
            font=FONTS["small"],
            text_color=TEXT_SECONDARY,
            anchor="w",
            wraplength=SIZES["card_width"] - PADDING["lg"],
        )
        self._desc_lbl.grid(row=2, column=0, sticky="ew", padx=PADDING["md"])

        next_row = 3

        # ── Python version dropdown ───────────────────────────────────────
        if app.get("has_version_select"):
            vf = ctk.CTkFrame(self, fg_color="transparent")
            vf.grid(row=next_row, column=0, sticky="ew",
                    padx=PADDING["md"], pady=(PADDING["xs"], 0))
            vf.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                vf, text="Phiên bản:",
                font=FONTS["small"], text_color=TEXT_MUTED,
            ).grid(row=0, column=0, sticky="w")

            self.version_dropdown = ctk.CTkOptionMenu(
                vf,
                values=app.get("versions", []),
                variable=self._version_var,
                width=112, height=24,
                corner_radius=6,
                fg_color=BTN_SECONDARY,
                button_color=ACCENT,
                button_hover_color=ACCENT_HOVER,
                text_color=TEXT_PRIMARY,
                font=FONTS["small"],
            )
            self.version_dropdown.grid(row=0, column=1, sticky="e")
            next_row += 1

        # ── Size + category ──────────────────────────────────────────────
        sf = ctk.CTkFrame(self, fg_color="transparent")
        sf.grid(row=next_row, column=0, sticky="ew",
                padx=PADDING["md"], pady=(PADDING["xs"], PADDING["md"]))
        sf.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            sf, text=f"💾 {app['size']}",
            font=FONTS["small"], text_color=TEXT_MUTED, anchor="w",
        ).grid(row=0, column=0, sticky="w")

        cat_color = {
            "Browser":       "#4A90D9",
            "Development":   "#4A90D9",
            "Utilities":     "#7a90c8",
            "Communication": "#0068FF",
        }.get(app.get("category", ""), ACCENT)

        ctk.CTkLabel(
            sf,
            text=app.get("category", ""),
            font=FONTS["small"],
            text_color="#ffffff",
            fg_color=cat_color,
            corner_radius=4,
            padx=6, pady=2,
        ).grid(row=0, column=1, sticky="e")

        self._clickable_widgets = [
            self, self._name_lbl, self._desc_lbl, sf,
        ]

    def _bind_click(self):
        for w in self._clickable_widgets:
            w.bind("<Button-1>", self._toggle)
            w.bind("<Enter>",    self._hover_enter)
            w.bind("<Leave>",    self._hover_leave)

    def _toggle(self, _=None):
        self._selected.set(not self._selected.get())
        self._on_check()

    def _on_check(self):
        sel = self._selected.get()
        self.configure(
            fg_color=BG_CARD_SELECTED if sel else BG_CARD,
            border_color=BORDER_SELECTED if sel else BORDER,
        )
        if self.on_toggle:
            self.on_toggle(self.app_data["id"], sel)

    def _hover_enter(self, _=None):
        if not self._selected.get():
            self.configure(fg_color=BG_CARD_HOVER)

    def _hover_leave(self, _=None):
        if not self._selected.get():
            self.configure(fg_color=BG_CARD)

    # ── Public API ────────────────────────────────────────────────────────
    def is_selected(self) -> bool:
        return self._selected.get()

    def set_selected(self, value: bool):
        self._selected.set(value)
        self._on_check()

    def get_version(self) -> str:
        return self._version_var.get()

    def get_app_id(self) -> str:
        return self.app_data["id"]


# ─────────────────────────────────────────────────────────────────────────────

class ProgressRow(ctk.CTkFrame):
    """Hàng tiến trình tải + cài đặt cho một app"""

    def __init__(self, parent, app_data: Dict[str, Any], **kwargs):
        self.app_data = app_data
        super().__init__(
            parent,
            fg_color=BG_SECONDARY if False else "transparent",  # inherit parent
            corner_radius=8,
            **kwargs,
        )
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        app = self.app_data

        # Icon + name (fixed width)
        nf = ctk.CTkFrame(self, fg_color="transparent", width=150)
        nf.grid(row=0, column=0, sticky="w",
                padx=(PADDING["sm"], PADDING["xs"]), pady=PADDING["sm"])
        nf.grid_propagate(False)

        ctk.CTkLabel(nf, text=app["icon_char"],
                     font=FONTS["icon_small"], text_color=TEXT_PRIMARY,
                     width=26).pack(side="left")
        ctk.CTkLabel(nf, text=app["name"],
                     font=FONTS["body"], text_color=TEXT_PRIMARY,
                     anchor="w").pack(side="left", fill="x", expand=True)

        # Progress bar + label
        pf = ctk.CTkFrame(self, fg_color="transparent")
        pf.grid(row=0, column=1, sticky="ew",
                padx=PADDING["xs"], pady=PADDING["sm"])
        pf.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(
            pf, height=SIZES["progress_height"],
            corner_radius=5,
            fg_color=PROGRESS_BG,
            progress_color=PROGRESS_FILL,
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 2))

        self.status_label = ctk.CTkLabel(
            pf, text="Chờ...",
            font=FONTS["small"], text_color=TEXT_MUTED, anchor="w",
        )
        self.status_label.grid(row=1, column=0, sticky="w")

        # Result icon
        self.result_label = ctk.CTkLabel(
            self, text="⏳",
            font=FONTS["icon_small"], text_color=TEXT_MUTED, width=40,
        )
        self.result_label.grid(row=0, column=2,
                                padx=PADDING["sm"], pady=PADDING["sm"])

    def update_progress(self, progress: float, downloaded: int,
                        total: int, speed: float):
        from ..core.downloader import format_bytes, format_speed
        self.progress_bar.set(min(progress, 1.0))
        pct = f"{progress * 100:.0f}%"
        if total > 0:
            txt = (f"⬇️ {format_bytes(downloaded)} / {format_bytes(total)}"
                   f"  •  {format_speed(speed)}")
        else:
            txt = f"⬇️ {format_bytes(downloaded)}  •  {format_speed(speed)}"
        self.status_label.configure(text=txt, text_color=TEXT_SECONDARY)
        self.result_label.configure(text=pct)

    def set_status_downloading(self):
        self.progress_bar.configure(progress_color=PROGRESS_FILL)
        self.result_label.configure(text="⬇️", text_color=TEXT_PRIMARY)

    def set_status_wsl(self):
        self.progress_bar.configure(progress_color=WARNING)
        self.progress_bar.set(0.1)
        self.status_label.configure(
            text="⚙️ Đang cài WSL (yêu cầu bởi Docker)...",
            text_color=WARNING)
        self.result_label.configure(text="⚙️", text_color=WARNING)

    def set_status_installing(self):
        self.progress_bar.configure(progress_color=WARNING)
        self.progress_bar.set(1.0)
        self.status_label.configure(
            text="Đang cài đặt...", text_color=WARNING)
        self.result_label.configure(text="⚙️", text_color=WARNING)

    def set_status_complete(self):
        self.progress_bar.configure(progress_color=SUCCESS)
        self.progress_bar.set(1.0)
        self.status_label.configure(
            text="✅ Hoàn thành!", text_color=SUCCESS)
        self.result_label.configure(text="✅", text_color=SUCCESS)

    def set_status_error(self, message: str):
        self.progress_bar.configure(progress_color=ERROR)
        self.status_label.configure(text=f"❌ {message}", text_color=ERROR)
        self.result_label.configure(text="❌", text_color=ERROR)

    def set_status_cancelled(self):
        self.status_label.configure(text="⛔ Đã hủy", text_color=TEXT_MUTED)
        self.result_label.configure(text="⛔", text_color=TEXT_MUTED)
