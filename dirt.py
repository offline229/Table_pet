import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication
from pets.pet_a import PetA  # 导入PetA类

if __name__ == '__main__':
    app = QApplication(sys.argv)

    pets = []  # 用于存储多个PetA实例

    # 创建多个PetA实例
    for i in range(3):  # 创建3个PetA实例
        pet_a = PetA()  # 创建一个PetA实例
        pet_a.move(QPoint(100 + i * 150, 100 + i * 50))  # 给每个实例设置不同的位置
        pet_a.show()  # 显示宠物实例
        pets.append(pet_a)  # 将每个实例添加到列表中

    sys.exit(app.exec_())


import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QDialog, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from pets.pet_a import PetA  # 导入PetA类
from pets.interactive_pet import PetMenu  # 导入自定义的PetMenu类

class TrayApp:
    def __init__(self):
        # 初始化任务栏图标
        self.app = QApplication(sys.argv)

        # 创建任务栏图标
        self.tray_icon = QSystemTrayIcon(QIcon("assets/icon.png"), self.app)  # 设置任务栏图标
        self.tray_icon.setVisible(True)

        # 创建任务栏右键菜单
        tray_menu = QMenu()

        # 创建菜单项
        summon_pet_action = QAction("召唤宠物", self.app)
        summon_pet_action.triggered.connect(self.show_pet_menu)
        tray_menu.addAction(summon_pet_action)

        # 退出程序
        quit_action = QAction("退出", self.app)
        quit_action.triggered.connect(self.app.quit)
        tray_menu.addAction(quit_action)

        # 设置任务栏菜单
        self.tray_icon.setContextMenu(tray_menu)

        # 创建并显示两只宠物作为测试
        self.create_and_show_test_pets()

    def show_pet_menu(self):
        """显示宠物菜单"""
        self.pet_menu = PetMenu()
        self.pet_menu.exec_()

    def create_and_show_test_pets(self):
        """创建并显示两只宠物作为测试"""
        pet_1 = PetA()  # 创建第一只宠物
        pet_1.move(QPoint(100, 100))  # 设置宠物的位置
        pet_1.show()  # 显示宠物

        pet_2 = PetA()  # 创建第二只宠物
        pet_2.move(QPoint(300, 100))  # 设置第二只宠物的位置
        pet_2.show()  # 显示宠物

    def run(self):
        self.app.exec_()

if __name__ == "__main__":
    tray_app = TrayApp()
    tray_app.run()
