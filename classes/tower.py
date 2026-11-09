import pygame
from pygame import SurfaceType, Rect


class Tower(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, health:int):
        super().__init__()
        self.__max_health = health
        self.__image = pygame.image.load("images/tower-tower.png")
        self.__image = pygame.transform.scale(self.__image, (200, 350))
        self.__x = x
        self.__y = y
        self.health = health
        self.rect = self.__image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.create_red_tower()
        self.attacked = False
        self.__attacked_count = 0
        self.__normal = True

    def create_red_tower(self):
        self.__blended_image = self.__image.copy()
        width = self.__blended_image.get_width()
        height = self.__blended_image.get_height()
        red_surface = pygame.Surface( (width, height) , pygame.SRCALPHA)
        red_surface.fill( ( 255, 0, 0, 250 ) )
        for x in range(width):
            for y in range(height):
                pixel = self.__image.get_at( (x, y) )
                red_pixel =  red_surface.get_at( (x, y) )
                blend_color = [
                    (pixel[0] * red_pixel[0]) // 255, # red
                    (pixel[1] * red_pixel[1]) // 255, # green
                    (pixel[2] * red_pixel[2]) // 255, # blue
                    pixel[3]
                ]
                if blend_color[0] == 1 and blend_color[1] == 1 and blend_color[2] == 1:
                    blend_color = (0, 0, 0, 255)
                self.__blended_image.set_at( (x,y), blend_color )
        self.__blended_image.set_colorkey( (255,255,255,255) )


    def draw(self, window: SurfaceType):
        if not self.attacked:
            window.blit(self.__image, (self.__x, self.__y))
        else:
            self.__attacked_count = self.__attacked_count + 1
            if self.__attacked_count > 15:
                self.__attacked_count = 0
                self.__normal = not self.__normal
            if self.__normal:
                window.blit(self.__blended_image, (self.__x, self.__y))
            else:
                window.blit(self.__image, (self.__x, self.__y))
        SHIFT = 20
        health_bar_height = 5
        health_bar_y = self.__y - 10
        health_bar_x = self.__x + SHIFT
        health_bar_width = self.__image.get_width() - 2 * SHIFT

        bg_rectangle = Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(window, (255, 0, 0), bg_rectangle)
        #   Red  Green   Blue

        health_bar_width_green = int(self.health / self.__max_health * health_bar_width)
        bg_rectangle = Rect(health_bar_x, health_bar_y, health_bar_width_green, health_bar_height)
        pygame.draw.rect(window, (0, 255, 0), bg_rectangle)


    def update(self):
        pass



