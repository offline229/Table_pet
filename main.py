import sys
import threading
from PyQt5.QtWidgets import QApplication
from pets.tray_menu import create_tray_icon  # 导入创建菜单栏的函数
from utils.windows_manager import monitor_windows  # 假设 monitor_windows 代码存在这个文件

def start_monitoring():
    """在单独的线程中运行 monitor_windows"""
    monitor_windows()  # 调用 monitor_windows 函数

if __name__ == '__main__':
    app = QApplication(sys.argv)

    tray_icon = create_tray_icon()
    tray_icon.show()
    
    # 启动 monitor_windows 在独立线程中运行
    monitor_thread = threading.Thread(target=start_monitoring)
    monitor_thread.daemon = True  # 设置为守护线程，主线程退出时会自动结束此线程
    monitor_thread.start()

    app.setQuitOnLastWindowClosed(False)  # 防止没有窗口时退出

    try:
        ret = app.exec_()
        sys.exit(ret)
    except Exception as e:
        print(f"事件循环异常退出: {e}")
