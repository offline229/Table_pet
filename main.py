import sys
from PyQt5.QtWidgets import QApplication
from pets.tray_menu import create_tray_icon  # 导入创建菜单栏的函数

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建系统托盘图标并启动菜单
    tray_icon = create_tray_icon()

    # 启动应用
    sys.exit(app.exec_())
