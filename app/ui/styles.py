"""
Styles - Color constants as (light, dark) tuples.
CustomTkinter tự động chọn đúng màu theo appearance mode.
"""

# ─── Backgrounds ───────────────────────────────────────────────────────────
BG_PRIMARY       = ("#f4f6f8", "#1e1e2e")   # Nền trang chính
BG_SECONDARY     = ("#ffffff", "#2a2a3e")   # Panels, header, footer
BG_CARD          = ("#ffffff", "#2e2e42")   # Card bình thường
BG_CARD_HOVER    = ("#f0f4fa", "#383850")   # Card hover
BG_CARD_SELECTED = ("#e8f0fe", "#1e3a5f")   # Card được chọn
BG_INPUT         = ("#f0f2f5", "#262636")   # Text entry

# ─── Accent — blue nhạt, dùng chung cả 2 mode ─────────────────────────────
ACCENT           = "#4A90D9"
ACCENT_HOVER     = "#3a7bc8"

# ─── Text ──────────────────────────────────────────────────────────────────
TEXT_PRIMARY     = ("#111111", "#f0f0f0")
TEXT_SECONDARY   = ("#444444", "#b0b8c8")
TEXT_MUTED       = ("#888888", "#6b7a8d")

# ─── Borders ───────────────────────────────────────────────────────────────
BORDER           = ("#dde1e8", "#3a3a52")
BORDER_SELECTED  = ACCENT

# ─── Status ────────────────────────────────────────────────────────────────
SUCCESS          = ("#1a9950", "#2ecc71")
ERROR            = ("#cc3333", "#e05050")
WARNING          = ("#b06800", "#f39c12")

# ─── Buttons ───────────────────────────────────────────────────────────────
BTN_PRIMARY         = ACCENT
BTN_PRIMARY_HOVER   = ACCENT_HOVER
BTN_SECONDARY       = ("#e4e8ee", "#3a3a52")
BTN_SECONDARY_HOVER = ("#d4d8e0", "#4a4a62")

# ─── Misc ──────────────────────────────────────────────────────────────────
PROGRESS_BG      = ("#e0e4ea", "#262636")
PROGRESS_FILL    = ACCENT
SCROLLBAR        = ("#c4c8d0", "#3a3a52")
DIVIDER          = ("#e0e4ea", "#3a3a52")

# ─── Fonts ─────────────────────────────────────────────────────────────────
FONTS = {
    "title":        ("Segoe UI", 24, "bold"),
    "subtitle":     ("Segoe UI", 13),
    "heading":      ("Segoe UI", 15, "bold"),
    "subheading":   ("Segoe UI", 13, "bold"),
    "body":         ("Segoe UI", 12),
    "small":        ("Segoe UI", 10),
    "icon":         ("Segoe UI Emoji", 24),
    "icon_small":   ("Segoe UI Emoji", 16),
    "monospace":    ("Consolas", 11),
    "button":       ("Segoe UI", 12, "bold"),
    "button_small": ("Segoe UI", 11),
}

# ─── Sizes ─────────────────────────────────────────────────────────────────
SIZES = {
    "window_width":        1000,
    "window_height":        720,
    "card_width":           200,
    "card_height":          190,
    "border_radius":         12,
    "button_height":         40,
    "button_height_small":   30,
    "progress_height":       10,
    "header_height":         64,
}

# ─── Padding ───────────────────────────────────────────────────────────────
PADDING = {
    "xs":  4,
    "sm":  8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}
