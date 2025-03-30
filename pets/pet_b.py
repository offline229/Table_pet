from pets.base_pet import BasePet

class PetB(BasePet):
    def __init__(self):
        super().__init__(images_path="assets/pet_b")
        print("宠物B初始化完成")
        
        # 开启重力
        self.enable_gravity()
        
    # 如果将来需要给 PetB 添加特殊功能，可以在这里进行扩展
    # 例如新的行为、动画等
