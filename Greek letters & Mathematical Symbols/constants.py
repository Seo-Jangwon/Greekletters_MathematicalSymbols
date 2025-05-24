# constants.py
"""
애플리케이션에서 사용되는 모든 상수와 테마 정의
"""

# 스케일 제한값
SCALE_LIMITS = {
    "min_font_size": 8,
    "max_font_size": 14,
    "base_font_size": 10,
    "min_button_height": 25,
    "max_button_height": 40,
    "min_padding": 2,
    "max_padding": 8,
    "recent_scroll_ratio": 0.3,
    "max_recent_items": 15,
    "favorites_scroll_ratio": 0.25,
    "max_favorites": 1000,
}

# 윈도우 설정
WINDOW_SETTINGS = {
    "base_width": 450,
    "base_height": 600,
    "min_width": 300,
    "min_height": 500,
    "max_width": 500,
    "max_height": 800,
}

# 다크 테마 색상
DARK_THEME = {
    "background": "#1a1b26",
    "foreground": "#a9b1d6",
    "accent1": "#bb9af7",
    "accent2": "#7aa2f7",
    "accent3": "#9ece6a",
    "accent4": "#f7768e",
    "accent5": "#7dcfff",
    "dark_bg": "#16161e",
    "light_bg": "#24283b",
    "button_bg": "#24283b",
    "button_hover": "#414868",
    "button_border": "#414868",
}

# 라이트 테마 색상
LIGHT_THEME = {
    "background": "#f0f1f5",
    "foreground": "#343b58",
    "accent1": "#9d7cd8",
    "accent2": "#5a80db",
    "accent3": "#79a15e",
    "accent4": "#d35b78",
    "accent5": "#5aacd3",
    "dark_bg": "#d8dae5",
    "light_bg": "#e0e2ed",
    "button_bg": "#e0e2ed",
    "button_hover": "#c6c9d8",
    "button_border": "#bbbfd1",
}

# 즐겨찾기 전용 색상
FAVORITES_COLORS = {
    "light": {
        "bg": "#fff8dc",
        "hover": "#ffebcd",
        "border": "#daa520",
        "container_bg": "#fffacd",
    },
    "dark": {
        "bg": "#3a3a1a",
        "hover": "#4a4a2a",
        "border": "#8b7500",
        "container_bg": "#3a3a2a",
    },
}

# 카테고리별 색상 매핑
CATEGORY_COLORS = [
    "accent2",
    "accent2",
    "accent2",
    "accent1",
    "accent1",
    "accent3",
    "accent3",
    "accent5",
    "accent4",
    "accent4",
    "accent1",
    "accent2",
]

# 폰트 우선순위
FONT_PREFERENCES = ["JetBrains Mono", "Inter", "Consolas", "Courier New", "monospace"]
