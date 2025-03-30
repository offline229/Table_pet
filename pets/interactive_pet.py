import pygame
from pets.base_pet import BasePet
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QAction, QComboBox
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QAction, QMenu, QPushButton
from PyQt5.QtCore import Qt
from pets.pet_a import PetA  # 导入PetA类
from pets.pet_b import PetB  # 导入PetA类
from pets.pet_manager import PetManager

class InteractivePet:
    def handle_interactions(self, pet_instance):
        nearby_pets = PetManager.get_nearby_pets(pet_instance)

        for other_pet in nearby_pets:
            if isinstance(pet_instance, PetA) and isinstance(other_pet, PetA):
                pet_instance.a_a_interaction(other_pet)
            elif isinstance(pet_instance, PetA) and isinstance(other_pet, PetB):
                pet_instance.a_b_interaction(other_pet)
            elif isinstance(pet_instance, PetB) and isinstance(other_pet, PetA):
                other_pet.a_b_interaction(pet_instance)