# ui_builder.py
"""
UI 섹션 생성 및 스타일 관리
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QScrollArea,
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon
from components import QFlowLayout, FavoritesDropZone, ToggleSwitch
from constants import SCALE_LIMITS, CATEGORY_COLORS
from settings_manager import SettingsManager


class UIBuilder:
    """UI 구성 요소 생성 클래스"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.separators = []

    def setup_window(self):
        """윈도우 기본 설정"""
        try:
            icon_path = SettingsManager.get_resource_path("app_icon.ico")
            self.main_window.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"아이콘 설정 오류: {e}")

        self.main_window.setWindowTitle("Greek letters & Mathematical Symbols")

        # 최대화 버튼 제거
        self.main_window.setWindowFlags(
            self.main_window.windowFlags() & ~Qt.WindowMaximizeButtonHint
        )

        # 크기 제한 설정
        from constants import WINDOW_SETTINGS

        self.main_window.setGeometry(
            100, 100, WINDOW_SETTINGS["base_width"], WINDOW_SETTINGS["base_height"]
        )
        self.main_window.setMinimumSize(
            WINDOW_SETTINGS["min_width"], WINDOW_SETTINGS["min_height"]
        )
        self.main_window.setMaximumSize(
            WINDOW_SETTINGS["max_width"], WINDOW_SETTINGS["max_height"]
        )

    def create_output_mode_section(self):
        """출력 모드 선택 영역 생성"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 5, 0, 5)

        # 출력 모드 라벨
        output_mode_label = QLabel("Output Mode: ")
        output_mode_label.setFont(
            QFont(self.main_window.default_font_family, 10, QFont.Bold)
        )
        layout.addWidget(output_mode_label)
        self.main_window.output_mode_label = output_mode_label

        # 라디오 버튼 그룹
        mode_group = QButtonGroup(self.main_window)

        # 일반 모드 라디오 버튼
        regular_mode_radio = QRadioButton("Regular")
        regular_mode_radio.setChecked(not self.main_window.latex_mode)
        regular_mode_radio.toggled.connect(self.main_window.toggle_output_mode)
        mode_group.addButton(regular_mode_radio)
        layout.addWidget(regular_mode_radio)
        self.main_window.regular_mode_radio = regular_mode_radio

        # LaTeX 모드 라디오 버튼
        latex_mode_radio = QRadioButton("LaTeX")
        latex_mode_radio.setChecked(self.main_window.latex_mode)
        latex_mode_radio.toggled.connect(self.main_window.toggle_output_mode)
        mode_group.addButton(latex_mode_radio)
        layout.addWidget(latex_mode_radio)
        self.main_window.latex_mode_radio = latex_mode_radio

        self.main_window.mode_group = mode_group

        layout.addStretch()

        # 설정 버튼
        settings_button = QPushButton("⛯")
        settings_button.setFixedSize(30, 30)
        settings_button.setToolTip("Settings")
        settings_button.clicked.connect(self.main_window.show_settings_menu)
        layout.addWidget(settings_button)
        self.main_window.settings_button = settings_button

        return container

    def create_recent_section(self):
        """최근 사용 항목 섹션 생성"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # 최근 사용 라벨
        recent_label = QLabel("Recently used")
        recent_label.setFont(
            QFont(self.main_window.default_font_family, 10, QFont.Bold)
        )
        layout.addWidget(recent_label)
        self.main_window.recent_label = recent_label

        # 스크롤 없는 컨테이너 위젯 (배경 스타일만 적용)
        recent_container_widget = QWidget()
        recent_container_widget.setStyleSheet(
            f"""
            background-color: {self._get_current_theme()['light_bg']};
            border: 1px solid {self._get_current_theme()['button_border']};
            border-radius: 4px;
            padding: 3px;
        """
        )

        recent_layout = QFlowLayout(recent_container_widget)
        recent_layout.setContentsMargins(3, 3, 3, 3)
        recent_container_widget.setMinimumHeight(50)

        layout.addWidget(recent_container_widget)

        # 참조 저장
        self.main_window.recent_container_widget = recent_container_widget
        self.main_window.recent_layout = recent_layout

        return container

    def create_favorites_section(self):
        """즐겨찾기 섹션 생성"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 5, 0, 5)

        # 즐겨찾기 헤더 (라벨 + 접기/펼치기 버튼)
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        # 접기/펼치기 버튼
        favorites_toggle_button = QPushButton(
            "▼" if not self.main_window.favorites_collapsed else "▶"
        )
        favorites_toggle_button.setFixedSize(20, 20)
        favorites_toggle_button.clicked.connect(
            self.main_window.toggle_favorites_section
        )
        header_layout.addWidget(favorites_toggle_button)
        self.main_window.favorites_toggle_button = favorites_toggle_button

        # 즐겨찾기 라벨
        favorites_label = QLabel("Favorites")
        favorites_label.setFont(
            QFont(self.main_window.default_font_family, 10, QFont.Bold)
        )
        header_layout.addWidget(favorites_label)
        self.main_window.favorites_label = favorites_label

        header_layout.addStretch()
        layout.addWidget(header_container)

        # 즐겨찾기 컨테이너 (드롭 존) - 배경색을 확실히 보이게 하기 위해 초기 스타일 설정
        favorites_container = FavoritesDropZone(self.main_window)
        
        # 초기 배경색 설정 (나중에 style_manager에서 덮어씀)
        initial_bg = "#fffacd" if not self.main_window.is_dark_mode else "#3a3a2a"
        initial_border = "#daa520" if not self.main_window.is_dark_mode else "#8b7500"
        
        favorites_container.setStyleSheet(f"""
            QWidget {{
                background-color: {initial_bg};
                border: 2px solid {initial_border};
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
            }}
        """)

        favorites_layout = QFlowLayout(favorites_container)
        favorites_layout.setContentsMargins(5, 5, 5, 5)

        # 초기 접기/펼치기 상태 적용
        favorites_container.setVisible(not self.main_window.favorites_collapsed)
        favorites_container.setMinimumHeight(50)
        
        layout.addWidget(favorites_container)

        # 참조 저장
        self.main_window.favorites_container = favorites_container
        self.main_window.favorites_layout = favorites_layout

        return container

    def create_category_buttons(self):
        """카테고리 버튼 생성 - 스크롤 가능"""
        # 카테고리 스크롤 영역 생성
        category_scroll = QScrollArea()
        category_scroll.setWidgetResizable(True)
        category_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        category_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        category_scroll.setFrameShape(QFrame.StyledPanel)
        # 스타일 적용 추가
        category_scroll.setStyleSheet(self._create_scroll_area_style())

        # 카테고리 컨테이너 위젯
        category_container = QWidget()
        # 컨테이너 스타일 적용 추가
        category_container.setStyleSheet(
            f"background-color: {self._get_current_theme()['light_bg']};"
        )
        button_layout = QVBoxLayout(category_container)
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(5, 5, 5, 5)

        from symbol_data import SymbolData

        category_buttons = []
        for i, (category_name, method_name) in enumerate(SymbolData.CATEGORIES):
            button = QPushButton(category_name)
            button.setFont(QFont(self.main_window.default_font_family, 8))
            button.setFixedHeight(40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # 이벤트 연결 - lambda의 기본값 바인딩 사용
            button.clicked.connect(
                lambda checked, method=method_name, idx=i: self.main_window.show_symbols_menu(
                    method, idx
                )
            )

            button_layout.addWidget(button)
            category_buttons.append(button)

        # 스크롤 영역에 컨테이너 설정
        category_scroll.setWidget(category_container)

        # 참조 저장
        self.main_window.category_scroll = category_scroll
        self.main_window.button_layout = button_layout
        self.main_window.category_buttons = category_buttons

        return category_scroll

    def create_separator(self):
        """구분선 생성"""
        line = QWidget()
        line.setFixedHeight(1)
        self.separators.append(line)
        return line

    def create_status_bar(self):
        """상태바 생성"""
        self.main_window.statusBar().showMessage("Select a symbol to copy to clipboard")

    def _get_current_theme(self):
        """현재 테마 반환"""
        from constants import DARK_THEME, LIGHT_THEME

        return DARK_THEME if self.main_window.is_dark_mode else LIGHT_THEME

    def _create_scroll_area_style(self):
        """카테고리 스크롤 영역 스타일 생성"""
        theme = self._get_current_theme()
        return f"""
            QScrollArea {{
                border: 1px solid {theme['button_border']};
                border-radius: 4px;
                background-color: {theme['light_bg']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {theme['dark_bg']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme['button_border']};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """
