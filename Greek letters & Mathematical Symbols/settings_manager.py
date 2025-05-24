# settings_manager.py
"""
설정 파일 저장/불러오기 및 커스텀 심볼 관리
"""

import os
import json
import subprocess
import platform
from pathlib import Path
from PyQt5.QtGui import QFontDatabase


class SettingsManager:
    """설정 관리 클래스"""

    def __init__(self):
        self.config_file = os.path.join(self.get_config_dir(), "settings.json")
        self.custom_symbols_dir = os.path.join(self.get_config_dir(), "custom_symbols")
        self.setup_custom_symbols_folder()

    def get_config_dir(self):
        """설정 파일 디렉토리 경로 반환"""
        if os.name == "nt":
            config_dir = os.path.join(os.environ["APPDATA"], "GreekLetterFloat")
        else:
            config_dir = os.path.join(os.path.expanduser("~"), ".greekletterfloat")

        Path(config_dir).mkdir(exist_ok=True)
        return config_dir

    def get_custom_symbols_dir(self):
        """커스텀 심볼 폴더 경로 반환"""
        return self.custom_symbols_dir

    def setup_custom_symbols_folder(self):
        """커스텀 심볼 폴더 초기 설정"""
        if not os.path.exists(self.custom_symbols_dir):
            os.makedirs(self.custom_symbols_dir)
            self.create_default_custom_files()
            self.create_readme_file()

    def create_default_custom_files(self):
        """기본 커스텀 JSON 파일들 생성 (기존 카테고리들)"""
        default_categories = [
            {
                "filename": "10_script_letters.json",
                "content": {
                    "category_info": {
                        "name": "Roman Script Letters",
                        "description": "Mathematical script and calligraphic letters",
                        "order": 10,
                        "color": "#bb9af7",
                    },
                    "symbols": [
                        {"symbol": "𝒜", "latex": "\\mathcal{A}", "name": "Script A"},
                        {"symbol": "ℬ", "latex": "\\mathcal{B}", "name": "Script B"},
                        {"symbol": "𝒞", "latex": "\\mathcal{C}", "name": "Script C"},
                        {"symbol": "𝒟", "latex": "\\mathcal{D}", "name": "Script D"},
                        {"symbol": "ℰ", "latex": "\\mathcal{E}", "name": "Script E"},
                        {"symbol": "ℱ", "latex": "\\mathcal{F}", "name": "Script F"},
                        {"symbol": "𝒢", "latex": "\\mathcal{G}", "name": "Script G"},
                        {"symbol": "ℋ", "latex": "\\mathcal{H}", "name": "Script H"},
                        {"symbol": "ℐ", "latex": "\\mathcal{I}", "name": "Script I"},
                        {"symbol": "𝒥", "latex": "\\mathcal{J}", "name": "Script J"},
                        {"symbol": "𝒦", "latex": "\\mathcal{K}", "name": "Script K"},
                        {"symbol": "ℒ", "latex": "\\mathcal{L}", "name": "Script L"},
                        {"symbol": "ℳ", "latex": "\\mathcal{M}", "name": "Script M"},
                        {"symbol": "𝒩", "latex": "\\mathcal{N}", "name": "Script N"},
                        {"symbol": "𝒪", "latex": "\\mathcal{O}", "name": "Script O"},
                        {"symbol": "𝒫", "latex": "\\mathcal{P}", "name": "Script P"},
                        {"symbol": "𝒬", "latex": "\\mathcal{Q}", "name": "Script Q"},
                        {"symbol": "ℛ", "latex": "\\mathcal{R}", "name": "Script R"},
                        {"symbol": "𝒮", "latex": "\\mathcal{S}", "name": "Script S"},
                        {"symbol": "𝒯", "latex": "\\mathcal{T}", "name": "Script T"},
                        {"symbol": "𝒰", "latex": "\\mathcal{U}", "name": "Script U"},
                        {"symbol": "𝒱", "latex": "\\mathcal{V}", "name": "Script V"},
                        {"symbol": "𝒲", "latex": "\\mathcal{W}", "name": "Script W"},
                        {"symbol": "𝒳", "latex": "\\mathcal{X}", "name": "Script X"},
                        {"symbol": "𝒴", "latex": "\\mathcal{Y}", "name": "Script Y"},
                        {"symbol": "𝒵", "latex": "\\mathcal{Z}", "name": "Script Z"},
                    ],
                },
            },
            {
                "filename": "20_math_symbols.json",
                "content": {
                    "category_info": {
                        "name": "Math/Engineering Symbols",
                        "description": "Common mathematical and engineering symbols",
                        "order": 20,
                        "color": "#7aa2f7",
                    },
                    "symbols": [
                        {"symbol": "∑", "latex": "\\sum_{i=1}^{n}", "name": "Sum"},
                        {"symbol": "∏", "latex": "\\prod_{i=1}^{n}", "name": "Product"},
                        {"symbol": "∂", "latex": "\\partial", "name": "Partial"},
                        {"symbol": "∇", "latex": "\\nabla", "name": "Nabla"},
                        {"symbol": "∞", "latex": "\\infty", "name": "Infinity"},
                        {"symbol": "∫", "latex": "\\int_{a}^{b}", "name": "Integral"},
                        {"symbol": "≈", "latex": "\\approx", "name": "Approximately"},
                        {"symbol": "≠", "latex": "\\neq", "name": "Not Equal"},
                        {"symbol": "≤", "latex": "\\leq", "name": "Less Than or Equal"},
                        {
                            "symbol": "≥",
                            "latex": "\\geq",
                            "name": "Greater Than or Equal",
                        },
                        {"symbol": "∈", "latex": "\\in", "name": "Element Of"},
                        {"symbol": "⊂", "latex": "\\subset", "name": "Subset"},
                        {"symbol": "∩", "latex": "\\cap", "name": "Intersection"},
                        {"symbol": "∪", "latex": "\\cup", "name": "Union"},
                        {"symbol": "→", "latex": "\\rightarrow", "name": "Right Arrow"},
                        {"symbol": "←", "latex": "\\leftarrow", "name": "Left Arrow"},
                        {
                            "symbol": "↔",
                            "latex": "\\leftrightarrow",
                            "name": "Double Arrow",
                        },
                        {"symbol": "≡", "latex": "\\equiv", "name": "Identical To"},
                        {"symbol": "≅", "latex": "\\cong", "name": "Congruent To"},
                        {"symbol": "≜", "latex": "\\triangleq", "name": "Defined As"},
                    ],
                },
            },
            {
                "filename": "30_physics_symbols.json",
                "content": {
                    "category_info": {
                        "name": "Physics Symbols",
                        "description": "Physics and quantum mechanics symbols",
                        "order": 30,
                        "color": "#f7768e",
                    },
                    "symbols": [
                        {"symbol": "ℏ", "latex": "\\hbar", "name": "h-bar"},
                        {"symbol": "ψ", "latex": "\\psi", "name": "wavefunction"},
                        {"symbol": "Ψ", "latex": "\\Psi", "name": "Wavefunction"},
                        {
                            "symbol": "⟨ϕ|ψ⟩",
                            "latex": "\\langle \\phi | \\psi \\rangle",
                            "name": "Bracket Notation",
                        },
                        {"symbol": "⊗", "latex": "\\otimes", "name": "Tensor Product"},
                        {
                            "symbol": "†",
                            "latex": "^\\dagger",
                            "name": "Hermitian Conjugate",
                        },
                        {"symbol": "°", "latex": "^\\circ", "name": "Degree"},
                        {"symbol": "∮", "latex": "\\oint", "name": "Contour Integral"},
                        {"symbol": "∇²", "latex": "\\nabla^2", "name": "Laplacian"},
                    ],
                },
            },
        ]

        for category in default_categories:
            file_path = os.path.join(self.custom_symbols_dir, category["filename"])
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(category["content"], f, ensure_ascii=False, indent=2)

    def create_readme_file(self):
        """사용법 설명 README 파일 생성"""
        readme_content = """# Custom Symbols Guide

## JSON File Structure:
```json
{
  "category_info": {
    "name": "My Custom Category",
    "description": "Optional description of this category",
    "order": 100,
    "color": "#7aa2f7"
  },
  "symbols": [
    {
      "symbol": "∮",
      "latex": "\\\\oint",
      "name": "contour integral"
    },
    {
      "symbol": "⟨ψ|φ⟩",
      "latex": "\\\\langle \\\\psi | \\\\phi \\\\rangle",
      "name": "inner product"
    }
  ]
}
```

## Instructions:
1. Create new .json files in this folder
2. Use the structure shown above
3. **Order**: Lower numbers appear first (10, 20, 30...)
4. **Color**: Hex color codes for category border color
5. **LaTeX**: Use double backslashes (\\\\alpha, not \\alpha)
6. Save files and restart the app to see changes

## Tips:
- File names starting with numbers help with organization
- Invalid JSON files will be ignored with error messages
- You can copy/paste symbols from other sources
- Use the "Add New Category" button for a template
- Edit existing files or delete them as needed

## Available Colors:
- Blue: #7aa2f7
- Purple: #bb9af7  
- Green: #9ece6a
- Red: #f7768e
- Cyan: #7dcfff
- Orange: #ff9e64
"""

        readme_path = os.path.join(self.custom_symbols_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

    def create_new_category_template(self):
        """새로운 카테고리 템플릿 파일 생성"""
        # 기존 파일들의 번호 확인하여 다음 번호 결정
        existing_numbers = []
        for filename in os.listdir(self.custom_symbols_dir):
            if filename.endswith(".json") and filename[0].isdigit():
                try:
                    num = int(filename.split("_")[0])
                    existing_numbers.append(num)
                except:
                    pass

        next_num = max(existing_numbers, default=90) + 10

        template_filename = f"{next_num:02d}_new_category.json"
        template_content = {
            "category_info": {
                "name": "My New Category",
                "description": "Description of my custom symbols",
                "order": next_num,
                "color": "#7aa2f7",
            },
            "symbols": [
                {"symbol": "∮", "latex": "\\oint", "name": "example symbol"},
                {
                    "symbol": "⟨ψ⟩",
                    "latex": "\\langle \\psi \\rangle",
                    "name": "another example",
                },
            ],
        }

        file_path = os.path.join(self.custom_symbols_dir, template_filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(template_content, f, ensure_ascii=False, indent=2)

        return file_path

    def load_custom_symbols(self):
        """커스텀 심볼 JSON 파일들 로드"""
        custom_categories = []
        invalid_files = []

        if not os.path.exists(self.custom_symbols_dir):
            return custom_categories, invalid_files

        for filename in os.listdir(self.custom_symbols_dir):
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(self.custom_symbols_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # JSON 구조 검증
                if self.validate_custom_json(data):
                    data["_filename"] = filename  # 파일명 저장
                    custom_categories.append(data)
                else:
                    invalid_files.append((filename, "Invalid JSON structure"))

            except json.JSONDecodeError as e:
                invalid_files.append((filename, f"JSON parsing error: {str(e)}"))
            except Exception as e:
                invalid_files.append((filename, f"Error: {str(e)}"))

        # 정렬: order 값으로 먼저, 같으면 파일명으로
        custom_categories.sort(
            key=lambda x: (
                x.get("category_info", {}).get("order", 999),
                x.get("_filename", ""),
            )
        )

        return custom_categories, invalid_files

    def validate_custom_json(self, data):
        """커스텀 JSON 구조 검증"""
        try:
            # 필수 필드 확인
            if "category_info" not in data or "symbols" not in data:
                return False

            category_info = data["category_info"]
            if "name" not in category_info:
                return False

            # symbols 배열 검증
            symbols = data.get("symbols", [])
            if not isinstance(symbols, list):
                return False

            for symbol in symbols:
                if not isinstance(symbol, dict):
                    return False
                if not all(key in symbol for key in ["symbol", "latex", "name"]):
                    return False

            return True
        except:
            return False

    def open_custom_symbols_folder(self):
        """커스텀 심볼 폴더를 시스템 파일 탐색기로 열기"""
        try:
            if platform.system() == "Windows":
                os.startfile(self.custom_symbols_dir)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.custom_symbols_dir])
            else:  # Linux
                subprocess.run(["xdg-open", self.custom_symbols_dir])
            return True
        except Exception as e:
            print(f"폴더 열기 오류: {e}")
            return False

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
            print(f"설정 불러우기 실패: {e}")

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
