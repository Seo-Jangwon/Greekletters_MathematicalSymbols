import os
import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QSizePolicy,
    QScrollArea,
    QWidgetAction,
    QRadioButton,
    QButtonGroup,
    QFrame,
    QLayout,
    QToolTip,
)
from PyQt5.QtCore import QTimer, Qt, QPoint, QSize, pyqtSignal, QRect, QMimeData
from PyQt5.QtGui import (
    QFont,
    QClipboard,
    QResizeEvent,
    QPainter,
    QBrush,
    QPen,
    QColor,
    QDrag,
    QIcon,
)


def get_resource_path(relative_path):
    """리소스 경로를 가져오는 함수"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 상수 정의
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

WINDOW_SETTINGS = {
    "base_width": 450,
    "base_height": 600,
    "min_width": 350,
    "min_height": 500,
    "max_width": 500,
    "max_height": 800,
}

# 도쿄나잇 테마 색상
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

THEME = LIGHT_THEME


class QFlowLayout(QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(QFlowLayout, self).__init__(parent)
        self._hspacing = hspacing if hspacing >= 0 else 5
        self._vspacing = vspacing if vspacing >= 0 else 5
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        return self._hspacing

    def verticalSpacing(self):
        return self._vspacing

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(QFlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testOnly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineHeight = 0

        for item in self._items:
            widget = item.widget()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = widget.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal
                )
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceY = widget.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical
                )

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effective.right() and lineHeight > 0:
                x = effective.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom


class DraggableButton(QPushButton):
    def __init__(self, text, symbol_data, parent=None, is_favorite=False):
        super().__init__(text, parent)
        self.symbol_data = symbol_data  # (symbol, latex, name)
        self.drag_start_position = None
        self.is_favorite = is_favorite

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if not self.drag_start_position:
            return
        if (
            event.pos() - self.drag_start_position
        ).manhattanLength() < QApplication.startDragDistance():
            return

        # 드래그 시작
        drag = QDrag(self)
        mimeData = QMimeData()
        drag_data = {
            "symbol_data": self.symbol_data,
            "source": "favorites" if self.is_favorite else "recent",
        }
        mimeData.setText(json.dumps(drag_data))
        drag.setMimeData(mimeData)

        # 드래그 효과 설정
        if self.is_favorite:
            drag.exec_(Qt.MoveAction)  # 즐겨찾기 내부는 이동
        else:
            drag.exec_(Qt.CopyAction)  # 최근사용에서는 복사


class FavoritesDropZone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.parent_app = parent

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        try:
            drag_data = json.loads(event.mimeData().text())
            symbol_data = drag_data["symbol_data"]
            source = drag_data["source"]

            if source == "recent":
                # 최근 사용에서 드래그: 즐겨찾기에 추가
                self.parent_app.add_to_favorites(*symbol_data)
            elif source == "favorites":
                # 즐겨찾기 내부 드래그: 순서 변경
                drop_pos = event.pos()
                self.parent_app.reorder_favorites(symbol_data, drop_pos)

            event.accept()
        except Exception as e:
            print(f"Drop event error: {e}")
            event.ignore()


class ToggleSwitch(QPushButton):
    """커스텀 토글 스위치 버튼"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(50, 25)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 스위치 배경
        if self.isChecked():
            bg_color = QColor(THEME["accent2"])
        else:
            bg_color = QColor(THEME["button_border"])

        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(Qt.NoPen))

        # 배경 그리기 (고정된 크기)
        bg_rect_width = 46
        bg_rect_height = 21
        bg_x = (self.width() - bg_rect_width) // 2
        bg_y = (self.height() - bg_rect_height) // 2

        painter.drawRoundedRect(
            bg_x,
            bg_y,
            bg_rect_width,
            bg_rect_height,
            bg_rect_height // 2,
            bg_rect_height // 2,
        )

        # 스위치 핸들
        handle_color = QColor(THEME["background"])
        painter.setBrush(QBrush(handle_color))

        # 핸들 크기와 위치 (고정된 값)
        handle_size = 17
        handle_y = bg_y + (bg_rect_height - handle_size) // 2

        if self.isChecked():
            handle_x = bg_x + bg_rect_width - handle_size - 2
        else:
            handle_x = bg_x + 2

        painter.drawEllipse(handle_x, handle_y, handle_size, handle_size)


