from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget
import random

class BasePet(QWidget):
    def __init__(self, images_path):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.images_path = images_path

        # 加载宠物图片
        self.idle_images = [self.load_image(f"idle/idle_{i}.png") for i in range(1, 3)]
        self.walk_images = [self.load_image(f"walking/walk_{i}.png") for i in range(1, 3)]
        self.current_frame = 0
        self.is_walking = False

        # 显示宠物
        self.label = QLabel(self)
        self.label.setPixmap(self.idle_images[self.current_frame])
        self.resize(self.idle_images[0].size())

        # 动画定时器
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(500)

        # 自由行走定时器
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.random_move)
        self.move_timer.start(2000)

        # 拖动相关
        self.dragging = False
        self.drag_position = None

        # 重力相关
        self.gravity_enabled = False
        self.gravity_timer = QTimer()
        self.gravity_timer.timeout.connect(self.apply_gravity)

        print("宠物初始化完成")

    def load_image(self, filename):
        return QPixmap(f"{self.images_path}/{filename}")

    def update_animation(self):
        images = self.walk_images if self.is_walking else self.idle_images
        self.current_frame = (self.current_frame + 1) % len(images)
        self.label.setPixmap(images[self.current_frame])

    def random_move(self):
        if random.random() < 0.5:
            self.is_walking = True
            move_x = random.randint(-50, 50)
            move_y = random.randint(-50, 50)
            new_pos = self.pos() + QPoint(move_x, move_y)
            self.move(new_pos)
            print(f"宠物随机移动到新位置: {new_pos}")
        else:
            self.is_walking = False
            print("宠物停止移动")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            print("开始拖拽宠物")

            # 如果重力已开启，停止重力
            if self.gravity_enabled:
                self.gravity_timer.stop()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            print("结束拖拽宠物")

            # 松手后开启重力
            if self.gravity_enabled:
                self.gravity_timer.start(30)

    def enable_gravity(self):
        """开启重力效果"""
        self.gravity_enabled = True
        self.gravity_timer.start(30)  # 每30毫秒进行一次重力检测
        print("重力效果已启用")

    def apply_gravity(self):
        """重力效果实现"""
        # 获取屏幕的底部位置
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry()  # 获取当前屏幕的大小和位置
        screen_bottom = screen_rect.bottom()  # 屏幕的底部位置
        taskbar_height = 40  # 假设工具栏高度为40px，需根据实际情况调整

        ground_level = screen_bottom - taskbar_height  # 计算工具栏顶部的高度

        # 检查宠物是否到达了"桌面"的底部（工具栏的顶部）
        if self.y() < ground_level:
            print("重力作用中...")
            self.move(self.x(), min(self.y() + 10, ground_level))  # 每次向下移动10px
        else:
            print("已落地")
            self.gravity_timer.stop()  # 落地后停止重力

