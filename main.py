import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

class PetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 加载宠物图片
        self.pet_images = [QPixmap(f"assets/pet_a/idle/idle_{i}.png") for i in range(1, 3)]
        self.current_frame = 0

        # 设置标签显示宠物
        self.label = QLabel(self)
        self.label.setPixmap(self.pet_images[self.current_frame])
        self.resize(self.pet_images[0].size())

        # 定时器实现动画
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(500)

        # 拖动相关
        self.dragging = False
        self.drag_position = None

    def update_animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.pet_images)
        self.label.setPixmap(self.pet_images[self.current_frame])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = PetWidget()
    pet.show()
    sys.exit(app.exec_())
