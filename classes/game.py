import pygame
import os
import random
from classes.platform import Platform


class Game:

    def __init__(self):
        random.seed(20)
        self.running = True
        self.bg_texture = pygame.image.load(os.path.join("assets/background_stuff", "BG.png"))
        self.platforms = []
        self.platforms.append(Platform((0, 384), pygame.image.load("assets/platforms/bigPlatform.png")))
        self.platforms.append(Platform((384, 384), pygame.image.load("assets/platforms/bigPlatform.png")))
        self.platform_sack = ["assets/platforms/bigPlatform.png", "assets/platforms/smallPlatform.png", "assets/platforms/midPlatform.png"]
        random.shuffle(self.platform_sack)
        self.score = 0
        self.inputs = ["cprelxpos", "prelxpos", "prelxpos2", "psize", "distance"]

    def draw(self, win, player):
        win.blit(self.bg_texture, (0, 0))

        player.draw(win)

        for platform in self.platforms:
            platform.draw(win)

        STAT_FONT = pygame.font.SysFont("comicsans", 50)
        text = STAT_FONT.render("Score: " + str(self.score), True, (255, 255, 255))
        win.blit(text, (640 - 10 - text.get_width(), 10))

        pygame.display.update()

    def update(self, player, network) -> int:
        output = self.getInputs(network=network, player=player)
        return_fitness = 0
        if output[0] > 0.5: #jump + jump strength x/y
            player.update(action="jump", value=(output[1], output[2]), platforms=self.platforms,
                                            platform_sack=self.platform_sack)
        else: #walk right
            player.update(action="walk", value=-2, platforms=self.platforms,
                                            platform_sack=self.platform_sack)

        for x, platform in enumerate(self.platforms):
            if platform.x + platform.width < 0:
                self.platforms.pop(x)
                self.spawnPlatform(player=player)
                self.score += 1
                return_fitness += 30 + self.score * 10

        if player.isDead:
            self.running = False

        if self.score > 500:
            self.running = False
            return 100000

        return return_fitness

    def spawnPlatform(self, player):
        if len(self.platform_sack) < 1:
            self.platform_sack = ["assets/platforms/bigPlatform.png", "assets/platforms/smallPlatform.png",
                                  "assets/platforms/midPlatform.png"]
            random.shuffle(self.platform_sack)

        offset = random.randint(500, 600)
        self.platforms.append(Platform((player.x + offset, 384), pygame.image.load(self.platform_sack[0])))
        self.platform_sack.pop(0)

    def getInputs(self, network, player):
        inputs = ()
        currentPlatform = self.platforms[0]
        nextPlatform = self.platforms[1]

        for inputType in self.inputs:
            if inputType == "xpos":
                inputs = inputs + (player.x,)
            if inputType == "ypos":
                inputs = inputs + (player.y,)
            if inputType == "grounded":
                inputs = inputs + (player.grounded,)

            if inputType == "cpxpos":
                inputs = inputs + (currentPlatform.x,)
            if inputType == "cpypos":
                inputs = inputs + (currentPlatform.y,)
            if inputType == "cpxlastpos":
                inputs = inputs + (currentPlatform.x + currentPlatform.width,)
            if inputType == "cpsize":
                inputs = inputs + (currentPlatform.width,)
            if inputType == "cprelxpos":
                inputs = inputs + (((player.x - (currentPlatform.x + currentPlatform.width)) * -1),)

            if inputType == "pxpos":
                inputs = inputs + (nextPlatform.x,)
            if inputType == "pypos":
                inputs = inputs + (nextPlatform.y,)
            if inputType == "pxlastpos":
                inputs = inputs + (nextPlatform.x + nextPlatform.width,)
            if inputType == "psize":
                inputs = inputs + (nextPlatform.width,)
            if inputType == "prelxpos":
                inputs = inputs + (((player.x - (nextPlatform.x + nextPlatform.width)) * -1),)
            if inputType == "prelxpos2":
                inputs = inputs + (((player.x - nextPlatform.x) * -1),)
            if inputType == "distance":
                inputs = inputs + ((currentPlatform.x + currentPlatform.width) - nextPlatform.x,)

        return network.activate(inputs)

    def IsRunning(self) -> bool:
        return self.running
