import random
import pygame

PATH_TO_IMAGES = "./images/" # !!!  windows = \  linux = /

PICTURE_SIZE = 100

def get_image(image_path, frame, width, height):
    sheet = pygame.image.load(image_path).convert_alpha()
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image.set_colorkey((0, 0, 0))
    return image


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))
    def show(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Platform(GameObject):
    def __init__(self, x, y, type):
        super().__init__(x, y, PATH_TO_IMAGES + "platforma.png", 200, 50)
        self.type = type
        if self.type == "BREAKING" :
            self.image.set_alpha(80)
        self.speed = random.randint(2, 8)   # !!!
    def update(self, scroll, WIDTH, HEIGHT):
        self.rect.y += scroll
        if self.type == "MOVING":
            self.rect.x += self.speed
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.speed *= -1
        if self.rect.top > HEIGHT:
            self.kill()

class Fireball(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, PATH_TO_IMAGES + "OGNEN.png", 35, 50)
    def update(self, enemy_group, moving_enemies_group) -> int:
        self.rect.y -= 20
        result = 0
        for enemy in enemy_group:
            if enemy.rect.colliderect(self.rect):
                enemy.kill()
                self.kill()
                result = 20
        for enemy in moving_enemies_group:
            if enemy.rect.colliderect(self.rect):
                enemy.kill()
                self.kill()
                result = 30
        if self.rect.bottom < 0:
            self.kill()
        return result

class MovingEnemy(GameObject):
    def __init__(self, image, y, frame_width, frame_heigth, WIDTH):
        super().__init__(WIDTH // 2, y, image, PICTURE_SIZE, PICTURE_SIZE)
        # self.image = get_image(image, 0, frame_width, frame_heigth)
        self.image = pygame.transform.scale(self.image, (frame_width, frame_heigth))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = y
        self.direction = random.choice([-5, 5])
        if self.direction > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image.set_colorkey((0, 0, 0))

    def update(self, scroll, HEIGHT, WIDTH):
        self.rect.y += scroll
        self.rect.x += self.direction
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1
            self.image = pygame.transform.flip(self.image, True, False)
            self.image.set_colorkey((0, 0, 0))


class Enemy(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, PICTURE_SIZE , PICTURE_SIZE)
    def update(self, scroll, HEIGHT):
        self.rect.y += scroll
        if self.rect.top > HEIGHT:
            self.kill()


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, PATH_TO_IMAGES + "geroy.png", PICTURE_SIZE, PICTURE_SIZE)
        self.flip = False
        self.velocity_y = 0
        self.jump = False   # !!!

    def move(self, WIDTH, GRAVITY, platform_group, SCROLL_THRESH, fireball_group):
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.jump = not self.jump
        if key[pygame.K_LEFT]:
            if self.rect.left < 0:
                self.rect.right = WIDTH
            self.rect.x -= 5
            self.flip = True
        if key[pygame.K_RIGHT]:
            if self.rect.right > WIDTH:  # !!!
                self.rect.left = 0
            self.rect.x += 5
            self.flip = False

        if key[pygame.K_SPACE]:
            if len(fireball_group) == 0:
                fireball = Fireball(self.rect.x + self.rect.width // 2 , self.rect.y)
                fireball_group.add(fireball)

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        for platform in platform_group:
            if platform.rect.colliderect(self.rect):
                if self.rect.bottom < platform.rect.bottom:
                    if self.velocity_y > 0:
                        self.rect.bottom = platform.rect.top
                        if self.jump:
                            self.velocity_y = -23
                        else:
                            self.velocity_y = 0
                    if platform.type == "BREAKING":
                        platform.kill()
        scroll = 0
        if self.rect.top <= SCROLL_THRESH:
            scroll = 15 # 5
        return scroll

    def show(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y))

