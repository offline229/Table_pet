import sys
from PyQt5.QtWidgets import QApplication
from pets.tray_menu import create_tray_icon  # 导入创建菜单栏的函数

if __name__ == '__main__':
    app = QApplication(sys.argv)

    tray_icon = create_tray_icon()  # 创建托盘图标

    # 确保持有 tray_icon 引用
    tray_icon.show()  # 强制显示托盘图标
    app.setQuitOnLastWindowClosed(False)  # 防止没有窗口时退出

    try:
        print("事件循环准备启动")
        ret = app.exec_()
        print(f"事件循环正常结束，返回值: {ret}")
        sys.exit(ret)
    except Exception as e:
        print(f"事件循环异常退出: {e}")

