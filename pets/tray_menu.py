import sys
import random
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from pets.pet_a import PetA  # 导入PetA类
from pets.pet_b import PetB  # 导入PetB类
from pets.pet_manager import PetManager  # 全局宠物管理器
from PyQt5.QtCore import QTimer, QPoint


import sys
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QCheckBox, QDialog, QVBoxLayout, QDialogButtonBox, QLabel
from pets.pet_a import PetA
from pets.pet_b import PetB
from pets.pet_manager import PetManager
from utils.upper import window_info_list, update_window_validity


app = QApplication(sys.argv)

# 所有宠物类型
pet_types = [PetA, PetB]

def summon_pet_a():
    """召唤2只PetA"""
    for i in range(2):  
        pet_a = PetA()
        pet_a.move(QPoint(100 + i * 150, 100 + i * 50))
        pet_a.show()
        PetManager.register_pet(pet_a)  # 注册宠物实例

def summon_pet_b():
    """召唤2只PetB"""
    for i in range(2):  
        pet_b = PetB()
        pet_b.move(QPoint(100 + i * 150, 100 + i * 50))
        pet_b.show()
        PetManager.register_pet(pet_b)  # 注册宠物实例

def random_summon():
    """随机召唤宠物"""
    pet_class = random.choice(pet_types)  # 从宠物类型列表中随机选择
    if pet_class == PetA:
        summon_pet_a()
    elif pet_class == PetB:
        summon_pet_b()

def destroy_random_pet():
    """随机销毁一只宠物"""
    pet_to_destroy = PetManager.get_random_pet()
    if pet_to_destroy:
        PetManager.unregister_pet(pet_to_destroy)
        pet_to_destroy.close()

def destroy_all_pets():
    """销毁所有宠物"""
    PetManager.clear_all_pets()

def exit_program():
    """退出程序"""
    destroy_all_pets()
    QApplication.quit()

def rain():
    """随机召唤10到20只宠物，并在几秒后全部销毁"""
    num_pets = random.randint(10, 20)  # 随机生成的宠物数量
    
    def summon_pet(i):
        """逐个召唤宠物"""
        if i >= num_pets:
            return  # 所有宠物已生成，退出递归

        pet_class = random.choice(pet_types)  # 随机选择宠物类型
        pet = pet_class()  # 创建宠物实例
        # 随机生成较高的位置（屏幕上方位置）
        x = random.randint(0, QApplication.primaryScreen().geometry().width() - 100)
        y = random.randint(0, 800)  # 随机高的位置（确保宠物在屏幕上方）
        pet.move(QPoint(x, y))
        pet.show()
        PetManager.register_pet(pet)  # 注册宠物实例

        # 设置延时，逐个显示宠物
        delay = random.randint(200, 500)  # 每只宠物之间的延迟
        QTimer.singleShot(delay, lambda i=i: summon_pet(i + 1))  # 递归调用下一个宠物的显示

    # 开始召唤第一只宠物
    summon_pet(0)

    # 延时几秒后销毁所有宠物
    # QTimer.singleShot(random.randint(3000, 5000), destroy_all_pets)


def create_window_selection_dialog():
    """创建窗口选择的对话框，用户可以勾选或取消勾选窗口"""
    dialog = QDialog()
    dialog.setWindowTitle("选择窗口范围")

    layout = QVBoxLayout()
    label = QLabel("请选择需要激活的窗口：")
    layout.addWidget(label)

    checkboxes = []
    for idx, (window_title, is_valid, _) in enumerate(window_info_list):
        checkbox = QCheckBox(window_title)
        checkbox.setChecked(is_valid == 1)  # 根据有效性设置勾选框状态

        # 使用 `lambda` 时确保传递正确的 `idx`
        checkbox.stateChanged.connect(lambda state, i=idx: on_checkbox_state_changed(state, i))

        layout.addWidget(checkbox)
        checkboxes.append(checkbox)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    dialog.setLayout(layout)
    return dialog


def on_checkbox_state_changed(state, index):
    """处理勾选框状态变化时的有效性更新"""
    # state: 0 (unchecked), 2 (checked)
    new_validity = 1 if state == 2 else 0
    update_window_validity(index, new_validity)


def window_interaction():
    """触发互动范围功能，显示所有窗口列表供用户选择"""
    dialog = create_window_selection_dialog()
    
    # 确保在对话框关闭后能正确处理事件
    result = dialog.exec_()  # 确保这是阻塞调用，直到用户做出选择
    print(f"对话框返回结果: {result}")  # 输出返回结果
    if result == QDialog.Accepted:
        print("对话框确认选择")
    else:
        print("对话框取消选择")
    
    # 这里可以处理其他后续操作，如关闭对话框后的清理工作


def create_tray_icon():
    """创建托盘图标和菜单"""
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon('assets/icon.png'))
    tray_icon.setVisible(True)

    menu = QMenu()

    # 宠物召唤菜单
    summon_action = menu.addMenu('召唤宠物')
    summon_random_action = summon_action.addAction('随机召唤')
    summon_random_action.triggered.connect(random_summon)

    summon_a_action = summon_action.addAction('召唤A')
    summon_a_action.triggered.connect(summon_pet_a)

    summon_b_action = summon_action.addAction('召唤B')
    summon_b_action.triggered.connect(summon_pet_b)

    # 宠物销毁菜单
    destroy_action = menu.addMenu('销毁宠物')
    destroy_random_action = destroy_action.addAction('随机销毁一只')
    destroy_random_action.triggered.connect(destroy_random_pet)

    destroy_all_action = destroy_action.addAction('销毁所有')
    destroy_all_action.triggered.connect(destroy_all_pets)

    # 更多功能菜单
    more_action = menu.addMenu('更多功能')
    
    ai_action = more_action.addAction('AI功能')
    ai_action.triggered.connect(lambda: print("AI功能被启用！"))
    
    window_interaction_action = more_action.addAction('互动范围')
    window_interaction_action.triggered.connect(window_interaction)


    rain_action = more_action.addAction('下灰狗雨')
    rain_action.triggered.connect(rain)

    # 退出程序菜单
    exit_action = menu.addAction('退出程序')
    exit_action.triggered.connect(exit_program)

    tray_icon.setContextMenu(menu)

    return tray_icon

# 创建并显示系统托盘图标
tray_icon = create_tray_icon()
sys.exit(app.exec_())
