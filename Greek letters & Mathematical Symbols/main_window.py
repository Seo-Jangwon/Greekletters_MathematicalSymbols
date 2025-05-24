# main_window.py
"""
메인 윈도우 클래스 - 모든 구성 요소를 통합
"""

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMenu,
    QWidgetAction,
    QLabel,
    QSizePolicy,
    QPushButton,
)
from PyQt5.QtCore import pyqtSignal, Qt, QPoint
from PyQt5.QtGui import QResizeEvent, QFont

from constants import SCALE_LIMITS, WINDOW_SETTINGS, FONT_PREFERENCES
from settings_manager import SettingsManager
from ui_builder import UIBuilder
from event_handlers import EventHandlers
from style_manager import StyleManager
from symbol_data import SymbolData
from components import DraggableButton


class SymbolApp(QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 기본 설정 초기화
        self.recent_symbols = []
        self.favorites = []
        self.favorites_collapsed = True
        self.latex_mode = False
        self.is_dark_mode = False
        self.is_always_on_top = False

        # 관리자 클래스들 초기화
        self.settings_manager = SettingsManager()
        self.ui_builder = UIBuilder(self)
        self.event_handlers = EventHandlers(self)
        self.style_manager = StyleManager(self)

        # 폰트 설정
        self.default_font_family = SettingsManager.get_available_font(FONT_PREFERENCES)

        # 스케일 팩터 초기화
        self.scale_factor = 1.0

        # 설정 불러오기
        self.load_settings()

        # UI 생성
        self.init_ui()

        # 테마 적용
        self.apply_current_theme()

        # 초기 리사이즈 이벤트
        self.calculate_scale_factor()
        self.on_resize()

        # 이벤트 연결
        self.resized.connect(self.on_resize)

        # 메뉴 폰트 크기 초기화
        self.symbol_font_size = 16
        self.name_font_size = 10

    def init_ui(self):
        """UI 초기화"""
        # 윈도우 기본 설정
        self.ui_builder.setup_window()

        # 중앙 위젯과 레이아웃 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(10)

        # UI 섹션들 생성
        self.main_layout.addWidget(self.ui_builder.create_output_mode_section())
        self.main_layout.addWidget(self.ui_builder.create_recent_section())
        self.main_layout.addWidget(self.ui_builder.create_separator())
        self.main_layout.addWidget(self.ui_builder.create_favorites_section())
        self.main_layout.addWidget(self.ui_builder.create_separator())
        self.main_layout.addWidget(self.ui_builder.create_category_buttons())

        self.ui_builder.create_status_bar()

        # 초기 데이터 업데이트
        self.update_recent_symbols()
        self.update_favorites_display()

    def load_settings(self):
        """설정 불러오기"""
        settings = self.settings_manager.load_settings()

        self.favorites = settings["favorites"]
        self.favorites_collapsed = settings["favorites_collapsed"]
        self.recent_symbols = settings["recent_symbols"]
        self.is_dark_mode = settings["is_dark_mode"]
        self.is_always_on_top = settings["always_on_top"]
        self.latex_mode = settings["latex_mode"]

        # 윈도우 크기 설정
        if "window_size" in settings:
            width, height = settings["window_size"]
            self.resize(width, height)

    def calculate_scale_factor(self):
        """화면 크기에 따른 스케일 팩터 계산"""
        current_width, current_height = self.width(), self.height()
        width_factor = current_width / WINDOW_SETTINGS["base_width"]
        height_factor = current_height / WINDOW_SETTINGS["base_height"]

        self.scale_factor = min(width_factor, height_factor)
        return self.scale_factor

    def calculate_scaled_size(self, base_size, scale_type="font"):
        """스케일 팩터를 적용한 크기 계산"""
        scaled = int(base_size * self.scale_factor)

        if scale_type == "font":
            return max(
                SCALE_LIMITS["min_font_size"],
                min(SCALE_LIMITS["max_font_size"], scaled),
            )
        elif scale_type == "padding":
            return max(
                SCALE_LIMITS["min_padding"], min(SCALE_LIMITS["max_padding"], scaled)
            )
        elif scale_type == "height":
            return max(
                SCALE_LIMITS["min_button_height"],
                min(SCALE_LIMITS["max_button_height"], scaled),
            )
        return scaled

    def apply_current_theme(self):
        """현재 테마 적용"""
        self.style_manager.apply_main_theme()
        self.style_manager.apply_component_styles()
        self.style_manager.apply_favorites_styles()

        self.update_recent_symbols()
        self.update_favorites_display()
        self.repaint()

    def resizeEvent(self, event: QResizeEvent):
        """윈도우 크기 변경 이벤트 처리"""
        self.resized.emit()
        self.calculate_scale_factor()
        return super().resizeEvent(event)

    def on_resize(self):
        """윈도우 크기에 따라 폰트 및 버튼 크기 조정"""
        self.symbol_font_size = self.calculate_scaled_size(16, "font")
        self.name_font_size = self.calculate_scaled_size(10, "font")
        self.style_manager.update_recent_buttons_style()

    def update_recent_symbols(self):
        """최근 사용 기호 목록 업데이트"""
        # 기존 버튼 제거
        for i in range(self.recent_layout.count()):
            item = self.recent_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                self.recent_layout.removeItem(item)

        # 최근 사용 항목이 없으면 빈 라벨 추가
        if not self.recent_symbols:
            empty_label = QLabel("None")
            empty_label.setStyleSheet(
                f"color: {self.style_manager.current_theme['foreground']};border: 0px solid transparent;"
            )
            self.recent_layout.addWidget(empty_label)
            return

        # 크기 계산
        recent_size = self.calculate_scaled_size(9, "font")
        button_height = self.calculate_scaled_size(30, "height")
        padding_h = self.calculate_scaled_size(6, "padding")
        padding_v = self.calculate_scaled_size(4, "padding")

        # 최근 사용 항목 버튼 생성
        for symbol, latex, name in self.recent_symbols:
            display_text = latex if self.latex_mode else symbol
            tooltip_text = f"Symbol: {symbol}\nLaTeX: {latex}\nName: {name}"
            tooltip_text += "\nDrag to favorites to save\nRight-click for options"

            button = DraggableButton(
                display_text,
                [symbol, latex, name],
                parent=self.recent_container_widget,
                is_favorite=False,
            )

            button.setFont(QFont(self.default_font_family, recent_size))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            button.setMinimumHeight(button_height)
            button.setToolTip(tooltip_text)

            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(
                lambda pos, s=symbol, l=latex, n=name, btn=button: self.event_handlers.show_recent_context_menu(
                    pos, s, l, n, btn
                )
            )

            button.setStyleSheet(
                self.style_manager.create_button_style(padding_v, padding_h)
            )

            button.clicked.connect(
                lambda checked, s=symbol, l=latex, n=name: self.event_handlers.copy_symbol(
                    s, l, n
                )
            )

            self.recent_layout.addWidget(button)

    def update_favorites_display(self):
        """즐겨찾기 표시 업데이트"""

        # 기존 버튼 제거
        for i in range(self.favorites_layout.count()):
            item = self.favorites_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        if not self.favorites:
            empty_label = QLabel("Drag symbols here or click ★ to add favorites")
            empty_label.setStyleSheet(
                f"""
                QLabel {{
                    color: {self.style_manager.current_theme['foreground']}; 
                    font-style: italic;
                    font-family: {self.default_font_family};
                    font-size: 8pt;
                    background-color: transparent;
                    border: 0px solid transparent;
                    padding: 0px;
                    margin: 0px;
                }}
                """
            )
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setWordWrap(True)
            self.favorites_layout.addWidget(empty_label)

            # 즐겨찾기가 없을 때도 배경색 적용
            self.style_manager.apply_favorites_styles()
            return

        # 크기 계산
        favorites_size = self.calculate_scaled_size(9, "font")
        button_height = self.calculate_scaled_size(30, "height")

        # 즐겨찾기 버튼 생성
        for symbol, latex, name in self.favorites:
            display_text = latex if self.latex_mode else symbol
            tooltip_text = f"Symbol: {symbol}\nLaTeX: {latex}\nName: {name}"
            tooltip_text += "\nRight-click to remove\nDrag to reorder"

            button = DraggableButton(
                display_text,
                [symbol, latex, name],
                parent=self.favorites_container,
                is_favorite=True,
            )

            button.setFont(QFont(self.default_font_family, favorites_size))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            button.setMinimumHeight(button_height)
            button.setToolTip(tooltip_text)

            # 통일된 스타일 적용
            button.setStyleSheet(self.style_manager.create_favorites_button_style())

            # 이벤트 설정
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(
                lambda pos, s=symbol, l=latex, n=name, btn=button: self.event_handlers.show_favorite_context_menu(
                    pos, s, l, n, btn
                )
            )

            button.clicked.connect(
                lambda checked, s=symbol, l=latex, n=name: self.event_handlers.copy_symbol(
                    s, l, n
                )
            )

            self.favorites_layout.addWidget(button)

        # 버튼들이 추가된 후 배경색 다시 적용
        self.style_manager.apply_favorites_styles()

    def show_symbols_menu(self, method_name, category_index=0):
        """심볼 메뉴 표시"""
        menu = QMenu(self)
        accent_color = self.style_manager.get_category_color(category_index)

        menu.setStyleSheet(
            f"""
            QMenu {{
                background-color: {self.style_manager.current_theme['dark_bg']};
                color: {self.style_manager.current_theme['foreground']};
                border: 1px solid {accent_color};
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 25px 8px 25px;
            }}
            QMenu::item:selected {{
                background-color: {self.style_manager.current_theme['button_hover']};
            }}
        """
        )

        # 심볼 데이터 가져오기
        symbols = SymbolData.get_category_symbols(method_name)

        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

        # 메뉴 표시
        button = self.sender()
        if button:
            pos = button.mapToGlobal(QPoint(button.width(), 0))
            menu.exec_(pos)

    def create_symbol_menu_item(self, menu, symbol, latex, name):
        """특수문자를 위한 메뉴 항목 생성"""
        action = QWidgetAction(menu)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 2, 5, 2)

        # 심볼 라벨
        symbol_label = QLabel(symbol)
        symbol_font = QFont(self.default_font_family, self.symbol_font_size)
        symbol_label.setFont(symbol_font)
        symbol_label.setStyleSheet(
            f"color: {self.style_manager.current_theme['foreground']};"
        )
        symbol_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 이름 라벨
        name_label = QLabel(f"({name})")
        name_font = QFont(self.default_font_family, self.name_font_size)
        name_label.setFont(name_font)
        name_label.setStyleSheet(
            f"color: {self.style_manager.current_theme['foreground']};"
        )
        name_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 별표 버튼 추가
        star_button = QPushButton(
            "★" if self.event_handlers.is_favorited(symbol) else "☆"
        )
        star_button.setFixedSize(20, 20)
        star_button.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {'#ffd700' if self.event_handlers.is_favorited(symbol) else '#888'};
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: #ffd700;
            }}
        """
        )

        # 별표 클릭 이벤트
        star_button.clicked.connect(
            lambda: self.event_handlers.toggle_favorite(
                symbol, latex, name, star_button, menu
            )
        )
        star_button.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        layout.addWidget(symbol_label)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(star_button)

        container.setStyleSheet(
            f"""
            QWidget {{
                background-color: {self.style_manager.current_theme['dark_bg']};
                border-radius: 3px;
                border: 1px solid transparent;
            }}
            QWidget:hover {{
                background-color: {self.style_manager.current_theme['dark_bg']};
                border: 1px solid {self.style_manager.current_theme['accent2']};
            }}
        """
        )

        action.setDefaultWidget(container)
        menu.addAction(action)

        # 컨테이너 클릭 이벤트 (별표 클릭 제외)
        def container_click(event):
            star_rect = star_button.geometry()
            if not star_rect.contains(event.pos()):
                self.event_handlers.copy_symbol(symbol, latex, name)

        container.mousePressEvent = container_click
        return action

    # 이벤트 핸들러들을 위임
    def toggle_output_mode(self):
        self.event_handlers.toggle_output_mode()

    def show_settings_menu(self):
        self.event_handlers.show_settings_menu()

    def toggle_favorites_section(self):
        self.event_handlers.toggle_favorites_section()

    def add_to_favorites(self, symbol, latex, name):
        self.event_handlers.add_to_favorites(symbol, latex, name)

    def remove_from_favorites(self, symbol):
        self.event_handlers.remove_from_favorites(symbol)

    def reorder_favorites(self, symbol_data, drop_pos):
        self.event_handlers.reorder_favorites(symbol_data, drop_pos)

    def closeEvent(self, event):
        """앱 종료 시 설정 저장"""
        self.settings_manager.save_settings(self)
        event.accept()
