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
    QGridLayout,
    QWidgetAction,
)
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QClipboard, QResizeEvent
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


class SymbolLabel(QLabel):
    """심볼을 표시하기 위한 라벨"""

    clicked = pyqtSignal(str, str)

    def __init__(self, symbol, name, parent=None):
        super().__init__(parent)
        self.symbol = symbol
        self.name = name

        # 텍스트 설정 (심볼은 더 크게)
        self.symbol_font = QFont("Arial", 16, QFont.Bold)
        self.name_font = QFont("Arial", 10)
        self.update_text()

        # 마우스 이벤트 추적
        self.setMouseTracking(True)

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
            self.clicked.emit(self.symbol, self.name)
        super().mousePressEvent(event)


class SymbolApp(QMainWindow):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 최근 사용된 문자 배열 초기화 (최대 7개 저장)
        self.recent_symbols = []

        self.init_ui()

    def init_ui(self):

        try:
            icon_path = get_resource_path("app_icon.ico")
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"아이콘 설정 오류: {e}")

        self.setWindowTitle("Greek letters & Mathematical Symbols")

        self.setWindowTitle("Greek letters & Mathematical Symbols")
        self.setGeometry(100, 100, 400, 600)

        # 최대화 버튼 제거
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # 최소 크기 설정
        self.setMinimumSize(300, 450)
        self.setMaximumSize(400, 600)

        # 중앙 위젯과 레이아웃 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(10)

        # 최근 사용 항목 표시 영역
        recent_container = QWidget()
        recent_container_layout = QVBoxLayout(recent_container)
        recent_container_layout.setContentsMargins(0, 0, 0, 0)

        # 최근 사용 라벨
        recent_label = QLabel("Recently used:")
        recent_label.setFont(QFont("Arial", 10, QFont.Bold))
        recent_container_layout.addWidget(recent_label)

        # 최근 사용 버튼 레이아웃
        self.recent_layout = QHBoxLayout()
        self.recent_layout.setSpacing(5)
        recent_container_layout.addLayout(self.recent_layout)

        self.main_layout.addWidget(recent_container)

        # 구분선
        line = QLabel()
        line.setFrameShape(QLabel.HLine)
        line.setFrameShadow(QLabel.Sunken)
        self.main_layout.addWidget(line)

        # 카테고리 버튼 컨테이너
        button_container = QWidget()
        button_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_layout = QVBoxLayout(button_container)
        self.button_layout.setSpacing(5)

        # 카테고리 버튼 생성
        categories = [
            ("lowercase greek letters", self.create_lowercase_greek),
            ("capital greek letters", self.create_uppercase_greek),
            ("Math/Engineering Symbols", self.create_math_symbols),
            ("Vector/Matrix Operations", self.create_vector_symbols),
            ("set theory", self.create_set_symbols),
            ("Logical operations", self.create_logic_symbols),
            ("Probability", self.create_stat_symbols),
            ("Physics", self.create_physics_symbols),
            ("Calculus", self.create_calculus_symbols),
            ("AI/ML", self.create_ai_symbols),
            ("Definition/Equation/Relationship", self.create_relation_symbols),
        ]

        # 버튼 객체 저장용 리스트
        self.category_buttons = []

        for category_name, create_func in categories:
            button = QPushButton(category_name)
            button.setFont(QFont("Arial", 9))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setMinimumHeight(30)
            button.clicked.connect(
                lambda checked, f=create_func: self.show_symbols_menu(f)
            )
            self.button_layout.addWidget(button)
            self.category_buttons.append(button)

        self.main_layout.addWidget(button_container)

        # 상태바 생성
        self.statusBar().showMessage("Select a symbol to copy to clipboard")

        # 메뉴 폰트 크기 초기화
        self.symbol_font_size = 16
        self.name_font_size = 10

        # 최근 사용 항목 업데이트
        self.update_recent_symbols()

        # 반응형 디자인을 위한 이벤트 연결
        self.resized.connect(self.on_resize)

    def resizeEvent(self, event: QResizeEvent):
        """윈도우 크기 변경 이벤트 처리"""
        self.resized.emit()
        return super().resizeEvent(event)

    def on_resize(self):
        """윈도우 크기에 따라 폰트 및 버튼 크기 조정"""
        width = self.width()
        height = self.height()

        # 폰트 크기 계산 (윈도우 크기에 비례)
        base_font_size = max(8, min(12, int(width / 40)))
        button_font_size = max(8, min(11, int(width / 45)))

        # 메뉴 폰트 크기 계산
        self.symbol_font_size = max(12, min(18, int(width / 30)))
        self.name_font_size = max(8, min(12, int(width / 45)))

        # 최근 사용 버튼 크기 계산
        recent_button_size = max(25, min(40, int(width / 12)))

        # 카테고리 버튼 높이 계산
        button_height = max(25, min(35, int(height / 20)))

        # 폰트 및 버튼 크기 업데이트
        for button in self.findChildren(QPushButton):
            if button in self.category_buttons:
                button.setFont(QFont("Arial", button_font_size))
                button.setMinimumHeight(button_height)
            else:  # 최근 사용 버튼
                button.setFont(QFont("Arial", base_font_size + 2))
                button.setFixedSize(recent_button_size, recent_button_size)

    def show_symbols_menu(self, create_func):
        # 메뉴 생성
        menu = QMenu(self)
        menu.setStyleSheet(
            f"""
            QMenu {{
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 25px 8px 25px;
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

    def create_symbol_menu_item(self, menu, symbol, name):
        """특수문자를 위한 메뉴 항목 생성"""
        # 위젯 액션 사용
        action = QWidgetAction(menu)

        # 사용자 정의 라벨 생성
        label = QLabel(f"{symbol}  ({name})")

        # 심볼 텍스트에 다른 폰트 적용
        symbol_font = QFont("Arial", self.symbol_font_size, QFont.Bold)
        label.setFont(symbol_font)

        # 패딩 및 여백 설정
        label.setContentsMargins(10, 5, 10, 5)

        # 위젯 액션에 라벨 설정
        action.setDefaultWidget(label)

        # 메뉴에 액션 추가
        menu.addAction(action)

        # 클릭 이벤트 연결
        action.triggered.connect(lambda: self.copy_symbol(symbol, name))

        return action

    def create_lowercase_greek(self, menu):
        symbols = [
            ("α", "alpha"),
            ("β", "beta"),
            ("γ", "gamma"),
            ("δ", "delta"),
            ("ε", "epsilon"),
            ("ζ", "zeta"),
            ("η", "eta"),
            ("θ", "theta"),
            ("ι", "iota"),
            ("κ", "kappa"),
            ("λ", "lambda"),
            ("μ", "mu"),
            ("ν", "nu"),
            ("ξ", "xi"),
            ("ο", "omicron"),
            ("π", "pi"),
            ("ρ", "rho"),
            ("σ", "sigma"),
            ("τ", "tau"),
            ("υ", "upsilon"),
            ("φ", "phi"),
            ("χ", "chi"),
            ("ψ", "psi"),
            ("ω", "omega"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_uppercase_greek(self, menu):
        symbols = [
            ("Α", "Alpha"),
            ("Β", "Beta"),
            ("Γ", "Gamma"),
            ("Δ", "Delta"),
            ("Ε", "Epsilon"),
            ("Ζ", "Zeta"),
            ("Η", "Eta"),
            ("Θ", "Theta"),
            ("Ι", "Iota"),
            ("Κ", "Kappa"),
            ("Λ", "Lambda"),
            ("Μ", "Mu"),
            ("Ν", "Nu"),
            ("Ξ", "Xi"),
            ("Ο", "Omicron"),
            ("Π", "Pi"),
            ("Ρ", "Rho"),
            ("Σ", "Sigma"),
            ("Τ", "Tau"),
            ("Υ", "Upsilon"),
            ("Φ", "Phi"),
            ("Χ", "Chi"),
            ("Ψ", "Psi"),
            ("Ω", "Omega"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_math_symbols(self, menu):
        symbols = [
            ("∑", "Sum"),
            ("∏", "Product"),
            ("∂", "Partial"),
            ("∇", "Nabla"),
            ("∞", "Infinity"),
            ("∫", "Integral"),
            ("≈", "Approximately"),
            ("≠", "Not Equal"),
            ("≤", "Less Than or Equal"),
            ("≥", "Greater Than or Equal"),
            ("∈", "Element Of"),
            ("⊂", "Subset"),
            ("∩", "Intersection"),
            ("∪", "Union"),
            ("→", "Right Arrow"),
            ("←", "Left Arrow"),
            ("↔", "Double Arrow"),
            ("≡", "Identical To"),
            ("≅", "Congruent To"),
            ("≜", "Defined As"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_vector_symbols(self, menu):
        symbols = [
            ("·", "Dot Product"),
            ("×", "Cross Product"),
            ("⊗", "Tensor Product"),
            ("⊕", "Direct Sum"),
            ("⟨", "Left Angle Bracket"),
            ("⟩", "Right Angle Bracket"),
            ("‖", "Norm"),
            ("⊥", "Perpendicular"),
            ("∥", "Parallel"),
            ("†", "Conjugate Transpose"),
            ("⊙", "Hadamard Product"),
            ("⨂", "Kronecker Product"),
            ("⨁", "Direct Sum Operator"),
            ("⟦", "Left Double Bracket"),
            ("⟧", "Right Double Bracket"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_set_symbols(self, menu):
        symbols = [
            ("∅", "Empty Set"),
            ("∀", "For All"),
            ("∃", "There Exists"),
            ("∄", "Does Not Exist"),
            ("∉", "Not Element Of"),
            ("⊄", "Not Subset"),
            ("⊆", "Subset or Equal"),
            ("⊇", "Superset or Equal"),
            ("⊊", "Proper Subset"),
            ("⊋", "Proper Superset"),
            ("ℕ", "Natural Numbers"),
            ("ℤ", "Integers"),
            ("ℚ", "Rational Numbers"),
            ("ℝ", "Real Numbers"),
            ("ℂ", "Complex Numbers"),
            ("ℙ", "Prime Numbers"),
            ("△", "Symmetric Difference"),
            ("×", "Cartesian Product"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_logic_symbols(self, menu):
        symbols = [
            ("¬", "Negation/Not"),
            ("∧", "Logical And"),
            ("∨", "Logical Or"),
            ("⊻", "Exclusive Or"),
            ("⇒", "Implies"),
            ("⇔", "If and Only If"),
            ("⊨", "Models/Entails"),
            ("⊢", "Proves"),
            ("□", "Necessary"),
            ("◊", "Possible"),
            ("⊤", "Top/True"),
            ("⊥", "Bottom/False"),
            ("≡", "Logical Equivalence"),
            ("⊦", "Assertion"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_stat_symbols(self, menu):
        symbols = [
            ("𝔼", "Expected Value"),
            ("ℙ", "Probability"),
            ("𝕍", "Variance"),
            ("√", "Square Root"),
            ("∝", "Proportional To"),
            ("±", "Plus-Minus"),
            ("∼", "Distributed As"),
            ("≫", "Much Greater Than"),
            ("≪", "Much Less Than"),
            ("μ̂", "mu hat - estimator"),
            ("σ̂", "sigma hat - estimator"),
            ("ρ", "rho - correlation"),
            ("χ²", "Chi-Squared"),
            ("σ²", "Variance"),
            ("⟂", "Independent"),
            ("∩", "Intersection/And"),
            ("∪", "Union/Or"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_physics_symbols(self, menu):
        symbols = [
            ("ℏ", "h-bar"),
            ("ψ", "wavefunction"),
            ("Ψ", "Wavefunction"),
            ("⟨ϕ|ψ⟩", "Bracket Notation"),
            ("⊗", "Tensor Product"),
            ("†", "Hermitian Conjugate"),
            ("°", "Degree"),
            ("∮", "Contour Integral"),
            ("∯", "Surface Integral"),
            ("∰", "Volume Integral"),
            ("∇²", "Laplacian"),
            ("×", "Curl Operator"),
            ("γ", "Lorentz Factor"),
            ("Λ", "Lambda/Cosmological Constant"),
            ("⟨Â⟩", "Expectation Value"),
            ("⨂", "Tensor Product Operator"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_calculus_symbols(self, menu):
        symbols = [
            ("∫", "Indefinite Integral"),
            ("∬", "Double Integral"),
            ("∭", "Triple Integral"),
            ("∮", "Contour Integral"),
            ("∯", "Surface Integral"),
            ("∰", "Volume Integral"),
            ("∂x", "Partial wrt x"),
            ("∂y", "Partial wrt y"),
            ("∂z", "Partial wrt z"),
            ("∂t", "Partial wrt t"),
            ("′", "Prime/Derivative"),
            ("″", "Double Prime"),
            ("dx", "Differential x"),
            ("∇f", "Gradient"),
            ("lim", "Limit"),
            ("δ", "Variation/Functional Derivative"),
            ("ε", "Epsilon/Small Quantity"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_ai_symbols(self, menu):
        symbols = [
            ("∇θ", "Gradient wrt Parameters"),
            ("∑", "Summation"),
            ("∏", "Product"),
            ("𝔼", "Expected Value"),
            ("ℙ", "Probability"),
            ("𝕍", "Variance"),
            ("⊗", "Tensor Product"),
            ("⊕", "Direct Sum"),
            ("⊙", "Hadamard Product"),
            ("∥W∥", "Norm of Weights"),
            ("θ̂", "Parameter Estimate"),
            ("ŷ", "Prediction"),
            ("𝓛", "Loss Function"),
            ("∂𝓛/∂θ", "Gradient of Loss"),
            ("≈", "Approximately Equal"),
            ("σ", "Activation Function/Sigmoid"),
            ("ϕ", "Feature Map"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def create_relation_symbols(self, menu):
        symbols = [
            ("≡", "Identical To"),
            ("≅", "Congruent To"),
            ("≈", "Approximately Equal"),
            ("≠", "Not Equal"),
            ("≤", "Less Than or Equal"),
            ("≥", "Greater Than or Equal"),
            ("≪", "Much Less Than"),
            ("≫", "Much Greater Than"),
            ("∝", "Proportional To"),
            ("≜", "Defined As"),
            ("≝", "Equal By Definition"),
            ("≐", "Approaches Limit"),
            ("≙", "Estimates"),
            ("≟", "Questioned Equal To"),
            ("≣", "Strictly Equivalent To"),
            ("⩵", "Double-Line Equal"),
            ("≑", "Geometrically Equal"),
            ("≒", "Approximately Equal/Congruent"),
        ]
        for symbol, name in symbols:
            action = QAction(f"{symbol}  ({name})", self)
            action.triggered.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            menu.addAction(action)

    def copy_symbol(self, symbol, name):
        # 클립보드에 복사
        clipboard = QApplication.clipboard()
        clipboard.setText(symbol, QClipboard.Clipboard)

        # 최근 사용 목록에 추가
        self.add_to_recent_symbols(symbol, name)

        # 상태바 메시지 업데이트
        self.statusBar().showMessage(f"Copied: {symbol} ({name})", 2000)

    def add_to_recent_symbols(self, symbol, name):
        # 이미 목록에 있는지 확인
        for i, (s, n) in enumerate(self.recent_symbols):
            if s == symbol:
                # 있으면 제거 (나중에 맨 앞에 추가)
                self.recent_symbols.pop(i)
                break

        # 맨 앞에 추가
        self.recent_symbols.insert(0, (symbol, name))

        # 최대 7개만 유지
        if len(self.recent_symbols) > 7:
            self.recent_symbols.pop()

        # 화면 업데이트
        self.update_recent_symbols()

    def update_recent_symbols(self):
        # 기존 버튼 제거
        while self.recent_layout.count():
            item = self.recent_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 최근 사용 항목이 없으면 빈 레이블 추가
        if not self.recent_symbols:
            empty_label = QLabel("None")
            self.recent_layout.addWidget(empty_label)
            self.recent_layout.addStretch()
            return

        # 윈도우 크기에 따른 버튼 크기 계산
        button_size = max(25, min(40, int(self.width() / 12)))

        # 최근 사용 항목 버튼 추가
        for symbol, name in self.recent_symbols:
            button = QPushButton(symbol)
            button.setToolTip(f"{symbol} ({name})")
            button.setFixedSize(button_size, button_size)
            button.setFont(QFont("Arial", 12))
            button.clicked.connect(
                lambda checked, s=symbol, n=name: self.copy_symbol(s, n)
            )
            self.recent_layout.addWidget(button)

        # 왼쪽 정렬을 위한 빈 공간 추가
        self.recent_layout.addStretch()

        # 반응형 UI 업데이트
        self.on_resize()


def main():
    app = QApplication(sys.argv)

    # 애플리케이션 스타일 설정
    app.setStyle("Fusion")
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    window = SymbolApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
