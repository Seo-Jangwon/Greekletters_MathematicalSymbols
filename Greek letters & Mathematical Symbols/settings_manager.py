# settings_manager.py
"""
설정 파일 저장/불러오기 및 테마 관리
"""

import os
import json
from pathlib import Path
from PyQt5.QtGui import QFontDatabase


class SettingsManager:
    """설정 관리 클래스"""

    def __init__(self):
        self.config_file = os.path.join(self.get_config_dir(), "settings.json")

    def get_config_dir(self):
        """설정 파일 디렉토리 경로 반환"""
        if os.name == "nt":
            config_dir = os.path.join(os.environ["APPDATA"], "GreekLetterFloat")
        else:
            config_dir = os.path.join(os.path.expanduser("~"), ".greekletterfloat")

        Path(config_dir).mkdir(exist_ok=True)
        return config_dir

    def save_settings(self, app_instance):
        """설정을 JSON 파일로 저장"""
        settings = {
            "favorites": app_instance.favorites,
            "favorites_collapsed": app_instance.favorites_collapsed,
            "recent_symbols": app_instance.recent_symbols,
            "is_dark_mode": app_instance.is_dark_mode,
            "always_on_top": app_instance.is_always_on_top,
            "latex_mode": app_instance.latex_mode,
            "window_size": [app_instance.width(), app_instance.height()],
        }

        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"설정 저장 실패: {e}")

    def load_settings(self):
        """JSON 파일에서 설정 불러오기"""
        default_settings = {
            "favorites": [],
            "favorites_collapsed": True,
            "recent_symbols": [],
            "is_dark_mode": False,
            "always_on_top": False,
            "latex_mode": False,
            "window_size": [450, 600],
        }

        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                # 기본값과 병합
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
        except Exception as e:
            print(f"설정 불러오기 실패: {e}")

        return default_settings

    @staticmethod
    def get_available_font(font_options):
        """사용 가능한 첫 번째 폰트 반환"""
        font_db = QFontDatabase()
        available_fonts = font_db.families()

        for font in font_options:
            for available_font in available_fonts:
                if font.lower() == available_font.lower():
                    return available_font

        return font_options[-1]

    @staticmethod
    def get_resource_path(relative_path):
        """리소스 경로를 가져오는 함수"""
        import sys

        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
