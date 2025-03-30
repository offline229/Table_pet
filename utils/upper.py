import win32gui
import win32con
# 此方法需要维护一全局变量数组，格式如下
# 名称、有效性、
# 获取桌面大小
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

# 计算窗口上界可见性，返回可见范围和层级信息
def calculate_visibility(hwnd, top, left, right, all_windows):
    visibility_ranges = [(left, right)]  # 初始可见范围
    all_windows.sort(key=lambda w: w[2])  # 按窗口 top 坐标排序，模拟 Z 轴层级
    layer_level = 0  # 层级计数

    for other_hwnd, o_left, o_top, o_right, o_bottom in all_windows:
        if other_hwnd == hwnd or not win32gui.IsWindowVisible(other_hwnd):
            continue

        if o_top > top:  # 仅计算更高层级窗口对当前窗口的影响
            continue

        layer_level += 1  # 层级递增
        new_ranges = []
        for v_left, v_right in visibility_ranges:
            if o_right <= v_left or o_left >= v_right:
                new_ranges.append((v_left, v_right))  # 没有遮挡
            else:
                if o_left > v_left:
                    new_ranges.append((v_left, o_left))
                if o_right < v_right:
                    new_ranges.append((o_right, v_right))
        visibility_ranges = new_ranges

    return visibility_ranges, layer_level

# 枚举窗口回调，输出层级信息
def enum_windows_callback(hwnd, all_windows, desktop_bounds, max_layer_window):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        if not window_title.strip() or is_invalid_window(window_title):
            return

        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width, height = right - left, bottom - top

        if width <= 0 or height <= 0 or is_window_out_of_bounds(left, top, right, bottom, desktop_bounds):
            return

        visibility_ranges, layer_level = calculate_visibility(hwnd, top, left, right, all_windows)
        
        # 如果当前窗口的层级比最大层级大，则更新最大层级窗口
        if layer_level > max_layer_window[1]:
            max_layer_window[0] = (top, left, right)  # 更新当前窗口的 (上界, 左值, 右值)
            max_layer_window[1] = layer_level

# 获取任务栏和最大层级窗口的上界、左值、右值
def get_window_and_taskbar_bounds():
    desktop_bounds = get_desktop_bounds()
    all_windows = []
    max_layer_window = [None, -1]  # 用于保存最大层级窗口的信息 (窗口坐标, 最大层级)
    taskbar_left, taskbar_right = desktop_bounds[0], desktop_bounds[2]  # 默认任务栏填充整个桌面宽度

    def collect_windows(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            all_windows.append((hwnd, left, top, right, bottom))

    win32gui.EnumWindows(collect_windows, None)
    all_windows.sort(key=lambda w: w[2])  # 按 top 位置排序，模拟 Z 轴

    # 输出任务栏上界
    taskbar_hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    taskbar_top = None
    if taskbar_hwnd:
        _, taskbar_top, _, _ = win32gui.GetWindowRect(taskbar_hwnd)
        _, _, taskbar_right, _ = win32gui.GetWindowRect(taskbar_hwnd)
        taskbar_left = desktop_bounds[0]
        taskbar_right = taskbar_right if taskbar_right else desktop_bounds[2]

    for hwnd, _, _, _, _ in all_windows:
        enum_windows_callback(hwnd, all_windows, desktop_bounds, max_layer_window)

    # 返回任务栏和最大层级窗口的信息
    if taskbar_top is not None and max_layer_window[0] is not None:
        return [(taskbar_top, taskbar_left, taskbar_right), max_layer_window[0]]  # 返回任务栏的 (上界, 左值, 右值) 和最大层级窗口的信息

# 示例：调用函数并获取结果
result = get_window_and_taskbar_bounds()
print(result)
