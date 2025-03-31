import win32gui
import win32con
import random

# 全局变量，存储窗口信息
window_info_list = []

# 获取桌面边界
def get_desktop_bounds():
    desktop_hwnd = win32gui.GetDesktopWindow()
    left, top, right, bottom = win32gui.GetWindowRect(desktop_hwnd)
    return left, top, right, bottom

# 判断窗口是否完全在桌面之外
def is_window_out_of_bounds(left, top, right, bottom, desktop_bounds):
    d_left, d_top, d_right, d_bottom = desktop_bounds
    return right <= d_left or left >= d_right or bottom <= d_top or top >= d_bottom

# 判断窗口是否无效（过滤设置、Windows 输入体验、Program Manager）
def is_invalid_window(window_title):
    invalid_titles = ["设置", "Windows 输入体验", "Program Manager"]
    return any(title in window_title for title in invalid_titles)

# 添加窗口信息
def add_window_info(window_title, is_valid, left, top, right, bottom):
    # 将窗口名称、有效性标志和坐标信息添加到全局变量数组中
    window_info_list.append([window_title, is_valid, (left, top, right, bottom)])

# 更新窗口有效性
def update_window_validity(index, validity):
    window_info_list[index][1] = validity  # 更新有效性（0 或 1）
    print_window_info()

# 打印所有窗口信息
def print_window_info():
    for window_info in window_info_list:
        print(f"名称: {window_info[0]}, 有效性: {window_info[1]}, 坐标: {window_info[2]}")

# 枚举窗口回调，输出窗口信息
def enum_windows_callback(hwnd, all_windows, desktop_bounds):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        if not window_title.strip() or is_invalid_window(window_title):
            return

        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width, height = right - left, bottom - top

        if width <= 0 or height <= 0 or is_window_out_of_bounds(left, top, right, bottom, desktop_bounds):
            return

        is_valid = 1  # 假设窗口有效，您可以在此进行其他有效性检查
        add_window_info(window_title, is_valid, left, top, right, bottom)

# 获取所有窗口的信息并打印
def get_all_windows_info():
    desktop_bounds = get_desktop_bounds()
    all_windows = []
    
    def collect_windows(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            all_windows.append((hwnd, left, top, right, bottom))
    
    win32gui.EnumWindows(collect_windows, None)
    
    for hwnd, _, _, _, _ in all_windows:
        enum_windows_callback(hwnd, all_windows, desktop_bounds)

    # 打印所有窗口信息
    print_window_info()

# 调用并打印窗口信息
get_all_windows_info()
