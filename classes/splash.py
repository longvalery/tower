import asyncio

import pygame

class Splash():
    def __init__(self, width, height, fps, caption):
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption(caption)
        self.__stop = False
        self.__font = pygame.font.Font(None, 30)
        self.load_background()
        self.draw()

    def load_background(self):
        self.__backround = pygame.image.load("images/icon.png")
        self.__backround = pygame.transform.scale(self.__backround, ( self.__width, self.__height))

    def draw(self):
        self.__screen.blit(self.__backround, (0, 0))
        text = self.__font.render("Игра Защити БАШНЮ", True, (255,255,255))
        self.__screen.blit(text, (5, 30))
        text = self.__font.render("Нажмите пробел для продолжения", True, (255, 255, 255))
        self.__screen.blit(text, (5, 60))
        pygame.display.flip()


    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                self.__stop = True
            if event.type == pygame.QUIT:
                exit(1)

    async def loop(self):
        while not self.__stop:
            self.handle()
            await asyncio.sleep(0)  # 🔑 Критически важная строка!

