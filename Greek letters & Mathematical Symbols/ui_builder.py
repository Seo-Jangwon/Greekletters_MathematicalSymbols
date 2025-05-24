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
from constants import SCALE_LIMITS, CATEGORY_COLORS, CONTAINER_SETTINGS
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

        # 최소 높이 설정 적용
        recent_container_widget.setMinimumHeight(
            CONTAINER_SETTINGS["recent_min_height"]
        )

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

        # 즐겨찾기 컨테이너 (드롭 존)
        favorites_container = FavoritesDropZone(self.main_window)

        # 최소 높이 설정 적용
        favorites_container.setMinimumHeight(CONTAINER_SETTINGS["favorites_min_height"])

        # 초기 배경색 설정 (나중에 style_manager에서 덮어씀)
        initial_bg = "#fffacd" if not self.main_window.is_dark_mode else "#3a3a2a"
        initial_border = "#daa520" if not self.main_window.is_dark_mode else "#8b7500"

        favorites_container.setStyleSheet(
            f"""
            QWidget {{
                background-color: {initial_bg};
                border: 2px solid {initial_border};
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
            }}
        """
        )

        favorites_layout = QFlowLayout(favorites_container)
        favorites_layout.setContentsMargins(5, 5, 5, 5)

        # 초기 접기/펼치기 상태 적용
        favorites_container.setVisible(not self.main_window.favorites_collapsed)

        layout.addWidget(favorites_container)

        # 참조 저장
        self.main_window.favorites_container = favorites_container
        self.main_window.favorites_layout = favorites_layout

        return container

    def create_custom_symbols_controls(self):
        """커스텀 심볼 관리 버튼들 생성"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 5, 0, 5)
        
        # Custom Symbols 라벨
        custom_label = QLabel("Categories")
        custom_label.setFont(QFont(self.main_window.default_font_family, 10, QFont.Bold))
        layout.addWidget(custom_label)
        
        layout.addStretch()
        
        # 버튼 스타일 정의
        button_style = self.create_control_button_style()
        
        # Add 버튼
        add_button = QPushButton("Add")
        add_button.setFixedSize(60, 25)
        add_button.setToolTip("Create new custom category template")
        add_button.setStyleSheet(button_style)
        add_button.clicked.connect(self.main_window.add_custom_category)
        layout.addWidget(add_button)
        
        # Edit 버튼  
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(60, 25)
        edit_button.setToolTip("Open custom symbols folder")
        edit_button.setStyleSheet(button_style)
        edit_button.clicked.connect(self.main_window.edit_custom_symbols)
        layout.addWidget(edit_button)
        
        # Reload 버튼
        reload_button = QPushButton("↻")
        reload_button.setFixedSize(25, 25)
        reload_button.setToolTip("Reload custom symbols")
        reload_button.setStyleSheet(button_style.replace('padding: 4px 8px;', 'padding: 4px;'))
        reload_button.clicked.connect(self.main_window.reload_custom_symbols)
        layout.addWidget(reload_button)
        
        # 참조 저장
        self.main_window.add_custom_button = add_button
        self.main_window.edit_custom_button = edit_button
        self.main_window.reload_custom_button = reload_button
        
        return container

    def create_control_button_style(self):
        """Add/Edit/Reload 버튼 스타일 생성"""
        theme = self._get_current_theme()
        return f"""
            QPushButton {{
                background-color: {theme['button_bg']};
                color: {theme['foreground']};
                border: 1px solid {theme['button_border']};
                border-radius: 4px;
                padding: 4px 8px;
                font-family: {self.main_window.default_font_family};
                font-size: 8pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
                border: 1px solid {theme['accent2']};
            }}
            QPushButton:pressed {{
                background-color: {theme['accent2']};
                color: {theme['dark_bg']};
            }}
        """

    def create_category_buttons(self):
        """카테고리 버튼 생성 - 스크롤 가능"""
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        # 커스텀 심볼 관리 버튼들 추가
        main_layout.addWidget(self.create_custom_symbols_controls())

        # 카테고리 스크롤 영역 생성
        category_scroll = QScrollArea()
        category_scroll.setWidgetResizable(True)
        category_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        category_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        category_scroll.setFrameShape(QFrame.StyledPanel)
        category_scroll.setStyleSheet(self._create_scroll_area_style())

        # 카테고리 컨테이너 위젯
        category_container = QWidget()
        category_container.setStyleSheet(
            f"background-color: {self._get_current_theme()['light_bg']};"
        )
        button_layout = QVBoxLayout(category_container)
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(5, 5, 5, 5)

        # 카테고리 버튼들은 main_window에서 동적으로 업데이트
        self.main_window.category_container = category_container
        self.main_window.button_layout = button_layout

        # 스크롤 영역에 컨테이너 설정
        category_scroll.setWidget(category_container)

        main_layout.addWidget(category_scroll)

        # 참조 저장
        self.main_window.category_scroll = category_scroll

        return main_container

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
