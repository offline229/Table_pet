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
