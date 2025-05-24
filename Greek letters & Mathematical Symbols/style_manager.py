# style_manager.py
"""
테마 및 스타일 관리
"""

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont
from constants import (
    DARK_THEME,
    FAVORITES_COLORS,
    LIGHT_THEME,
    SCALE_LIMITS,
    CATEGORY_COLORS,
)
from components import DraggableButton


class StyleManager:
    """스타일 및 테마 관리 클래스"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.current_theme = LIGHT_THEME

    def get_current_theme(self):
        """현재 테마 반환"""
        return DARK_THEME if self.main_window.is_dark_mode else LIGHT_THEME

    def get_favorites_colors(self):
        """즐겨찾기 전용 색상 반환"""
        mode = "dark" if self.main_window.is_dark_mode else "light"
        return FAVORITES_COLORS[mode]

    def create_favorites_container_style(self):
        """즐겨찾기 컨테이너 스타일 생성"""
        colors = self.get_favorites_colors()
        return f"""
            background-color: {colors['container_bg']};
            border: 1px solid {colors['border']};
            border-radius: 4px;
            padding: 3px;
        """

    def create_favorites_button_style(self):
        """즐겨찾기 버튼 스타일 생성"""
        colors = self.get_favorites_colors()
        padding_v = self.main_window.calculate_scaled_size(4, "padding")
        padding_h = self.main_window.calculate_scaled_size(6, "padding")

        return f"""
            QPushButton {{
                background-color: {colors['bg']};
                color: {self.current_theme['foreground']};
                padding: {padding_v}px {padding_h}px;
                margin: 2px;
                border: 1px solid {colors['border']};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {colors['hover']};
                border: 1px solid {colors['border']};
            }}
        """

    def apply_favorites_styles(self):
        """즐겨찾기 관련 모든 스타일 적용"""

        # 컨테이너 스타일 적용
        if hasattr(self.main_window, "favorites_container"):
            colors = self.get_favorites_colors()
            container_style = f"""
                QWidget {{
                    background-color: {colors['container_bg']};
                    border: 2px solid {colors['border']};
                    border-radius: 6px;
                    padding: 8px;
                    margin: 2px;
                }}
            """
            self.main_window.favorites_container.setStyleSheet(container_style)

            # 강제로 업데이트
            self.main_window.favorites_container.update()
            self.main_window.favorites_container.repaint()
        else:
            print("favorites_container not found!")  # 디버깅용

    def apply_main_theme(self):
        """메인 윈도우 테마 적용"""
        self.current_theme = self.get_current_theme()

        app = QApplication.instance()
        app.setStyle("Fusion")

        self.main_window.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {self.current_theme['background']};
                color: {self.current_theme['foreground']};
            }}
            QWidget {{
                background-color: {self.current_theme['background']};
                color: {self.current_theme['foreground']};
            }}
            QMenu {{
                background-color: {self.current_theme['dark_bg']};
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['button_border']};
            }}
            QMenu::item {{
                padding: 6px 25px 6px 25px;
            }}
            QMenu::item:selected {{
                background-color: {self.current_theme['button_hover']};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {self.current_theme['button_border']};
                margin: 5px 15px 5px 15px;
            }}
            QToolTip {{
                background-color: {self.current_theme['dark_bg']};
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['accent2']};
                padding: 3px;
                border-radius: 3px;
                opacity: 200;
            }}
            QFrame {{
                background-color: {self.current_theme['background']};
                color: {self.current_theme['foreground']};
            }}
        """
        )

    def apply_component_styles(self):
        """개별 컴포넌트 스타일 적용"""
        # 중앙 위젯 배경색
        central_widget = self.main_window.centralWidget()
        if central_widget:
            central_widget.setStyleSheet(
                f"background-color: {self.current_theme['background']};"
            )

        # 라벨들
        if hasattr(self.main_window, "output_mode_label"):
            self.main_window.output_mode_label.setStyleSheet(
                f"color: {self.current_theme['foreground']};"
            )
        if hasattr(self.main_window, "recent_label"):
            self.main_window.recent_label.setStyleSheet(
                f"color: {self.current_theme['foreground']};"
            )
        if hasattr(self.main_window, "favorites_label"):
            self.main_window.favorites_label.setStyleSheet(
                f"color: {self.current_theme['foreground']};"
            )

        # 라디오 버튼들
        radio_style = self.create_radio_button_style()
        if hasattr(self.main_window, "regular_mode_radio"):
            self.main_window.regular_mode_radio.setStyleSheet(radio_style)
        if hasattr(self.main_window, "latex_mode_radio"):
            self.main_window.latex_mode_radio.setStyleSheet(radio_style)

        # 설정 버튼
        if hasattr(self.main_window, "settings_button"):
            self.main_window.settings_button.setStyleSheet(
                self.create_settings_button_style()
            )

        # 컨테이너들
        if hasattr(self.main_window, "recent_container_widget"):
            theme = self.get_current_theme()
            self.main_window.recent_container_widget.setStyleSheet(
                f"""
                background-color: {theme['light_bg']};
                border: 1px solid {theme['button_border']};
                border-radius: 4px;
                padding: 3px;
            """
            )

        if hasattr(self.main_window, "category_scroll"):
            self.main_window.category_scroll.setStyleSheet(
                self.create_scroll_area_style()
            )
            category_container = self.main_window.category_scroll.widget()
            if category_container:
                category_container.setStyleSheet(
                    f"background-color: {self.current_theme['light_bg']};"
                )

        # 카테고리 버튼들
        if hasattr(self.main_window, "category_buttons"):
            for i, button in enumerate(self.main_window.category_buttons):
                accent_color = self.get_category_color(i)
                button.setStyleSheet(self.create_category_button_style(accent_color))

        # 상태바
        self.main_window.statusBar().setStyleSheet(
            f"""
            background-color: {self.current_theme['light_bg']};
            color: {self.current_theme['foreground']};
        """
        )

        # 즐겨찾기 토글 버튼
        if hasattr(self.main_window, "favorites_toggle_button"):
            self.main_window.favorites_toggle_button.setStyleSheet(
                f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    color: {self.current_theme['foreground']};
                    font-size: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    color: {self.current_theme['accent2']};
                }}
            """
            )

        # 구분선들
        if hasattr(self.main_window, "ui_builder") and hasattr(
            self.main_window.ui_builder, "separators"
        ):
            for separator in self.main_window.ui_builder.separators:
                separator.setStyleSheet(
                    f"background-color: {self.current_theme['button_border']};"
                )

    def create_radio_button_style(self):
        """라디오 버튼 스타일 생성"""
        return f"""
            QRadioButton {{
                color: {self.current_theme['foreground']};
                spacing: 5px;
            }}
            QRadioButton::indicator {{
                width: 13px;
                height: 13px;
                border-radius: 7px;
                border: 1px solid {self.current_theme['accent2']};
            }}
            QRadioButton::indicator:checked {{
                background-color: {self.current_theme['accent2']};
                border: 2px solid {self.current_theme['dark_bg']};
            }}
        """

    def create_settings_button_style(self):
        """설정 버튼 스타일 생성"""
        return f"""
            QPushButton {{
                background-color: {self.current_theme['button_bg']};
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['button_border']};
                border-radius: 4px;
                padding: 2px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
        """

    def create_scroll_area_style(self):
        """스크롤 영역 스타일 생성"""
        return f"""
            QScrollArea {{
                border: 1px solid {self.current_theme['button_border']};
                border-radius: 4px;
                background-color: {self.current_theme['light_bg']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {self.current_theme['dark_bg']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.current_theme['button_border']};
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

    def create_category_button_style(self, accent_color):
        """카테고리 버튼 스타일 생성"""
        return f"""
            QPushButton {{
                background-color: {self.current_theme['button_bg']};
                color: {self.current_theme['foreground']};
                border: 1px solid {accent_color};
                border-radius: 4px;
                padding: 8px 12px;
                margin: 2px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {accent_color};
                color: {self.current_theme['dark_bg']};
            }}
        """

    def create_button_style(self, padding_v, padding_h, margin=2, border_color=None):
        """일반 버튼 스타일 생성"""
        border = border_color or self.current_theme["button_border"]
        return f"""
            QPushButton {{
                background-color: {self.current_theme['button_bg']};
                color: {self.current_theme['foreground']};
                border: 1px solid {border};
                border-radius: 4px;
                padding: {padding_v}px {padding_h}px;
                margin: {margin}px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {border};
                color: {self.current_theme['dark_bg']};
            }}
        """

    def get_category_color(self, index):
        """카테고리 인덱스에 따른 강조색 반환"""
        color_key = CATEGORY_COLORS[index % len(CATEGORY_COLORS)]
        return self.current_theme[color_key]

    def apply_menu_style(self, menu):
        """메뉴 스타일 적용"""
        menu.setStyleSheet(
            f"""
            QMenu {{
                background-color: {self.current_theme['dark_bg']};
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['accent2']};
            }}
            QMenu::item:selected {{
                background-color: {self.current_theme['button_hover']};
            }}
        """
        )

    def apply_settings_menu_style(self, menu):
        """설정 메뉴 스타일 적용"""
        menu.setStyleSheet(
            f"""
            QMenu {{
                background-color: {self.current_theme['dark_bg']};
                color: {self.current_theme['foreground']};
                border: 1px solid {self.current_theme['accent2']};
                padding: 10px;
                min-width: 200px;
            }}
            QMenu::item {{
                padding: 0px;
                margin: 0px;
            }}
        """
        )

    def update_recent_buttons_style(self):
        """최근 사용 버튼 스타일 업데이트"""
        recent_size = self.main_window.calculate_scaled_size(9, "font")
        button_height = self.main_window.calculate_scaled_size(30, "height")
        padding_h = self.main_window.calculate_scaled_size(6, "padding")
        padding_v = self.main_window.calculate_scaled_size(4, "padding")

        for i in range(self.main_window.recent_layout.count()):
            item = self.main_window.recent_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, DraggableButton):
                    widget.setFont(
                        QFont(self.main_window.default_font_family, recent_size)
                    )
                    widget.setMinimumHeight(button_height)
                    widget.setStyleSheet(
                        f"""
                        QPushButton {{
                            background-color: {self.current_theme['button_bg']};
                            color: {self.current_theme['foreground']};
                            padding: {padding_v}px {padding_h}px;
                            margin: 2px;
                            border: 1px solid {self.current_theme['button_border']};
                            border-radius: 4px;
                        }}
                        QPushButton:hover {{
                            background-color: {self.current_theme['button_hover']};
                            border: 1px solid {self.current_theme['accent2']};
                        }}
                    """
                    )

    def update_category_section_styles(self):
        """카테고리 섹션의 스타일만 업데이트"""
        # Add/Edit/Reload 버튼들 업데이트
        if hasattr(self.main_window, "add_custom_button"):
            button_style = self.main_window.ui_builder.create_control_button_style()
            self.main_window.add_custom_button.setStyleSheet(button_style)
            self.main_window.edit_custom_button.setStyleSheet(button_style)
            reload_style = button_style.replace("padding: 4px 8px;", "padding: 4px;")
            self.main_window.reload_custom_button.setStyleSheet(reload_style)

        # Basic, Custom 라벨들 업데이트
        # button_layout 내의 모든 QLabel 찾아서 업데이트
        if hasattr(self.main_window, "button_layout"):
            for i in range(self.main_window.button_layout.count()):
                item = self.main_window.button_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QLabel):
                        widget.setStyleSheet(
                            f"""
                            QLabel {{
                                color: {self.current_theme['foreground']};
                                font-weight: bold;
                                padding: 5px 8px 2px 8px;
                                margin-top: 5px;
                            }}
                        """
                        )
                    elif (
                        isinstance(widget, QWidget)
                        and widget.objectName() == "category_separator"
                    ):
                        widget.setStyleSheet(
                            f"""
                            QWidget {{
                                background-color: {self.current_theme['button_border']};
                                margin: 8px 5px;
                            }}
                        """
                        )
