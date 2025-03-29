import pygame
from pets.base_pet import BasePet
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QAction, QComboBox
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QAction, QMenu, QPushButton
from PyQt5.QtCore import Qt
from pets.pet_a import PetA  # 导入PetA类

class InteractivePet(BasePet):
    def __init__(self, name, image_path):
        super().__init__(name, image_path)
        self.interactive = False

    def enable_interaction(self):
        self.interactive = True

    def disable_interaction(self):
        self.interactive = False

    def handle_event(self, event):
        if self.interactive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Example: If clicked, pet moves to mouse position
                self.x, self.y = pygame.mouse.get_pos()



class PetMenu(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("选择宠物")
        self.setFixedSize(200, 150)
        self.layout = QVBoxLayout()

        # 创建菜单项
        self.random_pet_action = QAction("随机召唤宠物", self)
        self.random_pet_action.triggered.connect(self.summon_random_pet)

        self.pet_a_action = QAction("召唤宠物 A", self)
        self.pet_a_action.triggered.connect(self.summon_pet_a)


        # 添加到菜单
        self.menu = QMenu(self)
        self.menu.addAction(self.random_pet_action)
        self.menu.addAction(self.pet_a_action)

        # 设置按钮来显示菜单
        self.show_menu_button = QPushButton("打开宠物菜单", self)
        self.show_menu_button.clicked.connect(self.show_menu)

        self.layout.addWidget(self.show_menu_button)
        self.setLayout(self.layout)

    def show_menu(self):
        """显示菜单"""
        self.menu.exec_(self.mapToGlobal(self.show_menu_button.pos()))

    def summon_random_pet(self):
        """随机召唤宠物"""
        from random import choice
        pet_class = choice([PetA])  # 随机选择一个宠物
        self.summon_pet(pet_class)

    def summon_pet_a(self):
        """召唤宠物A"""
        self.summon_pet(PetA)



    def summon_pet(self, pet_class):
        """召唤宠物并显示"""
        pet = pet_class()  # 创建宠物实例
        pet.move(100, 100)  # 设置宠物的位置
        pet.show()  # 显示宠物