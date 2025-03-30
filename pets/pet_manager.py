# pets/pet_manager.py

import random

class PetManager:
    _pets = []  # 存放所有宠物实例

    @classmethod
    def register_pet(cls, pet_instance):
        """注册宠物实例"""
        if pet_instance not in cls._pets:
            cls._pets.append(pet_instance)
        print(f"当前宠物数量: {len(cls._pets)}")

    @classmethod
    def unregister_pet(cls, pet_instance):
        """注销宠物实例"""
        if pet_instance in cls._pets:
            cls._pets.remove(pet_instance)
            pet_instance.close()
        print(f"当前宠物数量: {len(cls._pets)}")

    @classmethod
    def get_random_pet(cls):
        """获取随机宠物实例"""
        return random.choice(cls._pets) if cls._pets else None

    @classmethod
    def clear_all_pets(cls):
        """清空所有宠物实例"""
        while cls._pets:
            pet = cls._pets.pop()
            pet.close()
        print("所有宠物已销毁")

    @classmethod
    def get_all_pets(cls):
        """获取所有宠物实例"""
        return cls._pets
