"""
Settings Panel - Chỉnh định dạng ngày tháng Windows
"""

import tkinter as tk
import customtkinter as ctk
from typing import Optional

from .styles import (
    BG_SECONDARY, BG_PRIMARY, BG_INPUT,
    ACCENT, ACCENT_HOVER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    BORDER, SUCCESS, ERROR, WARNING,
    BTN_SECONDARY, BTN_SECONDARY_HOVER,
    FONTS, PADDING,
)

DATE_FORMAT_PRESETS = [
    ("dd/MM/yyyy  (Việt Nam)",  "dd/MM/yyyy",  "dddd, dd MMMM yyyy"),
    ("MM/dd/yyyy  (Mỹ)",        "MM/dd/yyyy",  "dddd, MMMM dd, yyyy"),
    ("yyyy-MM-dd  (ISO 8601)",  "yyyy-MM-dd",  "yyyy MMMM dd, dddd"),
    ("dd-MM-yyyy  (Dấu gạch)", "dd-MM-yyyy",  "dddd dd-MM-yyyy"),
    ("dd.MM.yyyy  (Châu Âu)",  "dd.MM.yyyy",  "dddd, dd. MMMM yyyy"),
    ("d/M/yyyy   (Ngắn)",      "d/M/yyyy",    "dddd, d MMMM yyyy"),
]


