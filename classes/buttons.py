import pygame
from pyexpat.errors import messages

# Здоровье
# Защитник ближнего боя
# Защитник дальнего боя
BUTTON_SIZE = 50
FONT_SIZE = 32
HEALTH_BUTTON_COST = 200
KNIGHT_BUTTON_COST = 300
ARCHER_BUTTON_COST = 400

class AbstrtactButton(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image_path:str, event: int, cost: int, text: str):
        super().__init__()
        self.__x = x
        self.__y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (BUTTON_SIZE, BUTTON_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__event = event
        self.__cost = cost
        self.__font = pygame.font.Font(None, FONT_SIZE)
        self.__text = text

    def click(self):
        event = pygame.event.Event(self.__event, message=str(self.__cost))
        pygame.event.post(event)

    def get_cost(self):
        return self.__cost

    def draw(self, window: pygame.surface.Surface):
        # Рисуем рамку вокруг кнопки
        outline_rect = self.rect.inflate(10, 10)  # увеличиваем rect на 10 px с каждой стороны
        pygame.draw.rect(window, (127, 127, 127), outline_rect)

        # Отрисовываем изображение кнопки
        window.blit(self.image, self.rect.topleft)

        # Рендерим и отрисовываем текст (под кнопкой)
        text_surface = self.__font.render(str(self.__cost), True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            midtop=(self.rect.centerx, self.rect.bottom + 5)  # по центру под кнопкой, с отступом 5 px
        )
        window.blit(text_surface, text_rect)
# было
        # rect = self.rect.copy()
        # rect.width += 10
        # rect.height += 10
        # pygame.draw.rect(window, (127, 127, 127), rect )
        # window.blit(self.image, ( self.__x, self.__y ))
        # text = self.__font.render(str(self.__cost), True, (0, 0, 0))
        # window.blit(text, (self.__x, self.__y + 50))



class HealthButton(AbstrtactButton):
    def __init__(self,  x: int, y: int, event):
        super().__init__(x,y,"images/tower-repair.png", event, HEALTH_BUTTON_COST, "200")

class HeroButton(AbstrtactButton):
    def __init__(self,  x: int, y: int, event):
        super().__init__(x,y,"images/tower-hero.png", event, KNIGHT_BUTTON_COST, "400")

class ArcherButton(AbstrtactButton):
    def __init__(self,  x: int, y: int, event):
        super().__init__(x,y,"images/tower-archers.png", event, ARCHER_BUTTON_COST, "600")