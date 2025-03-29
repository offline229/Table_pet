# pets/base_pet.py

import pygame
import os

class BasePet:
    def __init__(self, name, image_folder):
        self.name = name
        self.image_folder = image_folder
        self.images = {}  # 存储动作图像
        self.current_action = 'idle'  # 默认动作是闲置
        self.x = 100  # 宠物初始x位置
        self.y = 100  # 宠物初始y位置
        self.load_images()
    
    def load_images(self):
        """ 加载宠物的所有动作图像 """
        for action in ['idle', 'walking']:  # 支持的动作：闲置和行走
            action_path = os.path.join(self.image_folder, action)
            if os.path.exists(action_path):
                self.images[action] = [pygame.image.load(os.path.join(action_path, img))
                                       for img in os.listdir(action_path) if img.endswith('.png')]
    
    def change_action(self, action):
        """ 更改当前动作 """
        if action in self.images:
            self.current_action = action
    
    def display(self, screen):
        """ 显示当前动作的图像 """
        if self.current_action in self.images:
            image = self.images[self.current_action][0]  # 假设只显示第一个图像
            screen.blit(image, (self.x, self.y))  # 将图像显示到指定位置
    
    def move(self, dx, dy):
        """ 移动宠物 """
        self.x += dx
        self.y += dy
