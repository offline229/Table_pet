# 干脏活用

import os

def create_project_structure():
    # 项目根目录
    base_dir = "桌宠项目"

    # 资源目录和文件
    assets_dir = os.path.join(base_dir, "assets")
    pet_a_dir = os.path.join(assets_dir, "pet_a")
    pet_b_dir = os.path.join(assets_dir, "pet_b")
    
    # 桌宠资源子目录
    idle_a_dir = os.path.join(pet_a_dir, "idle")
    walking_a_dir = os.path.join(pet_a_dir, "walking")
    sound_a_dir = os.path.join(pet_a_dir, "sound")
    animation_a_dir = os.path.join(pet_a_dir, "animation")
    
    idle_b_dir = os.path.join(pet_b_dir, "idle")
    walking_b_dir = os.path.join(pet_b_dir, "walking")
    sound_b_dir = os.path.join(pet_b_dir, "sound")
    animation_b_dir = os.path.join(pet_b_dir, "animation")
    
    # 桌宠类目录
    pets_dir = os.path.join(base_dir, "pets")
    
    # 文件列表
    files = [
        os.path.join(pets_dir, "__init__.py"),
        os.path.join(pets_dir, "base_pet.py"),
        os.path.join(pets_dir, "interactive_pet.py"),
        os.path.join(pets_dir, "animated_pet.py"),
        os.path.join(pets_dir, "pet_a.py"),
        os.path.join(pets_dir, "pet_b.py"),
        os.path.join(base_dir, "main.py"),
        os.path.join(base_dir, "requirements.txt"),
        os.path.join(base_dir, "README.md"),
        os.path.join(base_dir, "setup.py"),
    ]

    # 创建目录
    dirs_to_create = [
        assets_dir, pet_a_dir, pet_b_dir, idle_a_dir, walking_a_dir,
        sound_a_dir, animation_a_dir, idle_b_dir, walking_b_dir,
        sound_b_dir, animation_b_dir, pets_dir
    ]

    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)

    # 创建空文件
    for file_path in files:
        with open(file_path, "w"):
            pass  # 只创建空文件

    print(f"项目结构已创建在 {base_dir} 目录下。")

if __name__ == "__main__":
    create_project_structure()
