# pets/pet_a.py

from PyQt5.QtGui import QPixmap

class PetA:
    def __init__(self):
        self.state = 'idle'  # 初始状态为闲置
        self.idle_images = ['assets/pet_a/idle/idle_1.png', 'assets/pet_a/idle/idle_2.png']
        self.walking_images = ['assets/pet_a/walking/walk_1.png', 'assets/pet_a/walking/walk_2.png']
        self.current_image_index = 0

    def get_image(self):
        """ 获取宠物当前状态的图像 """
        if self.state == 'idle':
            return self.idle_images[self.current_image_index]
        elif self.state == 'walking':
            return self.walking_images[self.current_image_index]

    def walk(self):
        """ 宠物走动 """
        self.state = 'walking'
        self.current_image_index = (self.current_image_index + 1) % len(self.walking_images)

    def idle(self):
        """ 宠物闲置 """
        self.state = 'idle'
        self.current_image_index = (self.current_image_index + 1) % len(self.idle_images)
