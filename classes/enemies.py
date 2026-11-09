import pygame
from pygame import Rect

ENEMY_SIZE = 70

class AbstractEnemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, health: int, damage: int, speed: int, image_path: str):
        super().__init__()
        self.__x = x
        self.health = health
        self.__max_health = health # !!!
        self.damage = damage
        self.__speed = speed
        self.__image_path = image_path
        self.__image = pygame.image.load(self.__image_path)
        self.__image = pygame.transform.scale(self.__image, (ENEMY_SIZE, ENEMY_SIZE))
        self.__y = y - self.__image.get_height()
        self.rect = self.__image.get_rect()
        self.__SPEED = speed


    def draw(self, window: pygame.surface.Surface):
        window.blit(self.__image, (self.__x, self.__y))
        SHIFT = 20
        health_bar_height = 5
        health_bar_y =  self.__y - 10
        health_bar_x = self.__x + SHIFT
        health_bar_width = self.__image.get_width() - 2 * SHIFT

        bg_rectangle = Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(window, (255, 0,      0) , bg_rectangle)
                                   #   Red  Green   Blue

        health_bar_width_green = int( self.health  / self.__max_health * health_bar_width )
        bg_rectangle = Rect(health_bar_x, health_bar_y, health_bar_width_green, health_bar_height)
        pygame.draw.rect(window, (0, 255, 0), bg_rectangle)




    def update(self):
        self.__x = self.__x + self.__speed
        self.rect.x = self.__x
        self.rect.y = self.__y

    def attack(self, target: object):
        target.health = target.health - self.damage

    def if_alive(self)-> bool:
        return self.damage > 0

    def is_out(self, x:int) -> bool:
        return self.__x > x

    def stop(self):
        self.__speed = 0

    def start(self):
        self.__speed = self.__SPEED

class Ork(AbstractEnemy):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, 100, 10, 1, "images/tower-enemy1.png")

class Goblin(AbstractEnemy):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, 200, 5, 1, "images/tower-enemy2.png")

class Gnome(AbstractEnemy):
    def __init__(self, x:int, y:int):
        super().__init__(x, y, 50, 20, 1, "images/tower-enemy3.png")