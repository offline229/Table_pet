import pygame
from pets.base_pet import BasePet


class InteractivePet(BasePet):
    def __init__(self, name, image_path):
        super().__init__(name, image_path)
        self.interactive = False

    def enable_interaction(self):
        self.interactive = True

    def disable_interaction(self):
        self.interactive = False

    def handle_event(self, event):
        if self.interactive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Example: If clicked, pet moves to mouse position
                self.x, self.y = pygame.mouse.get_pos()
