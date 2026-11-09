import asyncio
import random
import sys
import pygame

from classes.arrow import Arrow
from classes.buttons import HealthButton, HeroButton, ArcherButton, HEALTH_BUTTON_COST, KNIGHT_BUTTON_COST, \
    ARCHER_BUTTON_COST
from classes.defenders import Knight, Archer
from classes.enemies import Ork, Goblin, ENEMY_SIZE, Gnome
from classes.tower import Tower

CREATE_ENEMY_EVENT = pygame.USEREVENT + 1
BUTTON_HEALTH_EVENT = pygame.USEREVENT + 2
BUTTON_HERO_EVENT = pygame.USEREVENT + 3
BUTTON_ARCHER_EVENT = pygame.USEREVENT + 4
ARROW_COUNT = 4
TICK = 30
WIN_GAME = 1000

class Game():
    def __init__(self, width, height, fps, caption):
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode( (self.__width,  self.__height) )
        self.__floor = 515
        pygame.display.set_caption(caption)
        self.load_background()
        self.__tower = Tower(self.__width - 250, self.__floor - 350, 10_000)
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 5_000)
        self.__enemies = pygame.sprite.Group()
        self.__defenders = pygame.sprite.Group()
        self.__defender = 290
        self.__arrows = pygame.sprite.Group()
        self.__score = 0
        self.__font = pygame.font.Font(None, 40)

        self.__buttons = pygame.sprite.Group()
        self.__buttons.add(HealthButton(50, 50, BUTTON_HEALTH_EVENT))
        self.__buttons.add(HeroButton(150, 50, BUTTON_HERO_EVENT))
        self.__buttons.add(ArcherButton(250, 50, BUTTON_ARCHER_EVENT))

        self.__tick = TICK

    def load_background(self):
        self.__background = pygame.image.load("images/tower-background.png")
        self.__background = pygame.transform.scale(self.__background,(self.__width, self.__height ))

    def handle(self):
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                for button in self.__buttons:
                    if button.rect.collidepoint(mouse_position[0], mouse_position[1]):
                        # button.click()
                        if self.__score >= button.get_cost():
                            button.click()
                        return

                if len(self.__arrows) < ARROW_COUNT:
                    # print(mouse_position)
                    arrow = Arrow([self.__tower.rect.x + self.__tower.rect.width // 2 , self.__defender]
                                  , list(mouse_position))
                    self.__arrows.add(arrow)
            if event.type == pygame.QUIT:
                self.terminate()

            if event.type == BUTTON_HEALTH_EVENT:
                # print("BUTTON_HEALTH_EVENT")
                self.__score -= HEALTH_BUTTON_COST
                self.__tower.health += HEALTH_BUTTON_COST
            if event.type == BUTTON_HERO_EVENT:
                # print("BUTTON_HERO_EVENT")
                hero = Knight(self.__tower.rect.x, self.__floor )
                self.__score -= KNIGHT_BUTTON_COST
                self.__defenders.add(hero)
            if event.type == BUTTON_ARCHER_EVENT:
                hero = Archer(self.__tower.rect.x, self.__floor)
                self.__score -= ARCHER_BUTTON_COST
                self.__defenders.add(hero)
                #  !!! Homework
                # print("BUTTON_ARCHER_EVENT")
            if event.type == CREATE_ENEMY_EVENT:
                rand = random.randint(1, 100)
                if rand > 66:
                    enemy = Ork(-ENEMY_SIZE, self.__floor)
                elif rand > 33:
                    enemy = Gnome(-ENEMY_SIZE, self.__floor)
                else:
                    enemy = Goblin(-ENEMY_SIZE, self.__floor)
                self.__enemies.add(enemy)

    def update(self):
        self.__arrows.update()
        # print(len(self.__arrows))
        for arrow in self.__arrows:
            if arrow.rect.y > self.__floor:
                arrow.kill()
            if not arrow.rect.colliderect(self.__screen.get_rect()):
                arrow.kill()
            for enemy in self.__enemies:
                if enemy.rect.colliderect(arrow):
                    enemy.health = enemy.health - arrow.damage
                    arrow.kill()
                    if enemy.health < 0:
                        self.__score = self.__score + enemy.damage
                        enemy.kill()

        if self.__tower.health < 0:
            self.terminate()

        self.__tick = self.__tick - 1
        if self.__tick == 0:
            self.__tick = TICK

        for defender in self.__defenders:
            arrow = defender.update()
            if not arrow is None:
                self.__arrows.add(arrow)
            if self.__tick == TICK:
                for enemy in self.__enemies:
                    if defender.rect.colliderect(enemy.rect):
                        defender.stop()
                        defender.attack(enemy)
                        # print(enemy.health)
                        if enemy.health < 0:
                            self.__score = self.__score + enemy.damage
                            enemy.kill()

        self.__tower.attacked = False
        for enemy in self.__enemies:
            enemy.update()
            if self.__tick == TICK:
                if enemy.is_out(self.__width): # !!! Kill
                    enemy.kill()
                    continue
                enemy.start()

                if enemy.rect.colliderect(self.__tower.rect):
                    enemy.stop()
                    enemy.attack(self.__tower)
                    self.__tower.attacked = True

                for defender in self.__defenders:
                    if enemy.rect.colliderect(defender):
                        enemy.stop()
                        enemy.attack(defender)

                    if defender.health < 0:
                        defender.kill()

    def terminate(self):
        # Показать результат !!!
        sys.exit(0)

    def draw(self):
        self.__screen.blit(self.__background, (0, 0))
        self.__tower.draw(self.__screen)
        self.__arrows.draw(self.__screen)
        # pygame.draw.line(self.__screen, (0, 0, 0), (0, self.__defender)
        #                  , (self.__width , self.__defender) )


        for enemy in self.__enemies:
            enemy.draw(self.__screen)
        for defender in self.__defenders:
            defender.draw(self.__screen)

        self.show()
        for button in self.__buttons:
            button.draw(self.__screen)

        pygame.display.flip()
        self.__clock.tick(self.__fps)

    # await def loop(self):
    async def loop(self):
        # while True:
        while self.__tower.health > 0:
            self.handle()
            self.update()
            self.draw()
            await asyncio.sleep(0)  # 🔑 Критически важная строка!
            if self.__score > WIN_GAME:
                break
        return self.__tower.health, self.__score


    def show(self):
        text = self.__font.render(f"Очки {self.__score} Защита {self.__tower.health}"  # !!!
                                  , True, (0,0,0)
                                  )
        self.__screen.blit(text, (20 , 5))