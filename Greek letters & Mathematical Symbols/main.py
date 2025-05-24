# main.py
"""
애플리케이션 진입점
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from main_window import SymbolApp


def main():
    app = QApplication(sys.argv)

    # 고해상도 디스플레이 지원
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app.setStyle("Fusion")

    # 메인 윈도우 생성 및 표시
    window = SymbolApp()
    window.show()

    # 앱 종료 시 설정 저장
    app.aboutToQuit.connect(lambda: window.settings_manager.save_settings(window))

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
