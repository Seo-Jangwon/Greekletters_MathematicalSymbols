import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QAction,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QListWidget,
    QSizePolicy,
    QScrollArea,
    QWidgetAction,
    QRadioButton,
    QButtonGroup,
    QFrame,
    QLayout,
    QToolTip,
    QGridLayout,
)
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal, QRect, QSettings
from PyQt5.QtGui import QFont, QClipboard, QResizeEvent, QColor, QPalette
from PyQt5.QtGui import QIcon


def get_resource_path(relative_path):
    """리소스 경로를 가져오는 함수"""
    try:
        # PyInstaller가 생성한 임시 폴더 확인
        base_path = sys._MEIPASS
    except Exception:
        # 일반 파이썬 스크립트 실행 시 현재 경로 사용
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 도쿄나잇 테마 색상
DARK_THEME = {
    "background": "#1a1b26",
    "foreground": "#a9b1d6",
    "accent1": "#bb9af7",  # 보라색
    "accent2": "#7aa2f7",  # 파란색
    "accent3": "#9ece6a",  # 초록색
    "accent4": "#f7768e",  # 빨간색
    "accent5": "#7dcfff",  # 시안색
    "dark_bg": "#16161e",  # 더 어두운 배경
    "light_bg": "#24283b",  # 약간 밝은 배경
    "button_bg": "#24283b",  # 버튼 배경
    "button_hover": "#414868",  # 버튼 호버
    "button_border": "#414868",  # 버튼 테두리
}

LIGHT_THEME = {
    "background": "#f0f1f5",  # 밝은 배경
    "foreground": "#343b58",  # 어두운 텍스트
    "accent1": "#9d7cd8",  # 보라색 (어두운 버전)
    "accent2": "#5a80db",  # 파란색 (어두운 버전)
    "accent3": "#79a15e",  # 초록색 (어두운 버전)
    "accent4": "#d35b78",  # 빨간색 (어두운 버전)
    "accent5": "#5aacd3",  # 시안색 (어두운 버전)
    "dark_bg": "#d8dae5",  # 약간 어두운 배경
    "light_bg": "#e0e2ed",  # 약간 밝은 배경
    "button_bg": "#e0e2ed",  # 버튼 배경
    "button_hover": "#c6c9d8",  # 버튼 호버
    "button_border": "#bbbfd1",  # 버튼 테두리
}

THEME = LIGHT_THEME


# 사용자 정의 QFlowLayout 클래스 구현
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


# LaTeX 코드 버튼 클래스
class LatexButton(QPushButton):
    def __init__(
        self, symbol, latex, name, is_latex_mode=False, parent=None, scale_factor=1.0
    ):
        super().__init__(parent)
        self.symbol = symbol
        self.latex = latex
        self.name = name
        self.scale_factor = scale_factor

        # 모드에 따라 버튼 표시 텍스트 설정
        if is_latex_mode:
            self.setText(latex)  # LaTeX 모드일 때는 LaTeX 코드 표시
            self.setToolTip(f"{latex} ({name})")
        else:
            self.setText(symbol)  # 일반 모드일 때는 심볼 표시
            self.setToolTip(f"{symbol} ({name})")

        # 도쿄나잇 테마 스타일 적용
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {THEME["button_bg"]};
                color: {THEME["foreground"]};
                border: 1px solid {THEME["button_border"]};
                border-radius: 4px;
                padding: {4 * scale_factor}px {8 * scale_factor}px;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {THEME["button_hover"]};
                border: 1px solid {THEME["accent2"]};
            }}
        """
        )

    def enterEvent(self, event):
        """마우스가 버튼 위로 올라갔을 때 정보 표시"""
        if self.latex == self.text():  # LaTeX 모드
            QToolTip.showText(
                self.mapToGlobal(QPoint(0, -30)), f"{self.symbol} | {self.name}"
            )
        else:  # 일반 모드
            QToolTip.showText(
                self.mapToGlobal(QPoint(0, -30)), f"{self.latex} | {self.name}"
            )
        super().enterEvent(event)


class SymbolLabel(QLabel):
    """심볼을 표시하기 위한 라벨"""

    clicked = pyqtSignal(str, str, str)  # 일반 심볼, LaTeX 코드, 이름

    def __init__(self, symbol, latex, name, parent=None):
        super().__init__(parent)
        self.symbol = symbol
        self.latex = latex
        self.name = name

        # 텍스트 설정 (심볼은 더 크게)
        self.symbol_font = QFont("Inter", 16)
        self.name_font = QFont("Inter", 10)
        self.update_text()

        # 마우스 이벤트 추적
        self.setMouseTracking(True)

        # 도쿄나잇 테마 스타일 적용
        self.setStyleSheet(
            f"""
            color: {THEME["foreground"]};
            padding: 4px;
        """
        )

    def update_text(self):
        """심볼과 이름을 표시"""
        self.setText(f"{self.symbol}  ({self.name})")

    def set_font_sizes(self, symbol_size, name_size):
        """폰트 크기 설정"""
        self.symbol_font.setPointSize(symbol_size)
        self.name_font.setPointSize(name_size)
        self.update_text()

    def mousePressEvent(self, event):
        """마우스 클릭 이벤트 처리"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.symbol, self.latex, self.name)
        super().mousePressEvent(event)


