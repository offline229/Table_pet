# global_click_listener.py
from PyQt5.QtCore import QObject, QEvent, Qt, QCoreApplication
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import sys

class GlobalClickListener(QObject):
    """全局鼠标点击监听器"""

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.app.installEventFilter(self)  # 安装事件过滤器

    def eventFilter(self, obj, event):
        """事件过滤器，捕获全局鼠标点击事件"""
        # 捕获所有窗口的鼠标按下事件
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            cursor_pos = QCursor.pos()  # 获取全局鼠标位置
            print(f"全局鼠标点击位置: x={cursor_pos.x()}, y={cursor_pos.y()}")
        return super().eventFilter(obj, event)

class MyApp(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("全局鼠标监听器")
        self.setGeometry(100, 100, 400, 300)

        # 启动全局鼠标监听
        self.mouse_listener = GlobalClickListener(app)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp(app)
    window.show()
    sys.exit(app.exec_())
