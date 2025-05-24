# components.py
"""
재사용 가능한 커스텀 UI 컴포넌트들
"""

import json
from PyQt5.QtWidgets import QLayout, QPushButton, QWidget, QSizePolicy, QApplication
from PyQt5.QtCore import Qt, QSize, QRect, QPoint, QMimeData
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QDrag


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

    def paintEvent(self, event):
        """직접 배경 그리기"""
        super().paintEvent(event)
        
        if self.parent_app:
            is_dark_mode = getattr(self.parent_app, 'is_dark_mode', False)
            bg_color = "#3a3a2a" if is_dark_mode else "#fffacd"
            border_color = "#8b7500" if is_dark_mode else "#daa520"
            
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 배경 그리기
            painter.setBrush(QBrush(QColor(bg_color)))
            painter.setPen(QPen(QColor(border_color), 2))
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)

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
                self.parent_app.add_to_favorites(*symbol_data)
            elif source == "favorites":
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
        from constants import DARK_THEME, LIGHT_THEME

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 현재 테마 가져오기 (부모 윈도우에서)
        try:
            is_dark = self.parent().window().is_dark_mode
            THEME = DARK_THEME if is_dark else LIGHT_THEME
        except:
            THEME = LIGHT_THEME

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
