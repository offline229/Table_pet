from PyQt5.QtCore import Qt, QTimer, QPoint, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget
import random
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtGui import QScreen
from pets.pet_manager import PetManager
from utils.windows_manager import window_info_list
# 由于所有的move(x,y)都是基于图片左上角为坐标，自定义一个true_move(x,y),
# 最好的是根据xy作为真正坐标，move显示出结果
# 每隔一定时间

# 维护一套true_x,true_y用于坐标计算，作为当前图片底部
# 维护一个img的长宽，根据state变化
# 每当move,则移动到true_x -宽度/2, true_y -高度的位置
# 好像不行，看来状态切换的时候都需要一个move把当前状态的x,y更新。
# 摔落的时候x,y正常使用，但判断标准是底部判断
# 摔落完状态立马切换到idle的时候也需要一个move改变

# 如何实现动态检测重力呢，每隔一段时间查询是否脚在线上，如果不在，就开始摔落？
# 摔落
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
        self.interaction_images = [self.load_image(f"idle/idle_{i}.png") for i in range(1, 3)] #互动状态，作为可拓展的状态在子类实现

        self.current_frame = 0
        self.is_walking = False

        # 显示宠物
        self.label = QLabel(self)
        self.label.setPixmap(self.idle_images[self.current_frame])

        # 维护宠物当前状态的尺寸
        self.resize(self.idle_images[0].size())
        self.pet_width = self.idle_images[0].width()
        self.pet_height = self.idle_images[0].height()

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
        path = f"{self.images_path}/{filename}"
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"❌ 加载图片失败: {path}")
        return pixmap

    def update_animation(self):
        """更新动画，根据状态播放不同的动画"""
        if self.state == "idle":
            images = self.idle_images
            self.label.resize(self.idle_images[self.current_frame].width(), self.idle_images[self.current_frame].height())
        elif self.state == "walking":
            images = self.walk_images
            self.label.resize(self.walk_images[self.current_frame].width(), self.walk_images[self.current_frame].height())
        elif self.state == "dragging":
            images = self.drag_images
            self.label.resize(self.drag_images[self.current_frame].width(), self.drag_images[self.current_frame].height())
        elif self.state == "falling":
            images = self.fall_images
            self.label.resize(self.fall_images[self.current_frame].width(), self.fall_images[self.current_frame].height())
        elif self.state == "interaction":
            images = self.interaction_images  # 互动状态，允许特殊的动画播放
            # 在子类根据size动态添加好了
        self.current_frame = (self.current_frame + 1) % len(images)
        self.label.setPixmap(images[self.current_frame])

    # 每秒触发一次，根据state调用状态切换函数
    def update_state(self):
        """更新宠物状态"""
        
        if self.state == "idle":
            # 切换到 idle 状态
            self.pet_width = self.idle_images[0].width()
            self.pet_height = self.idle_images[0].height()
            self.check_ground()
            # print(f"size:{self.pet_width},{self.pet_height}")
            self.enter_idle_state()

        elif self.state == "walking":
            # 切换到 walking 状态
            self.pet_width = self.walk_images[0].width()
            self.pet_height = self.walk_images[0].height()
            self.check_ground()
            self.enter_walking_state()
            # print(f"size:{self.pet_width},{self.pet_height}")

        elif self.state == "falling":
            # 切换到 falling 状态
            self.pet_width = self.fall_images[0].width()  # 假设有单独的 falling 图
            self.pet_height = self.fall_images[0].height()
            self.apply_gravity()
            # print(f"size:{self.pet_width},{self.pet_height}")

        elif self.state == "dragging":
            # 切换到 dragging 状态
            self.pet_width = self.drag_images[0].width()  # 假设有单独的 dragging 图
            self.pet_height = self.drag_images[0].height()
            self.enter_dragging_state()
            # print(f"size:{self.pet_width},{self.pet_height}")


    def enter_dragging_state(self):
        """进入拖拽状态"""
        # print("进入拖拽状态")
        if hasattr(self, 'walk_timer') and self.walk_timer.isActive():
            self.walk_timer.stop()  # 停止行走定时器
            # print("停止行走定时器，进入拖拽状态")

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
            # setPixmap之前要
            self.label.setPixmap(self.idle_images[self.current_frame])
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
           # print("当前状态允许触发事件")
            event = random.choice(["walk", "interaction"])  # 50% 的概率选择
            if event == "walk":
                # print("触发进入行走状态")
                self.start_walking()  # 进入行走状态
            elif event == "interaction":
                # print("触发进入互动状态")
                self.state = "interaction"  # 进入互动状态
                if hasattr(self, 'random_event_timer') and self.random_event_timer.isActive():
                    self.random_event_timer.stop()  # 停止定时器
        else:
            # 如果当前状态为 'falling' 或 'dragging'，则直接取消定时器
            if hasattr(self, 'random_event_timer') and self.random_event_timer.isActive():
                self.random_event_timer.stop()  # 停止定时器
            # print("当前状态为 'falling' 或 'dragging'，已取消触发事件")
    def start_walking(self):
        """开始行走状态"""
        self.check_ground()
        if self.state != "falling" and self.state != "dragging":  # 检查是否处于掉落或拖拽状态
            print("开始行走状态")
            self.is_walking = True
            self.state = "walking"  # 进入行走状态
            self.current_frame = 0
            print(f"check {self.y()+ self.idle_images[0].height() - self.walk_images[0].height()}")
            self.move(int(self.x()+ self.idle_images[0].width()/2 - self.walk_images[0].width()/2),int(self.y()+ self.idle_images[0].height() - self.walk_images[0].height()))
            
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
        self.check_ground()
        if self.is_walking:
            if self.walk_distance > 0:
                # 每次更新非常小的步长，按照之前确定的方向
                # 获取当前true的x,y
                # 赋值计算得到应该move的位置
                move_x = self.walk_speed * self.walk_direction  # 使用固定方向
                new_pos = self.pos() + QPoint(move_x, 0)
                self.move(new_pos)
                self.walk_distance -= abs(move_x)
                # move完之后手动更新真坐标
                # print(f"宠物在运动，当前X位置：{self.x()}")
            else:
                self.state = "idle"
                self.move(int(self.x() + self.walk_images[0].width()/2- self.idle_images[0].width()/2), int(self.y()+self.walk_images[0].height()- self.idle_images[0].height()))
                self.walk_timer.stop()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.prev_position = event.globalPos()  # 记录鼠标按下时的位置
            print(f"poi{self.prev_position}")
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()  # 记录拖拽偏移量
            event.accept()
            # print("开始拖拽宠物")

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
            # print("结束拖拽宠物")

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
            # 停止行走定时器
            if hasattr(self, 'walk_timer') and self.walk_timer.isActive():
                self.walk_timer.stop()

            self.fall_velocity += 1 
            
            new_x = self.x() + self.release_velocity.x()
            new_y = self.y() + self.fall_velocity

            # 获取屏幕和任务栏信息
            screen = QApplication.primaryScreen()
            screen_rect = screen.geometry()
            screen_bottom = screen_rect.bottom()
            taskbar_height = 72
            ground_level = screen_bottom - taskbar_height

            # === 动态生成有效地面线段 ===
            standing_lines = [(ground_level, 0, screen_rect.width(), "桌面")]  # 默认地面线段

            for window_info in window_info_list:
                title, is_valid, (left, top, right, bottom) = window_info
                if is_valid:
                    standing_lines.append((top, left, right, title))  # 包含窗口名称

            # === 判断宠物是否落在任意线段上 ===
            can_stand = False
            for line_y, line_x1, line_x2, window_name in standing_lines:
                # 判断宠物x,y是否触碰地面线
                # x在范围内且y比线低一点，那么同步y到线上
                if  (line_y +  100 )>= (new_y + self.fall_images[0].height()) >= line_y and line_x1 <= new_x + self.fall_images[0].width() <= line_x2:
                    can_stand = True
                    print(f"宠物前位置:  y={self.y()+ self.fall_images[0].height()}")
                    print(f"宠物位置:  y={new_y+ self.fall_images[0].height()}")
                    new_y = line_y - self.idle_images[0].height()

                    # 调试信息
                    print(f"✅ 命中地面线段 - 窗口名称: {window_name}")
                    print(f"地面线段: y={line_y}, x范围=({line_x1}, {line_x2})")
                    print(f"宠物位置: x={new_x}, y={new_y}, 宠物宽度={self.pet_width}, 高度={self.pet_height}")
                    break

            # 如果能站立
            if can_stand:
                self.fall_velocity = 0
                self.move(int(new_x+self.pet_width/2- self.idle_images[0].width()/2), int(new_y))
                self.gravity_timer.stop()
                self.images = self.idle_images
                self.state = "idle"
            else:
                self.move(new_x, new_y)

    def check_ground(self):
            """检查是否在有效地面上，否则启动掉落"""
            # 获取宠物当前位置
            current_x = self.x() + int(self.pet_height/2)
            current_y = self.y() + self.pet_height

            # 获取屏幕和任务栏信息
            screen = QApplication.primaryScreen()
            screen_rect = screen.geometry()
            screen_bottom = screen_rect.bottom()
            taskbar_height = 72
            ground_level = screen_bottom - taskbar_height

            # === 动态生成有效地面线段 ===
            standing_lines = [(ground_level, 0, screen_rect.width(), "桌面")]  # 默认地面线段

            for window_info in window_info_list:
                title, is_valid, (left, top, right, bottom) = window_info
                if is_valid:
                    standing_lines.append((top, left, right, title))  # 包含窗口名称

            # === 判断当前位置是否站在地面上 ===
            on_ground = False
            for line_y, line_x1, line_x2, window_name in standing_lines:
                if current_y == line_y and line_x1 <= current_x + self.pet_width <= line_x2:
                    on_ground = True
                    print(f"ground{window_name},{line_y},{current_y}")
                    break

            # 如果不在地面上，启动掉落
            if not on_ground:
                self.state = "falling"
                self.gravity_enabled = True
                self.gravity_timer.start(30)
                print("not ground")
