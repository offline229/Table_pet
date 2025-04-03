import win32gui
import win32con
import time

# 动态维护的全局变量数组，包含信息：名称、有效性、上下左右坐标
# window_info_list = [idx][ [window_title, is_valid, (left, top, right, bottom)]]
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
    # 窗口名称、有效性标志和坐标信息添加到全局变量数组中
    window_info_list.append([window_title, is_valid, (left, top, right, bottom)])

# 更新窗口有效性（根据不同参数情况）
def update_window_validity(*args):
    if len(args) == 2:
        # 只传递了 index 和 new_validity，更新有效性
        index, new_validity = args
        if 0 <= index < len(window_info_list):
            window_info = window_info_list[index]
            if window_info[1] != new_validity:  # 仅在有效性变化时更新
                window_info[1] = new_validity  # 更新有效性
                print(f"更新窗口有效性：名称: {window_info[0]}, 有效性: {new_validity}, 坐标: {window_info[2]}")
        else:
            print(f"索引 {index} 超出窗口信息列表范围")
    
    elif len(args) == 6:
        # 如果传递了完整的窗口信息（标题和坐标），更新有效性和坐标
        window_title, validity, left, top, right, bottom = args
        for window_info in window_info_list:
            if window_info[0] == window_title:
                # 仅在有效性或坐标变化时才更新
                if window_info[1] != validity or window_info[2] != (left, top, right, bottom):
                    window_info[1] = validity  # 更新有效性
                    window_info[2] = (left, top, right, bottom)  # 更新坐标
                    print(f"更新窗口：名称: {window_info[0]}, 有效性: {validity}, 坐标: {window_info[2]}")
                break
        else:
            # 如果没有找到窗口，添加新窗口
            add_window_info(window_title, validity, left, top, right, bottom)
            print(f"添加新窗口：名称: {window_title}, 有效性: {validity}, 坐标: {(left, top, right, bottom)}")




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
        
        # 查找窗口是否已存在
        existing_window = next((w for w in window_info_list if w[0] == window_title), None)

        if existing_window:
            # 已存在窗口，仅更新坐标，不修改有效性
            existing_window[2] = (left, top, right, bottom)
        else:
            # 新窗口，初始化有效性
            is_valid = 0  # 假设窗口无效
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

# 每500ms动态更新窗口信息
def monitor_windows():
    while True:
        get_all_windows_info()
        time.sleep(0.5)  # 每隔500ms更新一次窗口信息

