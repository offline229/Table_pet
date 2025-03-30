from pets.base_pet import BasePet
from pets.pet_manager import PetManager
from PyQt5.QtCore import QTimer
import random

class PetA(BasePet):
    def __init__(self):
        super().__init__(images_path="assets/pet_a")
        print("宠物A初始化完成")
        
        # 开启重力
        self.enable_gravity()

        # 加载互动动画
        self.a_a_images = [self.load_image(f"a_a/a_a_{i}.png") for i in range(1, 3)]  # A-A 互动
        self.a_b_images = [self.load_image(f"a_b/a_b_{i}.png") for i in range(1, 3)]  # A-B 互动

        # 定期进行距离检测
        self.check_distance_timer = QTimer()
        self.check_distance_timer.timeout.connect(self.check_distance_and_interact)
        self.check_distance_timer.start(1000)  # 每秒检测一次
        
        self.interaction_duration = 0  # 动画播放时长

        # 初始化 interaction_timer
        self.interaction_timer = QTimer()
        self.interaction_timer.timeout.connect(self.finish_interaction)  # 绑定到 finish_interaction 方法

    def check_distance_and_interact(self):
        """检测与其他宠物的距离并触发相对动画"""
        if self.state == "interaction":  # 只有在互动状态下才进行互动检测
            print("概率触发互动")
            # 80% 概率触发互动
            if random.random() < 0.8:
                for other_pet in PetManager.get_all_pets():
                    if other_pet is not self:
                        distance = self.distance_to(other_pet)
                        print(f"与 {type(other_pet).__name__} 的距离: {distance}")

                        # 根据距离触发动画
                        if distance < 100:
                            self.trigger_close_interaction(other_pet)  # 触发互动
                            break  # 触发成功后停止循环
                        else:
                            print("距离太远，无法互动")

            # 如果没有触发互动，回到闲置状态
            else:
                self.enter_idle_state()


    def trigger_close_interaction(self, other_pet):
        """根据距离触发相对动画"""
        print("找到一个互动对象")
        if isinstance(other_pet, PetA):  # 如果是同类PetA
            print("两只 PetA 相遇，触发 A-A 互动动画！")
            self.enter_interaction_state("a_a")
            other_pet.enter_interaction_state("a_a")  # 被互动的宠物也进入 A-A 互动状态
        elif isinstance(other_pet, BasePet):  # 和其他宠物（例如 PetB）互动
            print("PetA 与其他宠物相遇，触发 A-B 互动动画")
            self.enter_interaction_state("a_b")

    def enter_interaction_state(self, interaction_type):
        """进入互动状态"""
        if self.state not in ["falling", "dragging"]:  # 避免在掉落或拖拽时改变状态
            if interaction_type == "a_a":
                self.interaction_images = self.a_a_images  # 使用 A-A 互动动画
            elif interaction_type == "a_b":
                self.interaction_images = self.a_b_images  # 使用 A-B 互动动画

            self.current_frame = 0
            self.is_walking = False  # 禁用行走，防止频闪
            self.state = "interaction"  # 设置为互动状态
            print(f"播放 {interaction_type} 动画")

            # 设置动画时长：随机 3-5 秒
            self.interaction_duration = random.randint(3000, 5000)
            self.interaction_timer.start(10)  # 每10毫秒检查一次动画播放时长

    def finish_interaction(self):
        """完成互动动画，回到闲置状态"""
        self.interaction_duration -= 10  # 每次检查减少 10 毫秒
        if self.interaction_duration <= 0:
            self.interaction_timer.stop()  # 停止动画定时器

            self.enter_idle_state()  # 回到闲置状态