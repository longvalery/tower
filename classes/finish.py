import asyncio

import pygame

class Finish():
    def __init__(self, width, height, fps, caption, score, win=False):
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption(caption)
        self.__score = score
        self.__win = win
        self.__stop = False
        self.__font = pygame.font.Font(None, 30)
        self.load_background()
        self.draw()

    def load_background(self):
        if self.__win:
            background = "images/tower-win.png"
        else:
            background = "images/tower-lose.png"
        self.__backround = pygame.image.load(background)
        self.__backround = pygame.transform.scale(self.__backround, ( self.__width, self.__height))

    def draw(self):
        self.__screen.blit(self.__backround, (0, 0))
        text = self.__font.render(f"Набрали {self.__score} очков", True, (255,255,255))
        self.__screen.blit(text, (5, 30))
        pygame.display.flip()


    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(1)
                self.__stop = True
            if event.type == pygame.QUIT:
                exit(1)

    async def loop(self):
        while not self.__stop:
            self.handle()
            await asyncio.sleep(0)  # 🔑 Критически важная строка!