class SymbolApp(QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 최근 사용된 문자 배열 초기화 (최대 15개 저장)
        self.recent_symbols = []

        # LaTeX 모드 여부
        self.latex_mode = False

        # 다크 모드 여부 (기본값은 라이트 모드)
        self.is_dark_mode = False
        global THEME
        THEME = LIGHT_THEME

        # 폰트 설정 - 폰트 우선순위 목록
        font_options = [
            "JetBrains Mono",
            "Inter",
            "Consolas",
            "Courier New",
            "monospace",
        ]
        self.default_font_family = self.get_available_font(font_options)

        # 기본 크기 설정
        self.base_width = 450
        self.base_height = 600

        # 스케일 팩터 초기화
        self.scale_factor = 1.0

        self.init_ui()

        # 초기 리사이즈 이벤트 강제 발생
        self.calculate_scale_factor()
        self.on_resize()

    def get_category_color(self, index):
        """카테고리 인덱스에 따른 강조색 반환"""
        colors = [
            THEME["accent2"],  # 파란색
            THEME["accent2"],  # 파란색
            THEME["accent2"],  # 파란색색
            THEME["accent1"],  # 보라색
            THEME["accent1"],  # 보라색
            THEME["accent3"],  # 초록색
            THEME["accent3"],  # 초록색
            THEME["accent5"],  # 시안색
            THEME["accent4"],  # 빨간색
            THEME["accent4"],  # 빨간색
            THEME["accent1"],  # 보라색
            THEME["accent2"],  # 파란색
        ]
        return colors[index % len(colors)]

    def get_available_font(self, font_options):
        """사용 가능한 첫 번째 폰트 반환"""
        from PyQt5.QtGui import QFontDatabase

        font_db = QFontDatabase()
        available_fonts = font_db.families()

        # 사용 가능한 폰트 중 첫 번째 옵션 선택
        for font in font_options:
            # Qt는 대소문자를 구분하므로 정확한 일치를 확인
            for available_font in available_fonts:
                if font.lower() == available_font.lower():
                    return available_font

        # 모든 옵션이 없으면 시스템 기본 폰트 사용
        return font_options[-1]

    def calculate_scale_factor(self):
        """화면 크기에 따른 스케일 팩터 계산"""
        # 기준 크기 (설계시 기준)
        base_width, base_height = self.base_width, self.base_height

        # 현재 화면 크기
        current_width, current_height = self.width(), self.height()

        # 너비와 높이 중 더 제한적인 요소 기준으로 스케일 팩터 계산
        width_factor = current_width / base_width
        height_factor = current_height / base_height

        # 두 요소 중 더 작은 값을 사용하여 왜곡 방지
        self.scale_factor = min(width_factor, height_factor)

        return self.scale_factor

    def init_ui(self):
        try:
            icon_path = get_resource_path("app_icon.ico")
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"아이콘 설정 오류: {e}")

        self.setWindowTitle("Greek letters & Mathematical Symbols")
        self.setGeometry(100, 100, self.base_width, self.base_height)

        # 최대화 버튼 제거
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # 최소 크기 설정
        self.setMinimumSize(350, 500)
        self.setMaximumSize(500, 800)

        # 중앙 위젯과 레이아웃 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(10)

        # 출력 모드 선택 영역
        output_mode_container = QWidget()
        output_mode_layout = QHBoxLayout(output_mode_container)
        output_mode_layout.setContentsMargins(0, 5, 0, 5)

        # 출력 모드 라벨
        self.output_mode_label = QLabel("Output Mode:")
        self.output_mode_label.setFont(QFont(self.default_font_family, 10, QFont.Bold))
        self.output_mode_label.setStyleSheet(f"color: {THEME['foreground']};")
        output_mode_layout.addWidget(self.output_mode_label)

        # 라디오 버튼 그룹
        self.mode_group = QButtonGroup(self)

        # 일반 모드 라디오 버튼
        self.regular_mode_radio = QRadioButton("Regular")
        self.regular_mode_radio.setChecked(True)  # 기본값: 일반 모드
        self.regular_mode_radio.toggled.connect(self.toggle_output_mode)
        self.regular_mode_radio.setStyleSheet(
            f"""
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
        )
        self.mode_group.addButton(self.regular_mode_radio)
        output_mode_layout.addWidget(self.regular_mode_radio)

        # LaTeX 모드 라디오 버튼
        self.latex_mode_radio = QRadioButton("LaTeX")
        self.latex_mode_radio.toggled.connect(self.toggle_output_mode)
        self.latex_mode_radio.setStyleSheet(
            f"""
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
        )
        self.mode_group.addButton(self.latex_mode_radio)
        output_mode_layout.addWidget(self.latex_mode_radio)

        # 여백 추가 (라디오 버튼과 핀 버튼 사이의 공간)
        output_mode_layout.addStretch()

        # 항상 위에 표시 버튼 (핀 버튼)
        self.always_on_top_button = QPushButton("📌")
        # 버튼 크기 설정 (정사각형으로)
        button_size = 24
        self.always_on_top_button.setFixedSize(button_size, button_size)
        # 도구 팁 설정
        self.always_on_top_button.setToolTip("Set Always on Top")
        # 클릭 이벤트 연결
        self.always_on_top_button.clicked.connect(self.toggle_always_on_top)
        # 상태 추적 변수
        self.is_always_on_top = False
        # 스타일 설정
        self.always_on_top_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {THEME['button_bg']};
                color: {THEME['foreground']};
                border: 1px solid {THEME['button_border']};
                border-radius: 4px;
                padding: 2px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {THEME['button_hover']};
            }}
        """
        )
        output_mode_layout.addWidget(self.always_on_top_button)

        self.main_layout.addWidget(output_mode_container)

        # 최근 사용 항목 표시 영역
        recent_container = QWidget()
        recent_container_layout = QVBoxLayout(recent_container)
        recent_container_layout.setContentsMargins(0, 0, 0, 0)

        # 최근 사용 라벨
        self.recent_label = QLabel("Recently used:")
        self.recent_label.setFont(QFont(self.default_font_family, 10, QFont.Bold))
        self.recent_label.setStyleSheet(f"color: {THEME['foreground']};")
        recent_container_layout.addWidget(self.recent_label)

        # 스크롤 영역 생성
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )  # 세로 스크롤만 사용
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )  # 필요할 때만 세로 스크롤 표시
        self.scroll_area.setFrameShape(QFrame.StyledPanel)  # 테두리 추가

        # 스크롤바 스타일 설정
        self.scroll_area.setStyleSheet(
            f"""
            QScrollArea {{
                border: 1px solid {THEME['button_border']};
                border-radius: 4px;
                background-color: {THEME['light_bg']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {THEME['dark_bg']};
                width: 8px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {THEME['button_border']};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical {{
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QScrollBar::sub-line:vertical {{
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """
        )

        # 스크롤 영역 내부 위젯 생성
        self.recent_container_widget = QWidget()
        self.recent_container_widget.setStyleSheet(
            f"background-color: {THEME['light_bg']};"
        )
        self.recent_layout = QFlowLayout(self.recent_container_widget)
        self.recent_layout.setContentsMargins(3, 3, 3, 3)  # 약간의 안쪽 여백 추가

        # 스크롤 영역에 위젯 설정
        self.scroll_area.setWidget(self.recent_container_widget)

        # 스크롤 영역의 최대 높이 설정 (전체 창 높이의 약 30%)
        self.scroll_area.recent_scroll_height_ratio = 0.3
        self.update_recent_scroll_height()

        # 레이아웃에 스크롤 영역 추가
        recent_container_layout.addWidget(self.scroll_area)

        self.main_layout.addWidget(recent_container)

        # 구분선
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {THEME['button_border']};")
        self.main_layout.addWidget(line)

        # 카테고리 버튼 컨테이너
        button_container = QWidget()
        button_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_layout = QVBoxLayout(button_container)
        self.button_layout.setSpacing(5)

        # 카테고리 버튼 생성
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

        # 버튼 객체 저장용 리스트
        self.category_buttons = []

        for i, (category_name, create_func) in enumerate(categories):
            button = QPushButton(category_name)
            button.setFont(QFont(self.default_font_family, 9))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setMinimumHeight(30)

            # 카테고리별 테두리 색상 설정
            border_color = self.get_category_color(i)

            # 버튼 스타일 설정
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {THEME['button_bg']};
                    color: {THEME['foreground']};
                    border: 1px solid {border_color};
                    border-radius: 4px;
                    
                    /* 내부 패딩 설정 - 버튼 내부 여백 */
                    padding-top: 3px;
                    padding-bottom: 3px;
                    padding-left: 12px;
                    padding-right: 12px;
                    
                    /* 외부 마진 설정 - 버튼 간 간격 */
                    margin-top: 3px;
                    margin-bottom: 3px;
                    margin-left: 2px;
                    margin-right: 2px;
            
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {border_color};
                    color: {THEME['dark_bg']};
                }}
            """
            )

            button.clicked.connect(
                lambda checked, f=create_func, idx=i: self.show_symbols_menu(f, idx)
            )
            self.button_layout.addWidget(button)
            self.category_buttons.append(button)

        self.main_layout.addWidget(button_container)

        # 상태바 생성
        self.statusBar().showMessage("Select a symbol to copy to clipboard")
        self.statusBar().setStyleSheet(
            f"""
            background-color: {THEME['light_bg']};
            color: {THEME['foreground']};
            """
        )

        # 테마 전환 버튼을 상태바 오른쪽에 추가
        self.theme_toggle_btn = QPushButton("🌙" if self.is_dark_mode else "☀️")
        self.theme_toggle_btn.setToolTip("Toggle Dark/Light Theme")
        self.theme_toggle_btn.setFixedSize(24, 24)
        self.theme_toggle_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {THEME['button_bg']};
                color: {THEME['foreground']};
                border: 1px solid {THEME['button_border']};
                border-radius: 4px;
                padding: 2px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {THEME['button_hover']};
            }}
            """
        )
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        
        # 상태바에 영구 위젯으로 추가
        self.statusBar().addPermanentWidget(self.theme_toggle_btn)

        # 메뉴 폰트 크기 초기화
        self.symbol_font_size = 16
        self.name_font_size = 10

        # 최근 사용 항목 업데이트
        self.update_recent_symbols()

        # 반응형 디자인을 위한 이벤트 연결
        self.resized.connect(self.on_resize)

    def toggle_always_on_top(self):
        """항상 위에 표시 기능 토글"""
        self.is_always_on_top = not self.is_always_on_top

        # 윈도우 플래그 설정
        if self.is_always_on_top:
            # 항상 위에 표시 활성화
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            # 버튼 스타일 변경 (활성화 상태 표시)
            self.always_on_top_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {THEME['accent2']};
                    color: {THEME['dark_bg']};
                    border: 1px solid {THEME['accent2']};
                    border-radius: 4px;
                    padding: 2px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                }}
            """
            )
        else:
            # 항상 위에 표시 비활성화
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            # 버튼 스타일 원래대로 변경
            self.always_on_top_button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {THEME['button_bg']};
                    color: {THEME['foreground']};
                    border: 1px solid {THEME['button_border']};
                    border-radius: 4px;
                    padding: 2px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                }}
            """
            )

        # 윈도우 플래그가 변경되면 창이 숨겨지므로 다시 표시
        self.show()

        # 상태바 메시지 업데이트
        message = (
            "Always on top: Enabled"
            if self.is_always_on_top
            else "Always on top: Disabled"
        )
        self.statusBar().showMessage(message, 2000)

    def update_recent_scroll_height(self):
        """창 크기에 따라 최근 항목 스크롤 영역 높이 업데이트"""
        if hasattr(self, "recent_scroll_area"):
            # 현재 창 높이의 일정 비율로 설정
            new_height = int(self.height() * self.recent_scroll_height_ratio)
            # 최소값과 최대값 제한
            new_height = max(120, min(250, new_height))
            self.recent_scroll_area.setMaximumHeight(new_height)

    def resizeEvent(self, event: QResizeEvent):
        """윈도우 크기 변경 이벤트 처리"""
        self.resized.emit()
        self.calculate_scale_factor()
        # 스크롤 영역 높이 업데이트
        self.update_recent_scroll_height()
        return super().resizeEvent(event)

    def toggle_theme(self):
        """다크 모드와 라이트 모드 전환"""
        self.is_dark_mode = not self.is_dark_mode
        
        # 전역 테마 변수 업데이트
        global THEME
        THEME = DARK_THEME if self.is_dark_mode else LIGHT_THEME
        
        # 테마 토글 버튼 아이콘 변경
        self.theme_toggle_btn.setText("🌙" if self.is_dark_mode else "☀️")
        
        # 전체 UI 테마 적용
        self.apply_theme()
        
        # 출력 모드 라벨 업데이트
        self.output_mode_label.setStyleSheet(f"color: {THEME['foreground']};")
        
        # 라디오 버튼 업데이트
        self.regular_mode_radio.setStyleSheet(
            f"""
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
        )
        
        self.latex_mode_radio.setStyleSheet(
            f"""
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
        )
        
        # 최근 사용 라벨 업데이트
        self.recent_label.setStyleSheet(f"color: {THEME['foreground']};")
        
        # 스크롤 영역 스타일 업데이트
        self.scroll_area.setStyleSheet(
            f"""
            QScrollArea {{
                border: 1px solid {THEME['button_border']};
                border-radius: 4px;
                background-color: {THEME['light_bg']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {THEME['dark_bg']};
                width: 8px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {THEME['button_border']};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical {{
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QScrollBar::sub-line:vertical {{
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """
        )
        
        # 최근 항목 컨테이너 배경색 업데이트
        self.recent_container_widget.setStyleSheet(
            f"background-color: {THEME['light_bg']};"
        )
        
        # 구분선 색상 업데이트
        self.separator_line = QFrame()
        self.separator_line.setStyleSheet(f"background-color: {THEME['button_border']};")

                
        # 카테고리 버튼 업데이트
        for i, button in enumerate(self.category_buttons):
            border_color = self.get_category_color(i)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {THEME['button_bg']};
                    color: {THEME['foreground']};
                    border: 1px solid {border_color};
                    border-radius: 4px;
                    padding-top: 3px;
                    padding-bottom: 3px;
                    padding-left: 12px;
                    padding-right: 12px;
                    margin-top: 3px;
                    margin-bottom: 3px;
                    margin-left: 2px;
                    margin-right: 2px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {border_color};
                    color: {THEME['dark_bg' if self.is_dark_mode else 'background']};
                }}
            """)
        
        # Always on Top 버튼 스타일 업데이트
        if self.is_always_on_top:
            self.always_on_top_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {THEME['accent2']};
                    color: {THEME['dark_bg' if self.is_dark_mode else 'background']};
                    border: 1px solid {THEME['accent2']};
                    border-radius: 4px;
                    padding: 2px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                }}
            """)
        else:
            self.always_on_top_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {THEME['button_bg']};
                    color: {THEME['foreground']};
                    border: 1px solid {THEME['button_border']};
                    border-radius: 4px;
                    padding: 2px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                }}
            """)
        
        # 테마 토글 버튼 스타일 업데이트
        self.theme_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['button_bg']};
                color: {THEME['foreground']};
                border: 1px solid {THEME['button_border']};
                border-radius: 4px;
                padding: 2px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {THEME['button_hover']};
            }}
        """)
        
        # 최근 사용 목록 업데이트
        self.update_recent_symbols()
        
        # 상태바 메시지 업데이트
        theme_text = "Dark" if self.is_dark_mode else "Light"
        self.statusBar().showMessage(f"Switched to {theme_text} theme", 2000)
        
        # 상태바 스타일 업데이트
        self.statusBar().setStyleSheet(
            f"""
            background-color: {THEME['light_bg']};
            color: {THEME['foreground']};
            """
        )
    def apply_theme(self):
        """현재 테마 적용"""
        # 애플리케이션 스타일 설정
        app = QApplication.instance()
        app.setStyle("Fusion")

        # 메인 윈도우 배경색 설정
        self.setStyleSheet(
            f"""
            QMainWindow, QWidget {{
                background-color: {THEME['background']};
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
            """
        )
    def toggle_output_mode(self):
        """출력 모드 전환 처리"""
        self.latex_mode = self.latex_mode_radio.isChecked()
        # 최근 사용 목록 업데이트 (표시 방식 변경)
        self.update_recent_symbols()

        # 상태바 메시지 업데이트
        mode_text = "LaTeX" if self.latex_mode else "Regular"
        self.statusBar().showMessage(f"Switched to {mode_text} mode", 2000)

    def resizeEvent(self, event: QResizeEvent):
        """윈도우 크기 변경 이벤트 처리"""
        self.resized.emit()
        self.calculate_scale_factor()
        return super().resizeEvent(event)

    def on_resize(self):
        """윈도우 크기에 따라 폰트 및 버튼 크기 조정 - 최근 사용 목록 포함"""
        # 현재 창 크기 기반으로 스케일 팩터 계산
        scale_factor = self.scale_factor

        # 폰트 크기 계산 (윈도우 크기에 비례)
        base_font_size = max(8, min(12, int(10 * scale_factor)))
        button_font_size = max(8, min(11, int(9 * scale_factor)))

        # 메뉴 폰트 크기 계산
        self.symbol_font_size = max(12, min(18, int(16 * scale_factor)))
        self.name_font_size = max(8, min(12, int(10 * scale_factor)))

        # 최근 사용 버튼 폰트 크기 계산
        recent_size = max(8, min(10, int(9 * scale_factor)))

        # 카테고리 버튼 높이 계산
        button_height = max(25, int(base_font_size * 4))

        # 카테고리 버튼 업데이트
        for button in self.category_buttons:
            button.setFont(QFont(self.default_font_family, button_font_size))
            button.setMinimumHeight(button_height)

        # 최근 사용 버튼 업데이트
        for i in range(self.recent_layout.count()):
            item = self.recent_layout.itemAt(i)
            if item and item.widget():
                button = item.widget()
                if isinstance(button, QPushButton):
                    # 모드에 따른 폰트 크기 조정
                    button.setFont(QFont(self.default_font_family, recent_size))

                    # 버튼 높이 조정 (가로 크기는 내용에 맞게 자동 조정)
                    button_height_recent = max(25, min(32, int(30 * scale_factor)))
                    button.setMinimumHeight(button_height_recent)

                    # 패딩 조정
                    padding_h = max(3, min(8, int(6 * scale_factor)))
                    padding_v = max(2, min(5, int(4 * scale_factor)))

                    # 스타일시트 업데이트 (도쿄나잇 테마 유지)
                    button.setStyleSheet(
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
        for i, button in enumerate(self.category_buttons):
            button.setFont(QFont(self.default_font_family, button_font_size))
            button.setMinimumHeight(button_height)

            # 화면 크기에 따른 패딩과 마진 계산
            min_padding_v = max(4, int(5 * scale_factor))
            min_padding_h = max(8, int(10 * scale_factor))
            min_margin = max(2, int(3 * scale_factor))

            # 카테고리별 테두리 색상 설정
            border_color = self.get_category_color(i)

            # 스타일시트 업데이트
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {THEME['button_bg']};
                    color: {THEME['foreground']};
                    border: 1px solid {border_color};
                    border-radius: 4px;
                    
                    /* 내부 패딩 설정 - 버튼 내부 여백 */
                    padding-top: {min_padding_v}px;
                    padding-bottom: {min_padding_v}px;
                    padding-left: {min_padding_h}px;
                    padding-right: {min_padding_h}px;
                    
                    /* 외부 마진 설정 - 버튼 간 간격 */
                    margin-top: {min_margin}px;
                    margin-bottom: {min_margin}px;
                    margin-left: {min_margin}px;
                    margin-right: {min_margin}px;
                    
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {border_color};
                    color: {THEME['dark_bg']};
                }}
            """
            )

    def show_symbols_menu(self, create_func, category_index=0):
        # 메뉴 생성
        menu = QMenu(self)

        # 카테고리에 맞는 강조색 가져오기
        accent_color = self.get_category_color(category_index)

        # 메뉴 스타일 설정
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

        # 메뉴 내용 생성
        create_func(menu)

        # 마우스 커서 위치에 메뉴 표시
        button = self.sender()
        if button:
            pos = button.mapToGlobal(QPoint(button.width(), 0))
            menu.exec_(pos)

    def create_symbol_menu_item(self, menu, symbol, latex, name):
        """특수문자를 위한 메뉴 항목 생성"""
        # 위젯 액션 사용
        action = QWidgetAction(menu)

        # 사용자 정의 라벨 생성
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

        layout.addWidget(symbol_label)
        layout.addWidget(name_label)
        layout.addStretch()

        # 그림자 효과 추가
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

        # 위젯 액션에 컨테이너 설정
        action.setDefaultWidget(container)

        # 메뉴에 액션 추가
        menu.addAction(action)

        # 클릭 이벤트 연결
        container.mousePressEvent = lambda event: self.copy_symbol(symbol, latex, name)

        return action

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
            ("𝒻", r"\mathcal{f}", "Script f"),  # 함수, 확률 밀도 함수
            ("𝒽", r"\mathcal{h}", "Script h"),  # 엔트로피 함수, 플랑크 관련
            ("𝒾", r"\mathcal{i}", "Script i"),  # 허수 단위 변형
            ("𝓁", r"\mathcal{l}", "Script l"),  # 라그랑지안, 손실 함수
            ("𝓂", r"\mathcal{m}", "Script m"),  # 측도(measure)
            ("𝓃", r"\mathcal{n}", "Script n"),  # 수치 함수
            ("𝓅", r"\mathcal{p}", "Script p"),  # 확률 분포
            ("𝓇", r"\mathcal{r}", "Script r"),  # 상관 함수
            ("𝓉", r"\mathcal{t}", "Script t"),  # 시간 함수
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

    def copy_symbol(self, symbol, latex, name):
        # 클립보드에 복사 (모드에 따라 다른 내용 복사)
        clipboard = QApplication.clipboard()
        if self.latex_mode:
            # LaTeX 모드일 때는 LaTeX 코드 복사
            clipboard.setText(latex, QClipboard.Clipboard)
            copied_text = latex
        else:
            # 일반 모드일 때는 심볼 복사
            clipboard.setText(symbol, QClipboard.Clipboard)
            copied_text = symbol

        # 최근 사용 목록에
        self.add_to_recent_symbols(symbol, latex, name)

        # 상태바 메시지 업데이트
        mode_text = "LaTeX" if self.latex_mode else "symbol"
        self.statusBar().showMessage(
            f"Copied {mode_text}: {copied_text} ({name})", 2000
        )

    def add_to_recent_symbols(self, symbol, latex, name):
        # 이미 목록에 있는지 확인
        for i, (s, l, n) in enumerate(self.recent_symbols):
            if s == symbol:
                # 있으면 제거 (나중에 맨 앞에 )
                self.recent_symbols.pop(i)
                break

        # 맨 앞에
        self.recent_symbols.insert(0, (symbol, latex, name))

        # 최대 15개만 유지
        if len(self.recent_symbols) > 15:
            self.recent_symbols.pop()

        # 화면 업데이트
        self.update_recent_symbols()

    def update_recent_symbols(self):
        """최근 사용 기호 목록 업데이트 - 모든 모드에서 내용에 맞게 버튼 크기 자동 조정"""
        # 기존 버튼 제거
        for i in range(self.recent_layout.count()):
            item = self.recent_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                self.recent_layout.removeItem(item)

        # 최근 사용 항목이 없으면 빈 레이블 추가
        if not self.recent_symbols:
            empty_label = QLabel("None")
            empty_label.setStyleSheet(f"color: {THEME['foreground']};")
            self.recent_layout.addWidget(empty_label)
            return

        # 윈도우 크기에 따른 폰트 크기 계산
        scale_factor = self.scale_factor
        recent_size = max(8, min(10, int(9 * scale_factor)))

        # 모드에 따라 표시할 내용 결정
        for symbol, latex, name in self.recent_symbols:
            # 버튼 생성 - 모드에 따라 내용만 다르게
            button = QPushButton()

            # 버튼에 모드 속성 추가 (on_resize에서 사용)
            button.setProperty("mode", "latex" if self.latex_mode else "symbol")

            # 모드에 따라 표시 내용 및 폰트 설정
            if self.latex_mode:
                button.setText(latex)
                button.setToolTip(f"{symbol} | {name}")
                button.setFont(QFont(self.default_font_family, recent_size))
            else:
                button.setText(symbol)
                button.setToolTip(f"{latex} | {name}")
                button.setFont(QFont(self.default_font_family, recent_size))

            # 내용에 맞게 자동 크기 조정
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

            # 버튼 높이 설정
            button_height = max(25, min(32, int(30 * scale_factor)))
            button.setMinimumHeight(button_height)

            # 패딩 조정
            padding_h = max(3, min(8, int(6 * scale_factor)))
            padding_v = max(2, min(5, int(4 * scale_factor)))

            # 그림자 효과 추가
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {THEME['button_bg']};
                    color: {THEME['foreground']};
                    padding: {padding_v}px {padding_h}px;
                    margin: 2px;
                    border: 1px solid {THEME['button_border']};
                    border-radius: 4px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }}
                QPushButton:hover {{
                    background-color: {THEME['button_hover']};
                    border: 1px solid {THEME['accent2']};
                }}
            """
            )

            # 클릭 이벤트 연결
            button.clicked.connect(
                lambda checked, s=symbol, l=latex, n=name: self.copy_symbol(s, l, n)
            )

            # 레이아웃에 버튼 추가
            self.recent_layout.addWidget(button)


def main():
    app = QApplication(sys.argv)

    # 고해상도 디스플레이 지원
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # 애플리케이션 스타일 설정
    app.setStyle("Fusion")

    window = SymbolApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
