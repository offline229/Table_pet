import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from pets.pet_a import PetA  # 导入PetA类
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication
from pets.pet_a import PetA  # 导入PetA类

pets = []  # 用于存储多个宠物实例

def summon_pet_a():
    for i in range(3):  # 创建3个PetA实例
        pet_a = PetA()  # 创建一个PetA实例
        pet_a.move(QPoint(100 + i * 150, 100 + i * 50))  # 给每个实例设置不同的位置
        pet_a.show()  # 显示宠物实例
        pets.append(pet_a)  # 将每个实例添加到列表中



def random_summon():
    import random
    # 随机选择召唤PetA或PetB
    if random.choice([True, False]):
        summon_pet_a()


def exit_program():
    QApplication.quit()

def create_tray_icon():
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon('assets/icon.png'))  # 设置任务栏图标
    tray_icon.setVisible(True)

    # 创建右键菜单
    menu = QMenu()

    # 添加菜单项
    summon_action = menu.addMenu('召唤宠物')  # 子菜单：召唤宠物
    summon_random_action = summon_action.addAction('随机召唤')
    summon_random_action.triggered.connect(random_summon)

    summon_a_action = summon_action.addAction('召唤A')
    summon_a_action.triggered.connect(summon_pet_a)


    exit_action = menu.addAction('退出程序')
    exit_action.triggered.connect(exit_program)

    # 设置任务栏右键点击时显示菜单
    tray_icon.setContextMenu(menu)

    return tray_icon
