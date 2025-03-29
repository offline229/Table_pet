from PyQt5.QtCore import Qt, QTimer, QPoint, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget
import random
from PyQt5.QtWidgets import QApplication 

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
        self.animation_timer.start(100)  # 加速更新动画频率（100毫秒）

        # 随机状态切换定时器
        self.state_timer = QTimer()
        self.state_timer.timeout.connect(self.update_state)
        self.state_timer.start(1000)

        # 重力相关
        self.gravity_enabled = False
        self.gravity_timer = QTimer()
        self.gravity_timer.timeout.connect(self.apply_gravity)

        # 初始化自由落体速度
        self.fall_velocity = 0

        # 初始化拖拽状态
        self.dragging = False
        self.drag_position = None
        self.prev_position = None
        self.release_velocity = QPoint(0, 0)  # 释放时的速度

        # 当前状态
        self.state = "falling"  # "idle", "walking", "falling", "dragging"

        print("宠物初始化完成")

    def load_image(self, filename):
        return QPixmap(f"{self.images_path}/{filename}")

    def update_animation(self):
        images = self.walk_images if self.is_walking else self.idle_images
        self.current_frame = (self.current_frame + 1) % len(images)
        self.label.setPixmap(images[self.current_frame])

    def update_state(self):
        """更新宠物状态"""
        if self.state == "idle":
            self.enter_idle_state()
        elif self.state == "walking":
            self.enter_walking_state()
        elif self.state == "falling":
            self.apply_gravity()  # 在掉落状态下应用重力

    def enter_idle_state(self):
        """进入闲置状态"""
        if self.state != "falling":  # 如果不是掉落状态
            self.is_walking = False
            self.current_frame = 0
            self.label.setPixmap(self.idle_images[self.current_frame])
            self.state = "walking"  # 随机切换到运动状态
            # print("宠物进入闲置状态")

            # 设置一个随机时间（1-5秒）后进入行走状态
            self.walk_timer = QTimer()
            self.walk_timer.timeout.connect(self.start_walking)
            self.walk_timer.start(random.randint(1000, 5000))

    def start_walking(self):
        """开始行走状态"""
        self.is_walking = True
        self.state = "walking"
        self.walk_timer.stop()  # 停止定时器

        # 随机选择方向和速度（恒定速度）
        self.walk_direction = random.choice([-1, 1])  # 记录运动方向，-1表示左，1表示右
        self.walk_distance = random.randint(100, 300)  # 走的距离
        self.walk_speed = 1  # 恒定速度，减小步长以实现平滑滑动

        # print(f"宠物进入行走状态，走向 {'左' if self.walk_direction == -1 else '右'}, 行走距离：{self.walk_distance}")

        # 使用高频率定时器来使位移看起来像在滑动
        self.walk_timer = QTimer()
        self.walk_timer.timeout.connect(self.enter_walking_state)
        self.walk_timer.start(10)  # 每10毫秒更新一次

    def enter_walking_state(self):
        """进入运动状态"""
        if self.is_walking:
            if self.walk_distance > 0:
                # 每次更新非常小的步长，按照之前确定的方向
                move_x = self.walk_speed * self.walk_direction  # 使用固定方向
                new_pos = self.pos() + QPoint(move_x, 0)
                self.move(new_pos)
                self.walk_distance -= abs(move_x)
                # print(f"宠物在运动，当前X位置：{self.x()}")
            else:
                self.state = "idle"
                self.walk_timer.stop()  # 停止定时器
                # print("宠物进入闲置状态")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.prev_position = event.globalPos()  # 记录鼠标按下时的位置
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()  # 记录拖拽偏移量
            event.accept()
            print("开始拖拽宠物")

            # 如果重力已开启，停止重力
            if self.gravity_enabled:
                self.gravity_timer.stop()

    def mouseMoveEvent(self, event):
        if self.dragging:
            if self.prev_position:
                # 计算瞬时速度，即当前位置和上次位置的差值
                delta = event.globalPos() - self.prev_position
                self.prev_position = event.globalPos()  # 更新上次位置
                # 将速度转换为较为平滑的值，例如除以一个常数来缩放
                self.release_velocity = QPoint(delta.x() // 10, delta.y() // 10)

            # 确保拖拽偏移量（self.drag_position）不为空
            if self.drag_position:
                self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            print("结束拖拽宠物")

            # 在鼠标释放时直接使用计算的瞬时速度
            print(f"拖拽释放时的瞬时速度：{self.release_velocity}")

            # 松手后开启重力并带有初始速度
            if self.gravity_enabled:
                self.state = "falling"  # 设置为掉落状态
                self.gravity_timer.start(30)  # 开启重力定时器

    def enable_gravity(self):
        """开启重力效果"""
        self.gravity_enabled = True
        self.gravity_timer.start(30)  # 每30毫秒进行一次重力检测
        print("重力效果已启用")

    def apply_gravity(self):
        """自由落体状态下的物理应用"""
        if self.state == "falling":
            self.fall_velocity += 1  # 每次增加速度，模拟重力加速度

            # 水平速度会受到释放速度影响，垂直方向则受重力影响
            new_x = self.x() + self.release_velocity.x()  # 水平速度受 release_velocity.x() 控制
            new_y = self.y() + self.fall_velocity  # 垂直速度受重力影响

            self.move(new_x, new_y)

            # 获取屏幕上的所有窗口
            desktop = QDesktopWidget()
            screen_rect = desktop.screenGeometry()
            screen_bottom = screen_rect.bottom()
            taskbar_height = 40
            ground_level = screen_bottom - taskbar_height
            pet_height = self.label.pixmap().height()
            target_bottom = ground_level - pet_height

            # 获取屏幕上的所有窗口
            all_windows = [w for w in QApplication.topLevelWidgets() if isinstance(w, QWidget)]

            # 设定一个标志，表示宠物是否接触到任何窗口的顶部
            is_contact_with_surface = False

            for window in all_windows:
                # 判断宠物与窗口顶部的距离
                window_rect = window.geometry()
                window_top = window_rect.top()
                window_bottom = window_rect.bottom()

                # 判断宠物是否接触到窗口顶部或最底部
                if new_y + pet_height >= window_top and new_y + pet_height <= window_bottom:
                    self.fall_velocity = 0
                    self.move(new_x, window_top - pet_height)  # 将宠物放置在窗口的顶部位置
                    self.gravity_timer.stop()  # 停止重力
                    self.state = "idle"  # 切换回闲置状态
                    print("宠物进入闲置状态")
                    is_contact_with_surface = True
                    break

            # 如果没有接触到任何窗口的顶部，宠物继续下落
            if not is_contact_with_surface:
                if self.y() >= target_bottom:  # 如果已经触底
                    self.fall_velocity = 0
                    self.move(self.x(), target_bottom)  # 将宠物放置在地面上
                    self.gravity_timer.stop()  # 停止重力
                    self.state = "idle"  # 切换回闲置状态
                    print("宠物已落地，进入闲置状态")