class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=BG_SECONDARY,
            corner_radius=12,
            **kwargs,
        )
        self.grid_columnconfigure(0, weight=1)
        self._selected_preset = tk.StringVar(value=DATE_FORMAT_PRESETS[0][1])
        self._build_ui()
        self._load_current_format()

    # ─── Build ────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew",
                    padx=PADDING["lg"], pady=(PADDING["lg"], PADDING["xs"]))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header, text="🗓️",
            font=FONTS["icon"], text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, padx=(0, PADDING["sm"]))

        title_col = ctk.CTkFrame(header, fg_color="transparent")
        title_col.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            title_col,
            text="Định dạng Ngày tháng Windows",
            font=FONTS["subheading"], text_color=TEXT_PRIMARY, anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_col,
            text="Thay đổi ngay, không cần khởi động lại",
            font=FONTS["small"], text_color=TEXT_MUTED, anchor="w",
        ).pack(anchor="w")

        ctk.CTkButton(
            header,
            text="⚙️ Region Settings",
            font=FONTS["button_small"],
            height=28, width=130,
            fg_color=BTN_SECONDARY,
            hover_color=BTN_SECONDARY_HOVER,
            text_color=TEXT_PRIMARY,
            corner_radius=6,
            command=self._open_region_settings,
        ).grid(row=0, column=2)

        # Current format display
        cur = ctk.CTkFrame(self, fg_color=BG_INPUT, corner_radius=8)
        cur.grid(row=1, column=0, sticky="ew",
                 padx=PADDING["lg"], pady=(0, PADDING["sm"]))
        cur.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            cur, text="Format hiện tại:",
            font=FONTS["small"], text_color=TEXT_MUTED,
            width=110, anchor="w",
        ).grid(row=0, column=0, padx=(PADDING["md"], PADDING["sm"]),
               pady=PADDING["sm"], sticky="w")

        self.current_label = ctk.CTkLabel(
            cur, text="Đang đọc...",
            font=("Consolas", 13, "bold"),
            text_color=ACCENT, anchor="w",
        )
        self.current_label.grid(row=0, column=1,
                                 padx=(0, PADDING["md"]),
                                 pady=PADDING["sm"], sticky="w")

        # Preset radio buttons (2 cột)
        pf = ctk.CTkFrame(self, fg_color="transparent")
        pf.grid(row=2, column=0, sticky="ew",
                padx=PADDING["lg"], pady=(0, PADDING["xs"]))

        ctk.CTkLabel(
            pf, text="Chọn format:",
            font=FONTS["body"], text_color=TEXT_SECONDARY, anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w",
               pady=(0, PADDING["xs"]))

        cols = 2
        for i, (label, short, _) in enumerate(DATE_FORMAT_PRESETS):
            r = i // cols
            c = i % cols
            ctk.CTkRadioButton(
                pf,
                text=label,
                font=FONTS["body"],
                text_color=TEXT_PRIMARY,
                variable=self._selected_preset,
                value=short,
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                border_color=BORDER,
                command=self._on_preset,
            ).grid(row=r + 1, column=c, sticky="w",
                   padx=(0, PADDING["xl"]), pady=2)

        # Custom input
        cf = ctk.CTkFrame(self, fg_color=BG_INPUT, corner_radius=8)
        cf.grid(row=3, column=0, sticky="ew",
                padx=PADDING["lg"], pady=(PADDING["xs"], 0))
        cf.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            cf, text="Tự nhập:",
            font=FONTS["small"], text_color=TEXT_MUTED,
            width=80, anchor="w",
        ).grid(row=0, column=0, padx=(PADDING["md"], PADDING["sm"]),
               pady=PADDING["sm"])

        self.custom_entry = ctk.CTkEntry(
            cf,
            placeholder_text="vd: dd/MM/yyyy",
            font=("Consolas", 12),
            height=30,
            fg_color=BG_INPUT,
            border_color=BORDER,
            text_color=TEXT_PRIMARY,
            corner_radius=6,
        )
        self.custom_entry.grid(row=0, column=1, sticky="ew",
                                padx=(0, PADDING["sm"]), pady=PADDING["sm"])
        self.custom_entry.bind("<KeyRelease>", self._on_custom)

        ctk.CTkLabel(
            cf, text="d=ngày  M=tháng  y=năm",
            font=FONTS["small"], text_color=TEXT_MUTED, anchor="w",
        ).grid(row=1, column=1, sticky="w",
               padx=(0, PADDING["md"]), pady=(0, PADDING["sm"]))

        # Preview
        pvf = ctk.CTkFrame(self, fg_color="transparent")
        pvf.grid(row=4, column=0, sticky="ew",
                 padx=PADDING["lg"], pady=(PADDING["xs"], 0))
        pvf.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            pvf, text="Preview:",
            font=FONTS["small"], text_color=TEXT_MUTED,
            width=80, anchor="w",
        ).grid(row=0, column=0)

        self.preview_label = ctk.CTkLabel(
            pvf, text="",
            font=("Consolas", 13, "bold"),
            text_color=SUCCESS, anchor="w",
        )
        self.preview_label.grid(row=0, column=1, sticky="w")

        # Apply + status
        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.grid(row=5, column=0, sticky="ew",
                padx=PADDING["lg"], pady=PADDING["md"])
        bf.grid_columnconfigure(1, weight=1)

        self.apply_btn = ctk.CTkButton(
            bf,
            text="✅  Áp dụng ngay",
            font=FONTS["button"],
            height=36, width=160,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#ffffff",
            corner_radius=8,
            command=self._apply,
        )
        self.apply_btn.grid(row=0, column=0)

        self.status_label = ctk.CTkLabel(
            bf, text="",
            font=FONTS["body"], text_color=TEXT_MUTED, anchor="w",
        )
        self.status_label.grid(row=0, column=1,
                                padx=(PADDING["md"], 0), sticky="w")

        # Init preview
        self._update_preview(DATE_FORMAT_PRESETS[0][1])

    # ─── Logic ────────────────────────────────────────────────────────────

    def _load_current_format(self):
        from ..core.system_settings import get_current_date_formats
        info = get_current_date_formats()
        self.current_label.configure(
            text=info.get("sShortDate") or "Chưa đặt"
        )

    def _on_preset(self):
        self.custom_entry.delete(0, "end")
        self._update_preview(self._selected_preset.get())

    def _on_custom(self, _=None):
        val = self.custom_entry.get().strip()
        if val:
            self._selected_preset.set("")
            self._update_preview(val)

    def _update_preview(self, fmt: str):
        from datetime import date
        today = date.today()
        try:
            token_map = [
                ("dddd", "%A"), ("ddd", "%a"),
                ("dd", "%d"),   ("d", "##DAY##"),
                ("MMMM", "%B"), ("MMM", "%b"),
                ("MM", "%m"),   ("M", "##MON##"),
                ("yyyy", "%Y"), ("yy", "%y"),
            ]
            py_fmt = fmt
            for win, py in token_map:
                py_fmt = py_fmt.replace(win, py)

            # Thay ##DAY## / ##MON## bằng giá trị thực (strip leading zero)
            day_stripped   = str(today.day)    # "1" thay "01"
            month_stripped = str(today.month)  # "10" giữ nguyên

            py_fmt = py_fmt.replace("##DAY##", day_stripped)
            py_fmt = py_fmt.replace("##MON##", month_stripped)

            preview = today.strftime(py_fmt)
            self.preview_label.configure(
                text=f"📅  {preview}  ({fmt})",
                text_color=SUCCESS,
            )
        except Exception:
            self.preview_label.configure(
                text=f"📅  {fmt}", text_color=TEXT_MUTED)

    def _apply(self):
        custom = self.custom_entry.get().strip()
        short_fmt = custom if custom else self._selected_preset.get()
        if not short_fmt:
            self._set_status("⚠️ Chưa chọn format!", WARNING)
            return

        long_fmt = "dddd, dd MMMM yyyy"
        for _, s, l in DATE_FORMAT_PRESETS:
            if s == short_fmt:
                long_fmt = l
                break

        self.apply_btn.configure(state="disabled", text="⏳ Đang áp dụng...")
        self.after(50, lambda: self._do_apply(short_fmt, long_fmt))

    def _do_apply(self, short_fmt: str, long_fmt: str):
        from ..core.system_settings import set_date_format
        ok, msg = set_date_format(short_fmt, long_fmt)
        if ok:
            self._set_status(f"✅ {msg}  →  {short_fmt}", SUCCESS)
            self.current_label.configure(text=short_fmt)
        else:
            self._set_status(f"❌ {msg}", ERROR)
        self.apply_btn.configure(state="normal", text="✅  Áp dụng ngay")

    def _set_status(self, text: str, color):
        self.status_label.configure(text=text, text_color=color)

    def _open_region_settings(self):
        from ..core.system_settings import open_region_settings
        open_region_settings()
