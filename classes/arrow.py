import math
import pygame
from pygame import SurfaceType


class Arrow(pygame.sprite.Sprite):
    def __init__(self, start: list, target: list):
        super().__init__()
        self.__start = start
        self.__target = target
        self.__xy = start
        dx = target[0] - start[0]
        dy = target[1] - start[1]
        self.__angle = math.atan(dy/dx)
        self.__speed = 5
        self.damage = 10
        self.image = pygame.image.load("images/tower-arrow.png")
        self.image = pygame.transform.scale(self.image, (40, 10))
        self.image = pygame.transform.rotate(self.image, math.degrees(- self.__angle))
        self.rect = self.image.get_rect()
        self.rect.x = self.__xy[0]
        self.rect.y = self.__xy[1]


    def update(self, *args, **kwargs):
        self.__xy[0] = self.__xy[0] - self.__speed * math.cos(self.__angle)
        self.__xy[1] = self.__xy[1] - self.__speed * math.sin(self.__angle)
        self.rect.x = self.__xy[0]
        self.rect.y = self.__xy[1]

    def draw(self, window: SurfaceType):
        window.blit(self.image, self.__xy)







