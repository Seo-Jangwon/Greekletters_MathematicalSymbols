# event_handlers.py
"""
이벤트 처리 및 사용자 상호작용 관리
"""

from PyQt5.QtWidgets import (
    QApplication,
    QMenu,
    QWidgetAction,
    QWidget,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QPushButton,
)
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QClipboard, QFont
from components import ToggleSwitch, DraggableButton
from constants import SCALE_LIMITS


class EventHandlers:
    """이벤트 처리 클래스"""

    def __init__(self, main_window):
        self.main_window = main_window

    def copy_symbol(self, symbol, latex, name):
        """심볼 복사 및 최근 사용 목록 업데이트"""
        clipboard = QApplication.clipboard()
        if self.main_window.latex_mode:
            clipboard.setText(latex, QClipboard.Clipboard)
            copied_text = latex
        else:
            clipboard.setText(symbol, QClipboard.Clipboard)
            copied_text = symbol

        self.add_to_recent_symbols(symbol, latex, name)

        mode_text = "LaTeX" if self.main_window.latex_mode else "symbol"
        self.main_window.statusBar().showMessage(
            f"Copied {mode_text}: {copied_text} ({name})", 2000
        )

    def add_to_recent_symbols(self, symbol, latex, name):
        """최근 사용 목록에 심볼 추가"""
        # 이미 목록에 있는지 확인
        for i, (s, l, n) in enumerate(self.main_window.recent_symbols):
            if s == symbol:
                self.main_window.recent_symbols.pop(i)
                break

        # 맨 앞에 추가
        self.main_window.recent_symbols.insert(0, (symbol, latex, name))

        # 최대 개수 제한
        if len(self.main_window.recent_symbols) > SCALE_LIMITS["max_recent_items"]:
            self.main_window.recent_symbols.pop()

        self.main_window.update_recent_symbols()

    def remove_from_recent_symbols(self, symbol):
        """최근 사용 목록에서 제거"""
        self.main_window.recent_symbols = [
            item for item in self.main_window.recent_symbols if item[0] != symbol
        ]
        self.main_window.update_recent_symbols()
        self.main_window.settings_manager.save_settings(self.main_window)
        self.main_window.statusBar().showMessage(
            f"Removed '{symbol}' from recent list", 2000
        )

    def add_to_favorites(self, symbol, latex, name):
        """즐겨찾기에 추가"""
        # 이미 존재하는지 확인
        if self.is_favorited(symbol):
            self.main_window.statusBar().showMessage(
                f"'{symbol}' is already in favorites", 2000
            )
            return

        # 최대 개수 확인
        if len(self.main_window.favorites) >= SCALE_LIMITS["max_favorites"]:
            self.main_window.statusBar().showMessage(
                f"Favorites limit reached ({SCALE_LIMITS['max_favorites']})", 3000
            )
            return

        self.main_window.favorites.append([symbol, latex, name])
        self.main_window.update_favorites_display()
        self.main_window.settings_manager.save_settings(self.main_window)
        self.main_window.statusBar().showMessage(
            f"Added '{symbol}' to favorites ({len(self.main_window.favorites)}/{SCALE_LIMITS['max_favorites']})",
            2000,
        )

    def remove_from_favorites(self, symbol):
        """즐겨찾기에서 제거"""
        self.main_window.favorites = [
            fav for fav in self.main_window.favorites if fav[0] != symbol
        ]
        self.main_window.update_favorites_display()
        self.main_window.settings_manager.save_settings(self.main_window)
        self.main_window.statusBar().showMessage(
            f"Removed '{symbol}' from favorites", 2000
        )

    def is_favorited(self, symbol):
        """심볼이 즐겨찾기에 있는지 확인"""
        return any(fav[0] == symbol for fav in self.main_window.favorites)

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

    def reorder_favorites(self, symbol_data, drop_pos):
        """즐겨찾기 내부 순서 변경"""
        # 기존 위치에서 제거
        symbol = symbol_data[0]
        item_to_move = None
        for i, fav in enumerate(self.main_window.favorites):
            if fav[0] == symbol:
                item_to_move = self.main_window.favorites.pop(i)
                break

        if not item_to_move:
            return

        # 드롭 위치 계산
        drop_index = self.calculate_drop_index(drop_pos)

        # 새 위치에 삽입
        self.main_window.favorites.insert(drop_index, item_to_move)
        self.main_window.update_favorites_display()
        self.main_window.settings_manager.save_settings(self.main_window)

    def calculate_drop_index(self, drop_pos):
        """드롭 위치를 기반으로 삽입 인덱스 계산"""
        button_positions = []
        for i in range(self.main_window.favorites_layout.count()):
            item = self.main_window.favorites_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, DraggableButton):
                    pos = widget.pos()
                    button_positions.append((i, pos.x() + pos.y() * 1000))

        # 드롭 위치와 가장 가까운 버튼 찾기
        drop_score = drop_pos.x() + drop_pos.y() * 1000

        for i, (idx, pos) in enumerate(button_positions):
            if drop_score < pos:
                return i

        return len(self.main_window.favorites)

    def toggle_favorites_section(self):
        """즐겨찾기 섹션 접기/펼치기"""
        self.main_window.favorites_collapsed = not self.main_window.favorites_collapsed

        # 버튼 아이콘 변경
        self.main_window.favorites_toggle_button.setText(
            "▶" if self.main_window.favorites_collapsed else "▼"
        )

        # 컨테이너 보이기/숨기기
        self.main_window.favorites_container.setVisible(
            not self.main_window.favorites_collapsed
        )

        # 설정 저장
        self.main_window.settings_manager.save_settings(self.main_window)

        # 상태 메시지
        state = "collapsed" if self.main_window.favorites_collapsed else "expanded"
        self.main_window.statusBar().showMessage(f"Favorites section {state}", 1000)

    def toggle_always_on_top(self):
        """항상 위에 표시 기능 토글"""
        self.main_window.is_always_on_top = (
            self.main_window.always_on_top_switch.isChecked()
        )

        if self.main_window.is_always_on_top:
            self.main_window.setWindowFlags(
                self.main_window.windowFlags() | Qt.WindowStaysOnTopHint
            )
        else:
            self.main_window.setWindowFlags(
                self.main_window.windowFlags() & ~Qt.WindowStaysOnTopHint
            )

        self.main_window.show()

        message = (
            "Always on top: Enabled"
            if self.main_window.is_always_on_top
            else "Always on top: Disabled"
        )
        self.main_window.statusBar().showMessage(message, 2000)

    def toggle_theme(self):
        """다크 모드와 라이트 모드 전환"""
        self.main_window.is_dark_mode = self.main_window.theme_switch.isChecked()
        self.main_window.apply_current_theme()

        theme_text = "Dark" if self.main_window.is_dark_mode else "Light"
        self.main_window.statusBar().showMessage(
            f"Switched to {theme_text} theme", 2000
        )

    def toggle_output_mode(self):
        """출력 모드 전환 처리"""
        self.main_window.latex_mode = self.main_window.latex_mode_radio.isChecked()
        self.main_window.update_recent_symbols()
        self.main_window.update_favorites_display()

        mode_text = "LaTeX" if self.main_window.latex_mode else "Regular"
        self.main_window.statusBar().showMessage(f"Switched to {mode_text} mode", 2000)

    def show_recent_context_menu(self, pos, symbol, latex, name, button):
        """최근 사용 항목 우클릭 메뉴"""
        menu = QMenu(self.main_window)
        self.main_window.style_manager.apply_menu_style(menu)

        # 즐겨찾기에 추가/제거 옵션
        if self.is_favorited(symbol):
            fav_action = menu.addAction("Remove from favorites")
            fav_action.triggered.connect(lambda: self.remove_from_favorites(symbol))
        else:
            fav_action = menu.addAction("Add to favorites")
            fav_action.triggered.connect(
                lambda: self.add_to_favorites(symbol, latex, name)
            )

        # 최근 목록에서 제거
        remove_action = menu.addAction("Remove from recent list")
        remove_action.triggered.connect(lambda: self.remove_from_recent_symbols(symbol))

        menu.exec_(button.mapToGlobal(pos))

    def show_favorite_context_menu(self, pos, symbol, latex, name, button):
        """즐겨찾기 우클릭 메뉴"""
        menu = QMenu(self.main_window)
        self.main_window.style_manager.apply_menu_style(menu)

        remove_action = menu.addAction("Remove from favorites")
        remove_action.triggered.connect(lambda: self.remove_from_favorites(symbol))

        menu.exec_(button.mapToGlobal(pos))

    def show_settings_menu(self):
        """설정 메뉴 표시"""
        menu = QMenu(self.main_window)
        
        # 보더 두께 줄이기 (기존 10px padding을 5px로, border 두께도 조정)
        theme = self.main_window.style_manager.get_current_theme()
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {theme['dark_bg']};
                color: {theme['foreground']};
                border: 0px
                padding: 5px;
                min-width: 200px;
            }}
            QMenu::item {{
                padding: 0px;
                margin: 0px;
            }}
        """)

        self.create_settings_content(menu)

        # 설정 버튼 아래쪽에 메뉴 표시 (오른쪽 정렬)
        button_pos = self.main_window.settings_button.mapToGlobal(
            QPoint(0, self.main_window.settings_button.height())
        )
        menu_width = 200
        button_width = self.main_window.settings_button.width()
        adjusted_pos = QPoint(
            button_pos.x() - menu_width + button_width, button_pos.y()
        )
        
        self.current_settings_menu = menu
        menu.exec_(adjusted_pos)

    def create_settings_content(self, menu):
        """설정 메뉴 내용 생성"""
        # Always on top 설정
        always_on_top_action = QWidgetAction(menu)
        always_on_top_container = self.create_settings_item(
            "Always on top",
            self.main_window.is_always_on_top,
            self.container_click_toggle_always_on_top,
        )
        always_on_top_action.setDefaultWidget(always_on_top_container)
        menu.addAction(always_on_top_action)

        # Dark mode 설정
        dark_mode_action = QWidgetAction(menu)
        dark_mode_container = self.create_settings_item(
            "Dark mode",
            self.main_window.is_dark_mode,
            self.container_click_toggle_theme,
        )
        dark_mode_action.setDefaultWidget(dark_mode_container)
        menu.addAction(dark_mode_action)

    def create_settings_item(self, label_text, checked_state, click_handler):
        """설정 항목 위젯 생성"""
        container = QWidget()
        container.setFixedHeight(35)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # 라벨
        label = QLabel(label_text)
        label.setFont(QFont(self.main_window.default_font_family, 10))
        label.setFixedHeight(25)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(label)

        layout.addStretch()

        # 스위치 컨테이너
        switch_container = QWidget()
        switch_layout = QHBoxLayout(switch_container)
        switch_layout.setContentsMargins(0, 0, 10, 0)
        switch_layout.setSpacing(0)

        # 토글 스위치
        toggle_switch = ToggleSwitch()
        toggle_switch.setChecked(checked_state)
        toggle_switch.setAttribute(Qt.WA_TransparentForMouseEvents)
        switch_layout.addWidget(toggle_switch)

        switch_container.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(switch_container)

        # 스위치 참조 저장
        if label_text == "Always on top":
            self.main_window.always_on_top_switch = toggle_switch
        elif label_text == "Dark mode":
            self.main_window.theme_switch = toggle_switch

        # 컨테이너 클릭 이벤트
        container.mousePressEvent = lambda event: click_handler()

        return container

    def container_click_toggle_always_on_top(self):
        """컨테이너 클릭으로 Always on top 토글"""
        self.main_window.always_on_top_switch.setChecked(
            not self.main_window.always_on_top_switch.isChecked()
        )
        self.toggle_always_on_top()
        # 메뉴 다시 열기
        QTimer.singleShot(100, self.show_settings_menu)

    def container_click_toggle_theme(self):
        """컨테이너 클릭으로 테마 토글"""
        self.main_window.theme_switch.setChecked(
            not self.main_window.theme_switch.isChecked()
        )
        if hasattr(self, 'current_settings_menu'):
            self.current_settings_menu.close()
    
        self.toggle_theme()
        QTimer.singleShot(100, self.show_settings_menu)
