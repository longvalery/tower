# /// script
dependencies = [
 "pygame-ce",
 "pygame-gui",
 "python-i18n",
]
# ///
# https://domino-sender.itch.io/castle-defender

import asyncio
import pygame
from classes.finish import Finish
from classes.game import Game
from classes.splash import Splash


async def main():
    splash = Splash(600, 600, 60, "Начинаем игру")
    await splash.loop()
    game = Game(1200, 600, 60, "Защита башни")
    health, score  = await game.loop()
    if health > 0:
        finish = Finish(600, 600, 60, "Победа", score, win=True)
    else:
        finish = Finish(600, 600, 60, "Провал", score, win=False)
    await finish.loo1200p()

if __name__ == "__main__":
    pygame.init()  # !!!!
    asyncio.run(main())

# Проверка домашнего задания.
# Исправить ошибку при добавлении Защитника.
# Добавить отображение здоровья участников.
# Добавление Стартового экрана.
# Создать экран окончания игры - class Finish
# Аналогичный классу Splash


# TOR
# about:config
# network.proxy.no_proxies_on = localhost,127.0.0.1,192.168.0.50
# network.proxy.allow_hijacking_localhost = True
#
# set PYTHONUTF8=1 && pygbag --disable-sound-format-error --bind 192.168.0.50 main.py
#
# $env:PYTHONUTF8=1; pygbag --disable-sound-format-error --bind 192.168.0.50 main.py



