import sys
import random
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from pets.pet_a import PetA  # 导入PetA类
from pets.pet_b import PetB  # 导入PetB类
from pets.pet_manager import PetManager  # 全局宠物管理器

app = QApplication(sys.argv)

# 所有宠物类型
pet_types = [PetA, PetB]

def summon_pet_a():
    """召唤2只PetA"""
    for i in range(2):  
        pet_a = PetA()
        pet_a.move(QPoint(100 + i * 150, 100 + i * 50))
        pet_a.show()
        PetManager.register_pet(pet_a)  # 注册宠物实例

def summon_pet_b():
    """召唤2只PetB"""
    for i in range(2):  
        pet_b = PetB()
        pet_b.move(QPoint(100 + i * 150, 100 + i * 50))
        pet_b.show()
        PetManager.register_pet(pet_b)  # 注册宠物实例

def random_summon():
    """随机召唤宠物"""
    pet_class = random.choice(pet_types)  # 从宠物类型列表中随机选择
    if pet_class == PetA:
        summon_pet_a()
    elif pet_class == PetB:
        summon_pet_b()

def destroy_random_pet():
    """随机销毁一只宠物"""
    pet_to_destroy = PetManager.get_random_pet()
    if pet_to_destroy:
        PetManager.unregister_pet(pet_to_destroy)
        pet_to_destroy.close()

def destroy_all_pets():
    """销毁所有宠物"""
    PetManager.clear_all_pets()

def exit_program():
    """退出程序"""
    destroy_all_pets()
    QApplication.quit()

def window_interaction():
    """触发窗口互动功能"""
    print("窗口互动功能被触发！")

def create_tray_icon():
    """创建托盘图标和菜单"""
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon('assets/icon.png'))
    tray_icon.setVisible(True)

    menu = QMenu()

    # 宠物召唤菜单
    summon_action = menu.addMenu('召唤宠物')
    summon_random_action = summon_action.addAction('随机召唤')
    summon_random_action.triggered.connect(random_summon)

    summon_a_action = summon_action.addAction('召唤A')
    summon_a_action.triggered.connect(summon_pet_a)

    summon_b_action = summon_action.addAction('召唤B')
    summon_b_action.triggered.connect(summon_pet_b)

    # 宠物销毁菜单
    destroy_action = menu.addMenu('销毁宠物')
    destroy_random_action = destroy_action.addAction('随机销毁一只')
    destroy_random_action.triggered.connect(destroy_random_pet)

    destroy_all_action = destroy_action.addAction('销毁所有')
    destroy_all_action.triggered.connect(destroy_all_pets)

    # 更多功能菜单
    more_action = menu.addMenu('更多功能')
    
    ai_action = more_action.addAction('AI功能')
    ai_action.triggered.connect(lambda: print("AI功能被启用！"))
    
    window_interaction_action = more_action.addAction('窗口互动功能')
    window_interaction_action.triggered.connect(window_interaction)

    # 退出程序菜单
    exit_action = menu.addAction('退出程序')
    exit_action.triggered.connect(exit_program)

    tray_icon.setContextMenu(menu)

    return tray_icon

# 创建并显示系统托盘图标
tray_icon = create_tray_icon()
sys.exit(app.exec_())
