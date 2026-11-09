import pygame

from classes.arrow import Arrow
from classes.enemies import AbstractEnemy, ENEMY_SIZE

ARROW_COUNT = 60

class Knight(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, 300, 50, -1, "images/tower-hero.png")

class Archer(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 10, 0, "images/tower-archers.png")
        self.arrow_count = ARROW_COUNT
        self.__y = y
        self.__x = x
        self.__image = pygame.image.load("images/tower-archers.png")
        self.__image = pygame.transform.scale(self.__image, (ENEMY_SIZE, ENEMY_SIZE))


    def update(self):
        super().update()
        self.arrow_count -= 1
        result = None
        if self.arrow_count == 0:
            self.arrow_count = ARROW_COUNT
            y = self.__y - self.__image.get_height() // 2
            result = Arrow([self.__x, y] , [ -50, y])
        return result