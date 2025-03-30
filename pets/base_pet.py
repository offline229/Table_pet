from PyQt5.QtCore import Qt, QTimer, QPoint, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget
import random
from PyQt5.QtWidgets import QApplication 
from utils.upper import get_window_and_taskbar_bounds
from PyQt5.QtGui import QScreen
from pets.pet_manager import PetManager

class BasePet(QWidget):
    def __init__(self, images_path):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.images_path = images_path
        PetManager.register_pet(self)

        # 加载宠物图片
        self.idle_images = [self.load_image(f"idle/idle_{i}.png") for i in range(1, 3)]
        self.walk_images = [self.load_image(f"walking/walk_{i}.png") for i in range(1, 3)]
        self.drag_images = [self.load_image(f"drag/drag_{i}.png") for i in range(1, 3)]  # 拖拽状态
        self.fall_images = [self.load_image(f"fall/fall_{i}.png") for i in range(1, 3)]  # 掉落状态
        self.interaction_images = [self.load_image(f"idle/idle_{i}.png") for i in range(1, 3)]

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

    def __del__(self):
        PetManager.unregister_pet(self)

    def distance_to(self, other_pet):
        """计算两个宠物间的距离"""
        return ((self.x() - other_pet.x()) ** 2 + (self.y() - other_pet.y()) ** 2) ** 0.5

    def load_image(self, filename):
        return QPixmap(f"{self.images_path}/{filename}")

    def update_animation(self):
        """更新动画，根据状态播放不同的动画"""
        if self.state == "idle":
            images = self.idle_images
        elif self.state == "walking":
            images = self.walk_images
        elif self.state == "dragging":
            images = self.drag_images
        elif self.state == "falling":
            images = self.fall_images
        elif self.state == "interaction":
            images = self.interaction_images  # 互动状态，允许特殊的动画播放
        self.current_frame = (self.current_frame + 1) % len(images)
        self.label.setPixmap(images[self.current_frame])

    # 每秒触发一次，根据state调用状态切换函数
    # 感觉这里可能会有bug
    def update_state(self):
        """更新宠物状态"""
        if self.state == "idle":
            print("idle1")
            self.enter_idle_state()
        elif self.state == "walking":
            print("walking")
            self.enter_walking_state()
        elif self.state == "falling":
            print("falling")
            self.apply_gravity()  # 在掉落状态下应用重力
        elif self.state == "dragging":
            print("dragging")
            self.enter_dragging_state()  # 拖拽状态的处理

    def enter_dragging_state(self):
        """进入拖拽状态"""
        print("进入拖拽状态")
        if hasattr(self, 'walk_timer') and self.walk_timer.isActive():
            self.walk_timer.stop()  # 停止行走定时器
            print("停止行走定时器，进入拖拽状态")

        self.is_walking = False  # 确保取消行走状态
        self.state = "dragging"  # 进入拖拽状态
        # 根据需要更新拖拽动画或处理其他逻辑
        self.label.setPixmap(self.drag_images[0])  # 更新为拖拽动画的第一帧

    def enter_idle_state(self):
        """进入闲置状态"""
        # 掉落时无法进入闲置状态，确保只有第一次进入时才设置定时器
        if self.state != "falling" and self.state != "dragging":  # 如果不是掉落或拖拽状态
            self.is_walking = False
            self.current_frame = 0
            self.label.setPixmap(self.idle_images[self.current_frame])
            print("enter_idle_state")
            self.state = "idle"  # 设置为闲置状态
            # print("进入闲置状态")
            # 设置一个随机时间（1-5秒）后决定进入 walk 或 interaction 状态
            if not hasattr(self, 'random_event_timer') or not self.random_event_timer.isActive():
                self.random_event_timer = QTimer()
                self.random_event_timer.timeout.connect(self.trigger_random_event)
                random_timeout = random.randint(1000, 5000)  # 每1-5秒触发一次
                self.random_event_timer.start(random_timeout)

    def trigger_random_event(self):
        """触发随机事件：进入 walk 或 interaction 状态"""
        if self.state != "falling" and self.state != "dragging":
            print("当前状态允许触发事件")
            event = random.choice(["walk", "interaction"])  # 50% 的概率选择
            if event == "walk":
                print("触发进入行走状态")
                self.start_walking()  # 进入行走状态
            elif event == "interaction":
                print("触发进入互动状态")
                self.state = "interaction"  # 进入互动状态
                if hasattr(self, 'random_event_timer') and self.random_event_timer.isActive():
                    self.random_event_timer.stop()  # 停止定时器
        else:
            # 如果当前状态为 'falling' 或 'dragging'，则直接取消定时器
            if hasattr(self, 'random_event_timer') and self.random_event_timer.isActive():
                self.random_event_timer.stop()  # 停止定时器
            print("当前状态为 'falling' 或 'dragging'，已取消触发事件")

    def start_walking(self):
        """开始行走状态"""
        if self.state != "falling" and self.state != "dragging":  # 检查是否处于掉落或拖拽状态
            print("开始行走状态")
            self.is_walking = True
            self.state = "walking"  # 进入行走状态
            self.current_frame = 0
            self.label.setPixmap(self.walk_images[self.current_frame])

            # 停止定时器，防止闲置状态被反复进入
            if hasattr(self, 'random_event_timer') and self.random_event_timer.isActive():
                self.random_event_timer.stop()



            # 随机选择方向和速度（恒定速度）
            self.walk_direction = random.choice([-1, 1])  # 记录运动方向，-1表示左，1表示右
            self.walk_distance = random.randint(100, 300)  # 走的距离
            self.walk_speed = 1  # 恒定速度，减小步长以实现平滑滑动

            print(f"宠物进入行走状态，走向 {'左' if self.walk_direction == -1 else '右'}, 行走距离：{self.walk_distance}")
            # 设置行走定时器更新位置
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
                print("宠物进入闲置状态walk")

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
            self.state = "dragging"  # 进入拖拽状态

    def mouseMoveEvent(self, event):
        if self.dragging:
            if self.prev_position:
                # 计算瞬时速度，即当前位置和上次位置的差值
                delta = event.globalPos() - self.prev_position
                self.prev_position = event.globalPos()  # 更新上次位置
                # 将速度转换为较为平滑的值，例如除以一个常数来缩放
                self.release_velocity = QPoint(delta.x() , delta.y() )

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
            self.fall_velocity = self.release_velocity.y()

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
            if hasattr(self, 'walk_timer') and self.walk_timer.isActive():
                self.walk_timer.stop()  # 停止行走定时器
                print("停止行走定时器，进入拖拽状态")
            self.fall_velocity += 1  # 每次增加速度，模拟重力加速度

            # 水平速度会受到释放速度影响，垂直方向则受重力影响
            new_x = self.x() + self.release_velocity.x()  # 水平速度受 release_velocity.x() 控制
            new_y = self.y() + self.fall_velocity  # 垂直速度受重力影响

            self.move(new_x, new_y)

            # 使用 QScreen 来获取屏幕信息
            screen = QApplication.primaryScreen()
            screen_rect = screen.geometry()
            screen_bottom = screen_rect.bottom()

            taskbar_height = 40  # 任务栏的高度
            ground_level = screen_bottom - taskbar_height  # 计算宠物应落地的位置（屏幕底部 - 任务栏高度）
            pet_height = self.label.pixmap().height()
            target_bottom = ground_level - pet_height  # 宠物的底部位置

            # 如果宠物已经触及底部，则停止掉落
            if new_y >= target_bottom:
                self.fall_velocity = 0  # 停止加速
                self.move(new_x, target_bottom)  # 将宠物位置设置为地面
                self.gravity_timer.stop()  # 停止重力
                self.state = "idle"  # 切换为闲置状态
                print("宠物已落地，进入闲置状态")
            else:
                # 在掉落过程中不允许进入其他状态
                print("宠物还在掉落中，不能切换状态")