class SymbolApp(QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 최근 사용된 문자 배열 초기화
        self.recent_symbols = []
        # 즐겨찾기 배열 초기화
        self.favorites = []
        # 즐겨찾기 접기/펼치기 상태
        self.favorites_collapsed = True

        # LaTeX 모드 여부
        self.latex_mode = False

        # 다크 모드 여부 (기본값은 라이트 모드)
        self.is_dark_mode = False

        # 설정 파일 경로 초기화
        self.config_file = os.path.join(self.get_config_dir(), 'settings.json')
        
        # 설정 불러오기 (UI 생성 전에)
        self.load_settings()
        
        # 테마 전역 변수 설정 (UI 생성 전에)
        global THEME
        THEME = DARK_THEME if self.is_dark_mode else LIGHT_THEME

        # 폰트 설정
        self.default_font_family = self.get_available_font(
            ["JetBrains Mono", "Inter", "Consolas", "Courier New", "monospace"]
        )

        # 스케일 팩터 초기화
        self.scale_factor = 1.0

        # UI 컴포넌트 저장용
        self.category_buttons = []

        # UI 생성
        self.init_ui()

        # 테마 적용 (UI 생성 후)
        self.apply_theme()
        self.apply_theme_to_all_components()

        # 초기 리사이즈 이벤트 강제 발생
        self.calculate_scale_factor()
        self.on_resize()

        # 반응형 디자인을 위한 이벤트 연결
        self.resized.connect(self.on_resize)

        # 초기 상태 설정
        self.is_always_on_top = False

    def get_category_color(self, index):
        """카테고리 인덱스에 따른 강조색 반환"""
        colors = [
            THEME["accent2"],
            THEME["accent2"],
            THEME["accent2"],
            THEME["accent1"],
            THEME["accent1"],
            THEME["accent3"],
            THEME["accent3"],
            THEME["accent5"],
            THEME["accent4"],
            THEME["accent4"],
            THEME["accent1"],
            THEME["accent2"],
        ]
        return colors[index % len(colors)]

    def get_available_font(self, font_options):
        """사용 가능한 첫 번째 폰트 반환"""
        from PyQt5.QtGui import QFontDatabase

        font_db = QFontDatabase()
        available_fonts = font_db.families()

        for font in font_options:
            for available_font in available_fonts:
                if font.lower() == available_font.lower():
                    return available_font

        return font_options[-1]

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

    def create_button_style(self, padding_v, padding_h, margin=2, border_color=None):
        """버튼 스타일 생성 헬퍼 함수"""
        border = border_color or THEME["button_border"]
        return f"""
           QPushButton {{
               background-color: {THEME['button_bg']};
               color: {THEME['foreground']};
               border: 1px solid {border};
               border-radius: 4px;
               padding: {padding_v}px {padding_h}px;
               margin: {margin}px;
               text-align: left;
           }}
           QPushButton:hover {{
               background-color: {THEME['button_hover']};
           }}
           QPushButton:pressed {{
               background-color: {border};
               color: {THEME['dark_bg']};
           }}
       """

    def create_radio_button_style(self):
        """라디오 버튼 스타일 생성"""
        return f"""
           QRadioButton {{
               color: {THEME['foreground']};
               spacing: 5px;
           }}
           QRadioButton::indicator {{
               width: 13px;
               height: 13px;
               border-radius: 7px;
               border: 1px solid {THEME['accent2']};
           }}
           QRadioButton::indicator:checked {{
               background-color: {THEME['accent2']};
               border: 2px solid {THEME['dark_bg']};
           }}
       """

    def create_scroll_area_style(self):
        """스크롤 영역 스타일 생성"""
        return f"""
           QScrollArea {{
               border: 1px solid {THEME['button_border']};
               border-radius: 4px;
               background-color: {THEME['light_bg']};
           }}
           QScrollBar:vertical {{
               border: none;
               background: {THEME['dark_bg']};
               width: 8px;
               margin: 0px;
           }}
           QScrollBar::handle:vertical {{
               background: {THEME['button_border']};
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

    def init_ui(self):
        try:
            icon_path = get_resource_path("app_icon.ico")
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"아이콘 설정 오류: {e}")

        self.setWindowTitle("Greek letters & Mathematical Symbols")
        self.setGeometry(
            100, 100, WINDOW_SETTINGS["base_width"], WINDOW_SETTINGS["base_height"]
        )

        # 최대화 버튼 제거
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # 크기 제한 설정
        self.setMinimumSize(WINDOW_SETTINGS["min_width"], WINDOW_SETTINGS["min_height"])
        self.setMaximumSize(WINDOW_SETTINGS["max_width"], WINDOW_SETTINGS["max_height"])

        # 중앙 위젯과 레이아웃 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(10)

        # UI 섹션들 생성
        self.create_output_mode_section()
        self.create_recent_section()
        self.create_separator()
        self.create_favorites_section()
        self.create_separator()
        self.create_category_buttons()
        self.create_status_bar()

        # 메뉴 폰트 크기 초기화
        self.symbol_font_size = 16
        self.name_font_size = 10

        # 최근 사용 항목 업데이트
        self.update_recent_symbols()

        # 반응형 디자인을 위한 이벤트 연결
        self.resized.connect(self.on_resize)

        # 초기 상태 설정
        self.is_always_on_top = False
        
        if self.latex_mode:
            self.latex_mode_radio.setChecked(True)
        else:
            self.regular_mode_radio.setChecked(True)

    def get_config_dir(self):
        """설정 파일 디렉토리 경로 반환"""
        if os.name == "nt":
            config_dir = os.path.join(os.environ["APPDATA"], "GreekLetterFloat")
        else:
            config_dir = os.path.join(os.path.expanduser("~"), ".greekletterfloat")

        Path(config_dir).mkdir(exist_ok=True)
        return config_dir

    def save_settings(self):
        """설정을 JSON 파일로 저장"""
        settings = {
            "favorites": self.favorites,
            'favorites_collapsed': self.favorites_collapsed,
            "recent_symbols": self.recent_symbols,
            "is_dark_mode": self.is_dark_mode,
            "always_on_top": self.is_always_on_top,
            "latex_mode": self.latex_mode,
            "window_size": [self.width(), self.height()],
        }

        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"설정 저장 실패: {e}")

    def load_settings(self):
        """JSON 파일에서 설정 불러오기"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                self.favorites = settings.get('favorites', [])
                self.favorites_collapsed = settings.get('favorites_collapsed', True)
                self.recent_symbols = settings.get('recent_symbols', [])
                self.is_dark_mode = settings.get('is_dark_mode', False)
                self.is_always_on_top = settings.get('always_on_top', False)
                self.latex_mode = settings.get('latex_mode', False)
                
        except Exception as e:
            print(f"설정 불러오기 실패: {e}")

    def create_output_mode_section(self):
        """출력 모드 선택 영역 생성"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 5, 0, 5)

        # 출력 모드 라벨
        self.output_mode_label = QLabel("Output Mode:")
        self.output_mode_label.setFont(QFont(self.default_font_family, 10, QFont.Bold))
        self.output_mode_label.setStyleSheet(f"color: {THEME['foreground']};")
        layout.addWidget(self.output_mode_label)

        # 라디오 버튼 그룹
        self.mode_group = QButtonGroup(self)

        # 일반 모드 라디오 버튼
        self.regular_mode_radio = QRadioButton("Regular")
        self.regular_mode_radio.setChecked(True)
        self.regular_mode_radio.toggled.connect(self.toggle_output_mode)
        self.regular_mode_radio.setStyleSheet(self.create_radio_button_style())
        self.mode_group.addButton(self.regular_mode_radio)
        layout.addWidget(self.regular_mode_radio)

        # LaTeX 모드 라디오 버튼
        self.latex_mode_radio = QRadioButton("LaTeX")
        self.latex_mode_radio.toggled.connect(self.toggle_output_mode)
        self.latex_mode_radio.setStyleSheet(self.create_radio_button_style())
        self.mode_group.addButton(self.latex_mode_radio)
        layout.addWidget(self.latex_mode_radio)

        layout.addStretch()

        # 설정 버튼
        self.settings_button = QPushButton("⛯")
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setToolTip("Settings")
        self.settings_button.clicked.connect(self.show_settings_menu)
        self.settings_button.setStyleSheet(
            f"""
           QPushButton {{
               background-color: {THEME['button_bg']};
               color: {THEME['foreground']};
               border: 1px solid {THEME['button_border']};
               border-radius: 4px;
               padding: 2px;
               font-size: 16px;
           }}
           QPushButton:hover {{
               background-color: {THEME['button_hover']};
           }}
       """
        )
        layout.addWidget(self.settings_button)

        self.main_layout.addWidget(container)

    def show_settings_menu(self):
        """설정 메뉴 표시"""
        menu = QMenu(self)

        # 설정 메뉴 스타일
        menu.setStyleSheet(
            f"""
           QMenu {{
               background-color: {THEME['dark_bg']};
               color: {THEME['foreground']};
               border: 1px solid {THEME['accent2']};
               padding: 10px;
               min-width: 200px;
           }}
           QMenu::item {{
               padding: 0px;
               margin: 0px;
           }}
       """
        )

        self.create_settings_content(menu)

        # 설정 버튼 아래쪽에 메뉴 표시 (오른쪽 정렬)
        button_pos = self.settings_button.mapToGlobal(
            QPoint(0, self.settings_button.height())
        )
        menu_width = 200
        button_width = self.settings_button.width()
        adjusted_pos = QPoint(
            button_pos.x() - menu_width + button_width, button_pos.y()
        )
        menu.exec_(adjusted_pos)

    def create_settings_content(self, menu):
        """설정 메뉴 내용 생성"""
        # Always on top 설정
        always_on_top_action = QWidgetAction(menu)
        always_on_top_container = QWidget()
        always_on_top_container.setFixedHeight(35)  # 컨테이너 고정 높이
        always_on_top_layout = QHBoxLayout(always_on_top_container)
        always_on_top_layout.setContentsMargins(5, 5, 5, 5)
        always_on_top_layout.setSpacing(10)  # 고정 간격

        self.always_on_top_label = QLabel("Always on top:")
        self.always_on_top_label.setFont(QFont(self.default_font_family, 10))
        self.always_on_top_label.setFixedHeight(25)  # 고정 높이 설정
        self.always_on_top_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.always_on_top_label.setStyleSheet(
            f"""
            QLabel {{
                color: {THEME['foreground']};
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            """
        )
        # 라벨의 마우스 이벤트 비활성화
        self.always_on_top_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        always_on_top_layout.addWidget(self.always_on_top_label)

        # 스위치 앞에 적절한 간격 추가
        always_on_top_layout.addStretch()

        # 스위치를 오른쪽 여백과 함께 배치
        switch_container = QWidget()
        switch_layout = QHBoxLayout(switch_container)
        switch_layout.setContentsMargins(0, 0, 10, 0)  # 오른쪽 여백 10px
        switch_layout.setSpacing(0)

        self.always_on_top_switch = ToggleSwitch()
        self.always_on_top_switch.setChecked(self.is_always_on_top)
        self.always_on_top_switch.toggled.connect(self.toggle_always_on_top)
        # 스위치도 마우스 이벤트 비활성화 (컨테이너에서 처리)
        self.always_on_top_switch.setAttribute(Qt.WA_TransparentForMouseEvents)
        switch_layout.addWidget(self.always_on_top_switch)

        switch_container.setAttribute(Qt.WA_TransparentForMouseEvents)
        always_on_top_layout.addWidget(switch_container)

        # 컨테이너 클릭 이벤트 추가
        always_on_top_container.mousePressEvent = (
            lambda event: self.container_click_toggle_always_on_top(menu)
        )

        always_on_top_container.setStyleSheet(
            f"""
        QWidget {{
            background-color: {THEME['dark_bg']};
            border-radius: 3px;
            border: 1px solid transparent;
        }}
        QWidget:hover {{
            background-color: {THEME['dark_bg']};
            border: 1px solid {THEME['accent2']};
        }}
        QWidget:hover QLabel {{
            background-color: {THEME['dark_bg']};
        }}
    """
        )

        always_on_top_action.setDefaultWidget(always_on_top_container)
        menu.addAction(always_on_top_action)

        # Dark mode 설정
        dark_mode_action = QWidgetAction(menu)
        dark_mode_container = QWidget()
        dark_mode_container.setFixedHeight(35)  # 컨테이너 고정 높이
        dark_mode_layout = QHBoxLayout(dark_mode_container)
        dark_mode_layout.setContentsMargins(5, 5, 5, 5)
        dark_mode_layout.setSpacing(10)  # 고정 간격

        self.dark_mode_label = QLabel("Dark mode:")
        self.dark_mode_label.setFont(QFont(self.default_font_family, 10))
        self.dark_mode_label.setFixedHeight(25)  # 고정 높이 설정
        self.dark_mode_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.dark_mode_label.setStyleSheet(
            f"""
            QLabel {{
                color: {THEME['foreground']};
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            """
        )
        # 라벨의 마우스 이벤트 비활성화
        self.dark_mode_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        dark_mode_layout.addWidget(self.dark_mode_label)

        # 스위치 앞에 적절한 간격 추가
        dark_mode_layout.addStretch()

        # 스위치를 오른쪽 여백과 함께 배치
        switch_container2 = QWidget()
        switch_layout2 = QHBoxLayout(switch_container2)
        switch_layout2.setContentsMargins(0, 0, 10, 0)  # 오른쪽 여백 10px
        switch_layout2.setSpacing(0)

        self.theme_switch = ToggleSwitch()
        self.theme_switch.setChecked(self.is_dark_mode)
        self.theme_switch.toggled.connect(self.toggle_theme)
        # 스위치도 마우스 이벤트 비활성화 (컨테이너에서 처리)
        self.theme_switch.setAttribute(Qt.WA_TransparentForMouseEvents)
        switch_layout2.addWidget(self.theme_switch)

        switch_container2.setAttribute(Qt.WA_TransparentForMouseEvents)
        dark_mode_layout.addWidget(switch_container2)

        # 컨테이너 클릭 이벤트 추가
        dark_mode_container.mousePressEvent = (
            lambda event: self.container_click_toggle_theme(menu)
        )

        dark_mode_container.setStyleSheet(
            f"""
        QWidget {{
            background-color: {THEME['dark_bg']};
            border-radius: 3px;
            border: 1px solid transparent;
        }}
        QWidget:hover {{
            background-color: {THEME['dark_bg']};
            border: 1px solid {THEME['accent2']};
        }}
        QWidget:hover QLabel {{
            background-color: {THEME['dark_bg']};
        }}
    """
        )

        dark_mode_action.setDefaultWidget(dark_mode_container)
        menu.addAction(dark_mode_action)

    def create_recent_section(self):
        """최근 사용 항목 섹션 생성"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # 최근 사용 라벨
        self.recent_label = QLabel("Recently used:")
        self.recent_label.setFont(QFont(self.default_font_family, 10, QFont.Bold))
        self.recent_label.setStyleSheet(f"color: {THEME['foreground']};")
        layout.addWidget(self.recent_label)

        # 스크롤 영역 생성
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QFrame.StyledPanel)
        self.scroll_area.setStyleSheet(self.create_scroll_area_style())

        # 스크롤 영역 내부 위젯 생성
        self.recent_container_widget = QWidget()
        self.recent_container_widget.setStyleSheet(
            f"background-color: {THEME['light_bg']};"
        )
        self.recent_layout = QFlowLayout(self.recent_container_widget)
        self.recent_layout.setContentsMargins(3, 3, 3, 3)

        self.scroll_area.setWidget(self.recent_container_widget)
        self.update_recent_scroll_height()

        layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(container)

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

        # 즐겨찾기 라벨
        self.favorites_label = QLabel("Favorites:")
        self.favorites_label.setFont(QFont(self.default_font_family, 10, QFont.Bold))
        self.favorites_label.setStyleSheet(f"color: {THEME['foreground']};")
        header_layout.addWidget(self.favorites_label)

        # 접기/펼치기 버튼
        self.favorites_toggle_button = QPushButton(
            "▼" if not self.favorites_collapsed else "▶"
        )
        self.favorites_toggle_button.setFixedSize(20, 20)
        self.favorites_toggle_button.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {THEME['foreground']};
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {THEME['accent2']};
            }}
        """
        )
        self.favorites_toggle_button.clicked.connect(self.toggle_favorites_section)
        header_layout.addWidget(self.favorites_toggle_button)

        header_layout.addStretch()
        layout.addWidget(header_container)

        # 스크롤 영역 생성 (노란 배경, 스크롤 가능)
        self.favorites_scroll = QScrollArea()
        self.favorites_scroll.setWidgetResizable(True)
        self.favorites_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.favorites_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.favorites_scroll.setFrameShape(QFrame.StyledPanel)

        # 스크롤 영역 내부 위젯 생성 (드롭 존)
        self.favorites_container = FavoritesDropZone(self)
        self.favorites_layout = QFlowLayout(self.favorites_container)
        self.favorites_layout.setContentsMargins(3, 3, 3, 3)

        self.favorites_scroll.setWidget(self.favorites_container)

        # 초기 높이 설정
        self.update_favorites_scroll_height()

        # 초기 접기/펼치기 상태 적용
        self.favorites_scroll.setVisible(not self.favorites_collapsed)

        layout.addWidget(self.favorites_scroll)
        self.main_layout.addWidget(container)

        # 초기 즐겨찾기 표시
        self.update_favorites_display()

    def toggle_favorites_section(self):
        """즐겨찾기 섹션 접기/펼치기"""
        self.favorites_collapsed = not self.favorites_collapsed

        # 버튼 아이콘 변경
        self.favorites_toggle_button.setText("▶" if self.favorites_collapsed else "▼")

        # 스크롤 영역 보이기/숨기기
        self.favorites_scroll.setVisible(not self.favorites_collapsed)

        # 설정 저장
        self.save_settings()

        # 상태 메시지
        state = "collapsed" if self.favorites_collapsed else "expanded"
        self.statusBar().showMessage(f"Favorites section {state}", 1000)

    def update_favorites_scroll_height(self):
        """창 크기에 따라 즐겨찾기 스크롤 영역 높이 업데이트"""
        new_height = int(self.height() * SCALE_LIMITS["favorites_scroll_ratio"])
        new_height = max(100, min(200, new_height))
        self.favorites_scroll.setMaximumHeight(new_height)

    def update_favorites_scroll_style(self):
        """즐겨찾기 스크롤 영역 스타일 업데이트"""
        yellow_bg = "#fffacd" if not self.is_dark_mode else "#3a3a2a"
        yellow_border = "#daa520" if not self.is_dark_mode else "#8b7500"

        style = f"""
            QScrollArea {{
                border: 1px solid {yellow_border};
                border-radius: 4px;
                background-color: {yellow_bg};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {THEME['dark_bg']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {THEME['button_border']};
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

        self.favorites_scroll.setStyleSheet(style)
        self.favorites_container.setStyleSheet(f"background-color: {yellow_bg};")

    def is_favorited(self, symbol):
        """심볼이 즐겨찾기에 있는지 확인"""
        return any(fav[0] == symbol for fav in self.favorites)

    def add_to_favorites(self, symbol, latex, name):
        """즐겨찾기에 추가 (중복 방지, 최대 개수 제한)"""
        # 이미 존재하는지 확인
        if self.is_favorited(symbol):
            self.statusBar().showMessage(f"'{symbol}' is already in favorites", 2000)
            return

        # 최대 개수 확인
        if len(self.favorites) >= SCALE_LIMITS["max_favorites"]:
            self.statusBar().showMessage(
                f"Favorites limit reached ({SCALE_LIMITS['max_favorites']})", 3000
            )
            return

        self.favorites.append([symbol, latex, name])
        self.update_favorites_display()
        self.save_settings()
        self.statusBar().showMessage(
            f"Added '{symbol}' to favorites ({len(self.favorites)}/{SCALE_LIMITS['max_favorites']})",
            2000,
        )

    def remove_from_favorites(self, symbol):
        """즐겨찾기에서 제거"""
        self.favorites = [fav for fav in self.favorites if fav[0] != symbol]
        self.update_favorites_display()
        self.save_settings()
        self.statusBar().showMessage(f"Removed '{symbol}' from favorites", 2000)

    def reorder_favorites(self, symbol_data, drop_pos):
        """즐겨찾기 내부 순서 변경"""
        # 기존 위치에서 제거
        symbol = symbol_data[0]
        item_to_move = None
        for i, fav in enumerate(self.favorites):
            if fav[0] == symbol:
                item_to_move = self.favorites.pop(i)
                break

        if not item_to_move:
            return

        # 드롭 위치 계산
        drop_index = self.calculate_drop_index(drop_pos)

        # 새 위치에 삽입
        self.favorites.insert(drop_index, item_to_move)
        self.update_favorites_display()
        self.save_settings()

    def calculate_drop_index(self, drop_pos):
        """드롭 위치를 기반으로 삽입 인덱스 계산"""
        # 간단한 구현: 버튼들의 위치를 비교하여 적절한 인덱스 반환
        button_positions = []
        for i in range(self.favorites_layout.count()):
            item = self.favorites_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, DraggableButton):
                    pos = widget.pos()
                    button_positions.append(
                        (i, pos.x() + pos.y() * 1000)
                    )  # 간단한 위치 계산

        # 드롭 위치와 가장 가까운 버튼 찾기
        drop_score = drop_pos.x() + drop_pos.y() * 1000

        for i, (idx, pos) in enumerate(button_positions):
            if drop_score < pos:
                return i

        return len(self.favorites)

    def update_favorites_display(self):
        """즐겨찾기 표시 업데이트"""
        # 기존 버튼 제거
        for i in range(self.favorites_layout.count()):
            item = self.favorites_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                self.favorites_layout.removeItem(item)

        # 즐겨찾기가 없으면 빈 라벨 추가
        if not self.favorites:
            empty_label = QLabel("Drag symbols here or click ★ to add favorites")
            empty_label.setStyleSheet(f"color: {THEME['foreground']}; font-style: italic;")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setWordWrap(True)
            self.favorites_layout.addWidget(empty_label)
            return

        # 크기 계산
        favorites_size = self.calculate_scaled_size(9, "font")
        button_height = self.calculate_scaled_size(30, "height")
        padding_h = self.calculate_scaled_size(6, "padding")
        padding_v = self.calculate_scaled_size(4, "padding")

        # 노란색 테마 색상
        yellow_bg = "#fff8dc" if not self.is_dark_mode else "#3a3a1a"
        yellow_hover = "#ffebcd" if not self.is_dark_mode else "#4a4a2a"
        yellow_border = "#daa520" if not self.is_dark_mode else "#8b7500"

        # 즐겨찾기 버튼 생성
        for symbol, latex, name in self.favorites:
            # LaTeX 모드에 따라 표시 텍스트 결정
            if self.latex_mode:
                display_text = latex  # LaTeX 코드만 표시
                tooltip_text = f"Symbol: {symbol}\nLaTeX: {latex}\nName: {name}"
            else:
                display_text = symbol  # 심볼만 표시  
                tooltip_text = f"Symbol: {symbol}\nLaTeX: {latex}\nName: {name}"
            
            button = DraggableButton(
                display_text,  # 수정된 부분
                [symbol, latex, name],
                parent=self.favorites_container,
                is_favorite=True
            )
            
            button.setFont(QFont(self.default_font_family, favorites_size))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            button.setMinimumHeight(button_height)
            button.setToolTip(f"{tooltip_text}\nRight-click to remove\nDrag to reorder")

            # 스타일 설정 (노란 테마)
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {yellow_bg};
                    color: {THEME['foreground']};
                    padding: {padding_v}px {padding_h}px;
                    margin: 2px;
                    border: 1px solid {yellow_border};
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {yellow_hover};
                    border: 1px solid {yellow_border};
                }}
            """
            )

            # 우클릭 메뉴 설정
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(
                lambda pos, s=symbol, l=latex, n=name, btn=button: self.show_favorite_context_menu(
                    pos, s, l, n, btn
                )
            )

            # 클릭 이벤트
            button.clicked.connect(
                lambda checked, s=symbol, l=latex, n=name: self.copy_symbol(s, l, n)
            )

            self.favorites_layout.addWidget(button)

    def show_favorite_context_menu(self, pos, symbol, latex, name, button):
        """즐겨찾기 우클릭 메뉴"""
        menu = QMenu(self)
        menu.setStyleSheet(
            f"""
            QMenu {{
                background-color: {THEME['dark_bg']};
                color: {THEME['foreground']};
                border: 1px solid {THEME['accent2']};
            }}
            QMenu::item:selected {{
                background-color: {THEME['button_hover']};
            }}
        """
        )

        remove_action = menu.addAction("Remove from favorites")
        remove_action.triggered.connect(lambda: self.remove_from_favorites(symbol))

        menu.exec_(button.mapToGlobal(pos))

    def create_separator(self):
        """구분선 생성"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {THEME['button_border']};")
        self.main_layout.addWidget(line)

    def create_category_buttons(self):
        """카테고리 버튼 생성"""
        container = QWidget()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_layout = QVBoxLayout(container)
        self.button_layout.setSpacing(5)

        categories = [
            ("Lowercase greek letters", self.create_lowercase_greek),
            ("Capital greek letters", self.create_uppercase_greek),
            ("Roman Script Letters", self.create_script_letters),
            ("Math/Engineering Symbols", self.create_math_symbols),
            ("Vector/Matrix Operations", self.create_vector_symbols),
            ("Set theory", self.create_set_symbols),
            ("Logical operations", self.create_logic_symbols),
            ("Probability", self.create_stat_symbols),
            ("Physics", self.create_physics_symbols),
            ("Calculus", self.create_calculus_symbols),
            ("AI/ML", self.create_ai_symbols),
            ("Definition/Equation/Relationship", self.create_relation_symbols),
        ]

        for i, (category_name, create_func) in enumerate(categories):
            button = QPushButton(category_name)
            button.setFont(QFont(self.default_font_family, 9))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setMinimumHeight(30)
            button.clicked.connect(
                lambda checked, f=create_func, idx=i: self.show_symbols_menu(f, idx)
            )
            self.button_layout.addWidget(button)
            self.category_buttons.append(button)

        self.main_layout.addWidget(container)

    def create_status_bar(self):
        """상태바 생성"""
        self.statusBar().showMessage("Select a symbol to copy to clipboard")
        self.statusBar().setStyleSheet(
            f"""
           background-color: {THEME['light_bg']};
           color: {THEME['foreground']};
       """
        )

    def container_click_toggle_always_on_top(self, menu):
        """컨테이너 클릭으로 Always on top 토글"""
        self.always_on_top_switch.setChecked(not self.always_on_top_switch.isChecked())
        # 메뉴 닫기
        menu.close()
        # 짧은 딜레이 후 다시 열기
        QTimer.singleShot(100, self.show_settings_menu)

    def container_click_toggle_theme(self, menu):
        """컨테이너 클릭으로 테마 토글"""
        self.theme_switch.setChecked(not self.theme_switch.isChecked())
        # 메뉴 닫기
        menu.close()
        # 짧은 딜레이 후 다시 열기
        QTimer.singleShot(100, self.show_settings_menu)

    def toggle_always_on_top(self):
        """항상 위에 표시 기능 토글"""
        self.is_always_on_top = self.always_on_top_switch.isChecked()

        if self.is_always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

        self.show()

        message = (
            "Always on top: Enabled"
            if self.is_always_on_top
            else "Always on top: Disabled"
        )
        self.statusBar().showMessage(message, 2000)

    def toggle_theme(self):
        """다크 모드와 라이트 모드 전환"""
        self.is_dark_mode = self.theme_switch.isChecked()

        global THEME
        THEME = DARK_THEME if self.is_dark_mode else LIGHT_THEME

        self.apply_theme()  # 먼저 전체 테마 적용
        self.apply_theme_to_all_components()  # 개별 컴포넌트 적용
        self.update_recent_symbols()  # UI 업데이트
        self.update_favorites_display()  # 즐겨찾기 업데이트
        
        # 강제 리페인트
        self.repaint()

        theme_text = "Dark" if self.is_dark_mode else "Light"
        self.statusBar().showMessage(f"Switched to {theme_text} theme", 2000)

    def toggle_output_mode(self):
        """출력 모드 전환 처리"""
        self.latex_mode = self.latex_mode_radio.isChecked()
        self.update_recent_symbols()
        self.update_favorites_display()

        mode_text = "LaTeX" if self.latex_mode else "Regular"
        self.statusBar().showMessage(f"Switched to {mode_text} mode", 2000)

    def update_recent_scroll_height(self):
        """창 크기에 따라 최근 항목 스크롤 영역 높이 업데이트"""
        new_height = int(self.height() * SCALE_LIMITS["recent_scroll_ratio"])
        new_height = max(120, min(250, new_height))
        self.scroll_area.setMaximumHeight(new_height)

    def resizeEvent(self, event: QResizeEvent):
        """윈도우 크기 변경 이벤트 처리"""
        self.resized.emit()
        self.calculate_scale_factor()
        self.update_recent_scroll_height()
        self.update_favorites_scroll_height()
        return super().resizeEvent(event)

    def apply_theme(self):
        """현재 테마 적용"""
        app = QApplication.instance()
        app.setStyle("Fusion")

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {THEME['background']};
                color: {THEME['foreground']};
            }}
            QWidget {{
                background-color: {THEME['background']};
                color: {THEME['foreground']};
            }}
            QMenu {{
                background-color: {THEME['dark_bg']};
                color: {THEME['foreground']};
                border: 1px solid {THEME['button_border']};
            }}
            QMenu::item {{
                padding: 6px 25px 6px 25px;
            }}
            QMenu::item:selected {{
                background-color: {THEME['button_hover']};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {THEME['button_border']};
                margin: 5px 15px 5px 15px;
            }}
            QToolTip {{
                background-color: {THEME['dark_bg']};
                color: {THEME['foreground']};
                border: 1px solid {THEME['accent2']};
                padding: 3px;
                border-radius: 3px;
                opacity: 200;
            }}
            QFrame {{
                background-color: {THEME['background']};
                color: {THEME['foreground']};
            }}
        """)

    def apply_theme_to_all_components(self):
        """모든 UI 컴포넌트에 테마 적용"""
        
        # 중앙 위젯 배경색 명시적 설정
        central_widget = self.centralWidget()
        if central_widget:
            central_widget.setStyleSheet(f"background-color: {THEME['background']};")
        
        # 라벨 업데이트
        self.output_mode_label.setStyleSheet(f"color: {THEME['foreground']};")
        self.recent_label.setStyleSheet(f"color: {THEME['foreground']};")

        # 라디오 버튼 업데이트
        radio_style = self.create_radio_button_style()
        self.regular_mode_radio.setStyleSheet(radio_style)
        self.latex_mode_radio.setStyleSheet(radio_style)

        # 설정 버튼 업데이트
        self.settings_button.setStyleSheet(
            f"""
           QPushButton {{
               background-color: {THEME['button_bg']};
               color: {THEME['foreground']};
               border: 1px solid {THEME['button_border']};
               border-radius: 4px;
               padding: 2px;
               font-size: 16px;
           }}
           QPushButton:hover {{
               background-color: {THEME['button_hover']};
           }}
       """
        )

        # 스크롤 영역 업데이트
        self.scroll_area.setStyleSheet(self.create_scroll_area_style())
        self.recent_container_widget.setStyleSheet(
            f"background-color: {THEME['light_bg']};"
        )

        # 카테고리 버튼 스타일 업데이트
        self.update_category_button_styles()

        # 상태바 업데이트
        self.statusBar().setStyleSheet(
            f"""
           background-color: {THEME['light_bg']};
           color: {THEME['foreground']};
       """
        )
        
        self.favorites_label.setStyleSheet(f"color: {THEME['foreground']};")
        self.favorites_toggle_button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {THEME['foreground']};
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                color: {THEME['accent2']};
            }}
        """)

        self.update_favorites_scroll_style()
        self.favorites_label.setStyleSheet(f"color: {THEME['foreground']};")
        self.update_favorites_display()

    def update_category_button_styles(self):
        """카테고리 버튼 스타일 업데이트"""
        for i, button in enumerate(self.category_buttons):
            border_color = self.get_category_color(i)
            padding_v = self.calculate_scaled_size(5, "padding")
            padding_h = self.calculate_scaled_size(10, "padding")
            margin = self.calculate_scaled_size(3, "padding")

            button.setStyleSheet(
                self.create_button_style(padding_v, padding_h, margin, border_color)
            )

    def on_resize(self):
        """윈도우 크기에 따라 폰트 및 버튼 크기 조정"""
        # 폰트 크기 계산
        base_font_size = self.calculate_scaled_size(
            SCALE_LIMITS["base_font_size"], "font"
        )
        button_font_size = self.calculate_scaled_size(9, "font")

        # 메뉴 폰트 크기 계산
        self.symbol_font_size = self.calculate_scaled_size(16, "font")
        self.name_font_size = self.calculate_scaled_size(10, "font")

        # 버튼 높이 계산
        button_height = self.calculate_scaled_size(30, "height")

        # 카테고리 버튼 업데이트
        for i, button in enumerate(self.category_buttons):
            button.setFont(QFont(self.default_font_family, button_font_size))
            button.setMinimumHeight(button_height)

        # 최근 사용 버튼 업데이트
        self.update_recent_buttons_style()

        # 카테고리 버튼 스타일 업데이트
        self.update_category_button_styles()

    def update_recent_buttons_style(self):
        """최근 사용 버튼 스타일 업데이트"""
        recent_size = self.calculate_scaled_size(9, "font")
        button_height = self.calculate_scaled_size(30, "height")
        padding_h = self.calculate_scaled_size(6, "padding")
        padding_v = self.calculate_scaled_size(4, "padding")

        for i in range(self.recent_layout.count()):
            item = self.recent_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QPushButton):
                    widget.setFont(QFont(self.default_font_family, recent_size))
                    widget.setMinimumHeight(button_height)
                    widget.setStyleSheet(
                        f"""
                       QPushButton {{
                           background-color: {THEME['button_bg']};
                           color: {THEME['foreground']};
                           padding: {padding_v}px {padding_h}px;
                           margin: 2px;
                           border: 1px solid {THEME['button_border']};
                           border-radius: 4px;
                       }}
                       QPushButton:hover {{
                           background-color: {THEME['button_hover']};
                           border: 1px solid {THEME['accent2']};
                       }}
                   """
                    )

    def show_symbols_menu(self, create_func, category_index=0):
        """심볼 메뉴 표시"""
        menu = QMenu(self)
        accent_color = self.get_category_color(category_index)

        menu.setStyleSheet(
            f"""
           QMenu {{
               background-color: {THEME['dark_bg']};
               color: {THEME['foreground']};
               border: 1px solid {accent_color};
               padding: 5px;
           }}
           QMenu::item {{
               padding: 8px 25px 8px 25px;
           }}
           QMenu::item:selected {{
               background-color: {THEME['button_hover']};
           }}
       """
        )

        create_func(menu)

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
        symbol_label.setStyleSheet(f"color: {THEME['foreground']};")
        symbol_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 이름 라벨
        name_label = QLabel(f"({name})")
        name_font = QFont(self.default_font_family, self.name_font_size)
        name_label.setFont(name_font)
        name_label.setStyleSheet(f"color: {THEME['foreground']};")
        name_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 별표 버튼 추가
        star_button = QPushButton("★" if self.is_favorited(symbol) else "☆")
        star_button.setFixedSize(20, 20)
        star_button.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {'#ffd700' if self.is_favorited(symbol) else '#888'};
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: #ffd700;
            }}
        """
        )

        # 별표 클릭 이벤트
        star_button.clicked.connect(
            lambda: self.toggle_favorite(symbol, latex, name, star_button, menu)
        )
        star_button.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        layout.addWidget(symbol_label)
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(star_button)

        container.setStyleSheet(
            f"""
            QWidget {{
                background-color: {THEME['dark_bg']};
                border-radius: 3px;
                border: 1px solid transparent;
            }}
            QWidget:hover {{
                background-color: {THEME['dark_bg']};
                border: 1px solid {THEME['accent2']};
            }}
        """
        )

        action.setDefaultWidget(container)
        menu.addAction(action)

        # 컨테이너 클릭 이벤트 (별표 클릭 제외)
        def container_click(event):
            # 별표 버튼 영역이 아닌 경우에만 복사
            star_rect = star_button.geometry()
            if not star_rect.contains(event.pos()):
                self.copy_symbol(symbol, latex, name)

        container.mousePressEvent = container_click
        return action

    def toggle_favorite(self, symbol, latex, name, star_button, menu):
        """즐겨찾기 토글"""
        if self.is_favorited(symbol):
            self.remove_from_favorites(symbol)
            star_button.setText("☆")
            star_button.setStyleSheet(
                star_button.styleSheet().replace("#ffd700", "#888")
            )
        else:
            self.add_to_favorites(symbol, latex, name)
            star_button.setText("★")
            star_button.setStyleSheet(
                star_button.styleSheet().replace("#888", "#ffd700")
            )

    def copy_symbol(self, symbol, latex, name):
        """심볼 복사 및 최근 사용 목록 업데이트"""
        clipboard = QApplication.clipboard()
        if self.latex_mode:
            clipboard.setText(latex, QClipboard.Clipboard)
            copied_text = latex
        else:
            clipboard.setText(symbol, QClipboard.Clipboard)
            copied_text = symbol

        self.add_to_recent_symbols(symbol, latex, name)

        mode_text = "LaTeX" if self.latex_mode else "symbol"
        self.statusBar().showMessage(
            f"Copied {mode_text}: {copied_text} ({name})", 2000
        )

    def add_to_recent_symbols(self, symbol, latex, name):
        """최근 사용 목록에 심볼 추가"""
        # 이미 목록에 있는지 확인
        for i, (s, l, n) in enumerate(self.recent_symbols):
            if s == symbol:
                self.recent_symbols.pop(i)
                break

        # 맨 앞에 추가
        self.recent_symbols.insert(0, (symbol, latex, name))

        # 최대 개수 제한
        if len(self.recent_symbols) > SCALE_LIMITS["max_recent_items"]:
            self.recent_symbols.pop()

        self.update_recent_symbols()

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
            empty_label.setStyleSheet(f"color: {THEME['foreground']};")
            self.recent_layout.addWidget(empty_label)
            return

        # 크기 계산
        recent_size = self.calculate_scaled_size(9, "font")
        button_height = self.calculate_scaled_size(30, "height")
        padding_h = self.calculate_scaled_size(6, "padding")
        padding_v = self.calculate_scaled_size(4, "padding")

        # 최근 사용 항목 버튼 생성 (드래그 가능)
        for symbol, latex, name in self.recent_symbols:
            # LaTeX 모드에 따라 표시 텍스트 결정 (수정된 부분)
            if self.latex_mode:
                display_text = latex  # LaTeX 코드만 표시
                tooltip_text = f"Symbol: {symbol}\nLaTeX: {latex}\nName: {name}"
            else:
                display_text = symbol  # 심볼만 표시
                tooltip_text = f"Symbol: {symbol}\nLaTeX: {latex}\nName: {name}"
            
            button = DraggableButton(
                display_text,  # 수정된 부분
                [symbol, latex, name],
                parent=self.recent_container_widget,
                is_favorite=False
            )

            button.setFont(QFont(self.default_font_family, recent_size))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            button.setMinimumHeight(button_height)
            
            # 툴팁에 드래그 힌트 추가
            tooltip_text += "\nDrag to favorites to save"
            button.setToolTip(tooltip_text)

            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {THEME['button_bg']};
                    color: {THEME['foreground']};
                    padding: {padding_v}px {padding_h}px;
                    margin: 2px;
                    border: 1px solid {THEME['button_border']};
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                    border: 1px solid {THEME['accent2']};
                }}
            """)

            button.clicked.connect(
                lambda checked, s=symbol, l=latex, n=name: self.copy_symbol(s, l, n)
            )

            self.recent_layout.addWidget(button)

    def create_lowercase_greek(self, menu):
        symbols = [
            ("α", r"\alpha", "alpha"),
            ("β", r"\beta", "beta"),
            ("γ", r"\gamma", "gamma"),
            ("δ", r"\delta", "delta"),
            ("ε", r"\epsilon", "epsilon"),
            ("ϵ", r"\varepsilon", "varepsilon"),
            ("ζ", r"\zeta", "zeta"),
            ("η", r"\eta", "eta"),
            ("θ", r"\theta", "theta"),
            ("ϑ", r"\vartheta", "vartheta"),
            ("ι", r"\iota", "iota"),
            ("κ", r"\kappa", "kappa"),
            ("ϰ", r"\varkappa", "varkappa"),
            ("λ", r"\lambda", "lambda"),
            ("μ", r"\mu", "mu"),
            ("ν", r"\nu", "nu"),
            ("ξ", r"\xi", "xi"),
            ("ο", "o", "omicron"),
            ("π", r"\pi", "pi"),
            ("ϖ", r"\varpi", "varpi"),
            ("ρ", r"\rho", "rho"),
            ("ϱ", r"\varrho", "varrho"),
            ("σ", r"\sigma", "sigma"),
            ("ς", r"\varsigma", "varsigma"),
            ("τ", r"\tau", "tau"),
            ("υ", r"\upsilon", "upsilon"),
            ("φ", r"\phi", "phi"),
            ("ϕ", r"\varphi", "varphi"),
            ("χ", r"\chi", "chi"),
            ("ψ", r"\psi", "psi"),
            ("ω", r"\omega", "omega"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_uppercase_greek(self, menu):
        symbols = [
            ("Α", "A", "Alpha"),
            ("Β", "B", "Beta"),
            ("Γ", r"\Gamma", "Gamma"),
            ("Δ", r"\Delta", "Delta"),
            ("Ε", "E", "Epsilon"),
            ("Ζ", "Z", "Zeta"),
            ("Η", "H", "Eta"),
            ("Θ", r"\Theta", "Theta"),
            ("Ι", "I", "Iota"),
            ("Κ", "K", "Kappa"),
            ("Λ", r"\Lambda", "Lambda"),
            ("Μ", "M", "Mu"),
            ("Ν", "N", "Nu"),
            ("Ξ", r"\Xi", "Xi"),
            ("Ο", "O", "Omicron"),
            ("Π", r"\Pi", "Pi"),
            ("Ρ", "P", "Rho"),
            ("Σ", r"\Sigma", "Sigma"),
            ("Τ", "T", "Tau"),
            ("Υ", r"\Upsilon", "Upsilon"),
            ("Φ", r"\Phi", "Phi"),
            ("Χ", "X", "Chi"),
            ("Ψ", r"\Psi", "Psi"),
            ("Ω", r"\Omega", "Omega"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_script_letters(self, menu):
        symbols = [
            ("𝒜", r"\mathcal{A}", "Script A"),
            ("ℬ", r"\mathcal{B}", "Script B"),
            ("𝒞", r"\mathcal{C}", "Script C"),
            ("𝒟", r"\mathcal{D}", "Script D"),
            ("ℰ", r"\mathcal{E}", "Script E"),
            ("ℱ", r"\mathcal{F}", "Script F"),
            ("𝒢", r"\mathcal{G}", "Script G"),
            ("ℋ", r"\mathcal{H}", "Script H"),
            ("ℐ", r"\mathcal{I}", "Script I"),
            ("𝒥", r"\mathcal{J}", "Script J"),
            ("𝒦", r"\mathcal{K}", "Script K"),
            ("ℒ", r"\mathcal{L}", "Script L"),
            ("ℳ", r"\mathcal{M}", "Script M"),
            ("𝒩", r"\mathcal{N}", "Script N"),
            ("𝒪", r"\mathcal{O}", "Script O"),
            ("𝒫", r"\mathcal{P}", "Script P"),
            ("𝒬", r"\mathcal{Q}", "Script Q"),
            ("ℛ", r"\mathcal{R}", "Script R"),
            ("𝒮", r"\mathcal{S}", "Script S"),
            ("𝒯", r"\mathcal{T}", "Script T"),
            ("𝒰", r"\mathcal{U}", "Script U"),
            ("𝒱", r"\mathcal{V}", "Script V"),
            ("𝒲", r"\mathcal{W}", "Script W"),
            ("𝒳", r"\mathcal{X}", "Script X"),
            ("𝒴", r"\mathcal{Y}", "Script Y"),
            ("𝒵", r"\mathcal{Z}", "Script Z"),
            ("𝒻", r"\mathcal{f}", "Script f"),
            ("𝒽", r"\mathcal{h}", "Script h"),
            ("𝒾", r"\mathcal{i}", "Script i"),
            ("𝓁", r"\mathcal{l}", "Script l"),
            ("𝓂", r"\mathcal{m}", "Script m"),
            ("𝓃", r"\mathcal{n}", "Script n"),
            ("𝓅", r"\mathcal{p}", "Script p"),
            ("𝓇", r"\mathcal{r}", "Script r"),
            ("𝓉", r"\mathcal{t}", "Script t"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_math_symbols(self, menu):
        symbols = [
            ("∑", r"\sum_{i=1}^{n}", "Sum"),
            ("∏", r"\prod_{i=1}^{n}", "Product"),
            ("∂", r"\partial", "Partial"),
            ("∇", r"\nabla", "Nabla"),
            ("∞", r"\infty", "Infinity"),
            ("∫", r"\int_{a}^{b}", "Integral"),
            ("≈", r"\approx", "Approximately"),
            ("≠", r"\neq", "Not Equal"),
            ("≤", r"\leq", "Less Than or Equal"),
            ("≥", r"\geq", "Greater Than or Equal"),
            ("∈", r"\in", "Element Of"),
            ("⊂", r"\subset", "Subset"),
            ("∩", r"\cap", "Intersection"),
            ("∪", r"\cup", "Union"),
            ("→", r"\rightarrow", "Right Arrow"),
            ("←", r"\leftarrow", "Left Arrow"),
            ("↔", r"\leftrightarrow", "Double Arrow"),
            ("≡", r"\equiv", "Identical To"),
            ("≅", r"\cong", "Congruent To"),
            ("≜", r"\triangleq", "Defined As"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_vector_symbols(self, menu):
        symbols = [
            ("·", r"\cdot", "Dot Product"),
            ("×", r"\times", "Cross Product"),
            ("⊗", r"\otimes", "Tensor Product"),
            ("⊕", r"\oplus", "Direct Sum"),
            ("⟨", r"\langle", "Left Angle Bracket"),
            ("⟩", r"\rangle", "Right Angle Bracket"),
            ("‖", r"\|", "Norm"),
            ("⊥", r"\perp", "Perpendicular"),
            ("∥", r"\parallel", "Parallel"),
            ("†", r"^\dagger", "Conjugate Transpose"),
            ("⊙", r"\odot", "Hadamard Product"),
            ("⨂", r"\bigotimes", "Kronecker Product"),
            ("⨁", r"\bigoplus", "Direct Sum Operator"),
            ("⟦", r"\llbracket", "Left Double Bracket"),
            ("⟧", r"\rrbracket", "Right Double Bracket"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_set_symbols(self, menu):
        symbols = [
            ("∅", r"\emptyset", "Empty Set"),
            ("∀", r"\forall", "For All"),
            ("∃", r"\exists", "There Exists"),
            ("∄", r"\nexists", "Does Not Exist"),
            ("∉", r"\notin", "Not Element Of"),
            ("⊄", r"\not\subset", "Not Subset"),
            ("⊆", r"\subseteq", "Subset or Equal"),
            ("⊇", r"\supseteq", "Superset or Equal"),
            ("⊊", r"\subsetneq", "Proper Subset"),
            ("⊋", r"\supsetneq", "Proper Superset"),
            ("ℕ", r"\mathbb{N}", "Natural Numbers"),
            ("ℤ", r"\mathbb{Z}", "Integers"),
            ("ℚ", r"\mathbb{Q}", "Rational Numbers"),
            ("ℝ", r"\mathbb{R}", "Real Numbers"),
            ("ℂ", r"\mathbb{C}", "Complex Numbers"),
            ("ℙ", r"\mathbb{P}", "Prime Numbers"),
            ("△", r"\triangle", "Symmetric Difference"),
            ("×", r"\times", "Cartesian Product"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_logic_symbols(self, menu):
        symbols = [
            ("¬", r"\neg", "Negation/Not"),
            ("∧", r"\wedge", "Logical And"),
            ("∨", r"\vee", "Logical Or"),
            ("⊻", r"\veebar", "Exclusive Or"),
            ("⇒", r"\Rightarrow", "Implies"),
            ("⇔", r"\Leftrightarrow", "If and Only If"),
            ("⊨", r"\models", "Models/Entails"),
            ("⊢", r"\vdash", "Proves"),
            ("□", r"\Box", "Necessary"),
            ("◊", r"\Diamond", "Possible"),
            ("⊤", r"\top", "Top/True"),
            ("⊥", r"\bot", "Bottom/False"),
            ("≡", r"\equiv", "Logical Equivalence"),
            ("⊦", r"\vdash", "Assertion"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_stat_symbols(self, menu):
        symbols = [
            ("𝔼", r"\mathbb{E}", "Expected Value"),
            ("ℙ", r"\mathbb{P}", "Probability"),
            ("𝕍", r"\mathbb{V}", "Variance"),
            ("√", r"\sqrt{x}", "Square Root"),
            ("∝", r"\propto", "Proportional To"),
            ("±", r"\pm", "Plus-Minus"),
            ("∼", r"\sim", "Distributed As"),
            ("≫", r"\gg", "Much Greater Than"),
            ("≪", r"\ll", "Much Less Than"),
            ("μ̂", r"\hat{\mu}", "mu hat - estimator"),
            ("σ̂", r"\hat{\sigma}", "sigma hat - estimator"),
            ("ρ", r"\rho", "rho - correlation"),
            ("χ²", r"\chi^2", "Chi-Squared"),
            ("σ²", r"\sigma^2", "Variance"),
            ("⟂", r"\perp", "Independent"),
            ("∩", r"\cap", "Intersection/And"),
            ("∪", r"\cup", "Union/Or"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_physics_symbols(self, menu):
        symbols = [
            ("ℏ", r"\hbar", "h-bar"),
            ("ψ", r"\psi", "wavefunction"),
            ("Ψ", r"\Psi", "Wavefunction"),
            ("⟨ϕ|ψ⟩", r"\langle \phi | \psi \rangle", "Bracket Notation"),
            ("⊗", r"\otimes", "Tensor Product"),
            ("†", r"^\dagger", "Hermitian Conjugate"),
            ("°", r"^\circ", "Degree"),
            ("∮", r"\oint", "Contour Integral"),
            ("∯", r"\oiint", "Surface Integral"),
            ("∰", r"\oiiint", "Volume Integral"),
            ("∇²", r"\nabla^2", "Laplacian"),
            ("×", r"\times", "Curl Operator"),
            ("γ", r"\gamma", "Lorentz Factor"),
            ("Λ", r"\Lambda", "Lambda/Cosmological Constant"),
            ("⟨Â⟩", r"\langle \hat{A} \rangle", "Expectation Value"),
            ("⨂", r"\bigotimes", "Tensor Product Operator"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_calculus_symbols(self, menu):
        symbols = [
            ("∫", r"\int_{a}^{b}", "Definite Integral"),
            ("∫", r"\int", "Indefinite Integral"),
            ("∬", r"\iint_{D}", "Double Integral"),
            ("∭", r"\iiint_{V}", "Triple Integral"),
            ("∮", r"\oint_{C}", "Contour Integral"),
            ("∯", r"\oiint_{S}", "Surface Integral"),
            ("∰", r"\oiiint_{V}", "Volume Integral"),
            ("∂x", r"\frac{\partial}{\partial x}", "Partial wrt x"),
            ("∂y", r"\frac{\partial}{\partial y}", "Partial wrt y"),
            ("∂z", r"\frac{\partial}{\partial z}", "Partial wrt z"),
            ("∂t", r"\frac{\partial}{\partial t}", "Partial wrt t"),
            ("′", r"^\prime", "Prime/Derivative"),
            ("″", r"^{\prime\prime}", "Double Prime"),
            ("dx", "dx", "Differential x"),
            ("∇f", r"\nabla f", "Gradient"),
            ("lim", r"\lim_{x \to a}", "Limit"),
            ("δ", r"\delta", "Variation/Functional Derivative"),
            ("ε", r"\epsilon", "Epsilon/Small Quantity"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_ai_symbols(self, menu):
        symbols = [
            ("∇θ", r"\nabla_\theta", "Gradient wrt Parameters"),
            ("∑", r"\sum_{i=1}^{n}", "Summation"),
            ("∏", r"\prod_{i=1}^{n}", "Product"),
            ("𝔼", r"\mathbb{E}", "Expected Value"),
            ("ℙ", r"\mathbb{P}", "Probability"),
            ("𝕍", r"\mathbb{V}", "Variance"),
            ("⊗", r"\otimes", "Tensor Product"),
            ("⊕", r"\oplus", "Direct Sum"),
            ("⊙", r"\odot", "Hadamard Product"),
            ("∥W∥", r"\|W\|", "Norm of Weights"),
            ("θ̂", r"\hat{\theta}", "Parameter Estimate"),
            ("ŷ", r"\hat{y}", "Prediction"),
            ("𝓛", r"\mathcal{L}", "Loss Function"),
            (
                "∂𝓛/∂θ",
                r"\frac{\partial\mathcal{L}}{\partial\theta}",
                "Gradient of Loss",
            ),
            ("≈", r"\approx", "Approximately Equal"),
            ("σ", r"\sigma", "Activation Function/Sigmoid"),
            ("ϕ", r"\phi", "Feature Map"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)

    def create_relation_symbols(self, menu):
        symbols = [
            ("≡", r"\equiv", "Identical To"),
            ("≡", r"\equiv \pmod{n}", "Congruent Modulo n"),
            ("≃", r"\simeq", "Asymptotically Equal"),
            ("≍", r"\asymp", "Equivalent To"),
            ("≕", r"\coloneq", "Equal By Definition"),
            ("≔", r"\coloneqq", "Equal By Definition (variant)"),
            ("≅", r"\cong", "Congruent To"),
            ("≈", r"\approx", "Approximately Equal"),
            ("≠", r"\neq", "Not Equal"),
            ("≻", r"\succ", "Succeeds"),
            ("≺", r"\prec", "Precedes"),
            ("≼", r"\preceq", "Precedes or Equal"),
            ("≽", r"\succeq", "Succeeds or Equal"),
            ("≤", r"\leq", "Less Than or Equal"),
            ("≥", r"\geq", "Greater Than or Equal"),
            ("≪", r"\ll", "Much Less Than"),
            ("≫", r"\gg", "Much Greater Than"),
            ("∝", r"\propto", "Proportional To"),
            ("≜", r"\triangleq", "Defined As"),
            ("≝", r"\triangleq", "Equal By Definition"),
            ("≐", r"\doteq", "Approaches Limit"),
            ("≙", r"\eqcirc", "Estimates"),
            ("≟", r"\stackrel{?}{=}", "Questioned Equal To"),
            ("≑", r"\doteqdot", "Geometrically Equal"),
            ("≒", r"\fallingdotseq", "Approximately Equal/Congruent"),
        ]
        for symbol, latex, name in symbols:
            self.create_symbol_menu_item(menu, symbol, latex, name)


def main():
    app = QApplication(sys.argv)

    # 고해상도 디스플레이 지원
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app.setStyle("Fusion")

    window = SymbolApp()

    app.aboutToQuit.connect(window.save_settings)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
