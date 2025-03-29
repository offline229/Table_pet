# 桌宠项目：基础功能实现
# 文件：main.py
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from pets.pet_a import PetA

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = PetA()
    pet.show()
    sys.exit(app.exec_())
