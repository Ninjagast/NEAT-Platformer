import pygame
import os

class Player:
    def __init__(self):
        self.x = 32
        self.y = 321
        self.isDead = False
        self.speed = 2
        self.grounded = True
        self.jumpMomentum_x = 0  # hangt van de strenght af
        self.jumpMomentum_y = 0  # hangt van de strenght af
        self.texture = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "player.png")))
        self.deadTexture = pygame.transform.grayscale(self.texture)
        self.gravity = 0.6

        self.waited = 0  # anti troll mechanism
        self.timeStayedOnePlatform = 0

        self.diePoints = -10
        self.landJumpPoints = 0
        self.fallingPoints = 0
        self.jumpPoints = 0
        self.jumpSackLen = 0
        self.waitingPoints = -10
        self.isFalling = False

    def update(self, action: str, value, platforms: [], platform_sack: []) -> int:
        if self.y > 416:
            self.isDead = True
            return self.diePoints

        self.timeStayedOnePlatform += 1

        if self.timeStayedOnePlatform > 200:
            self.isDead = True
            return self.diePoints

        if not self.isDead:
            return self.movement(action, value, platforms, platform_sack) + 1

    def movement(self, action: str, value, platforms: [], platform_sack: []) -> int:
        player_mask = pygame.mask.from_surface(self.texture)
        collided = False
        return_points = 0

        for platform in platforms:
            collided = self.collision_check(player_mask, platform)
            if collided:
                break

        if (not collided and self.grounded) or self.isFalling:  # falling of the edge
            self.y += 4
            self.isFalling = True
            return self.fallingPoints

        if collided and not self.grounded:  # landed from a jump
            self.grounded = True
            return 0

        if not collided and not self.grounded:  # in the middle of a jump
            self.timeStayedOnePlatform -= 1
            self.y -= self.jumpMomentum_y
            self.jumpMomentum_y -= self.gravity
            for platform in platforms:
                platform.move(-self.jumpMomentum_x)
            result2 = False
            for x, platform in enumerate(platforms): # if we are colliding in the next frame
                result2 = self.collision_check(player_mask, platform)
                if result2:
                    if x == 0:
                        if self.jumpSackLen == len(platform_sack):
                            return_points -= self.landJumpPoints
                            self.timeStayedOnePlatform += 10
                    else:
                        self.timeStayedOnePlatform = 0
                    break

            if result2:
                if self.y < 335:
                    self.y = 321
                    for platform in platforms:
                        platform.move(-self.jumpMomentum_x)
                    self.jumpMomentum_y = 0
                    return return_points + self.landJumpPoints
                else:
                    self.isDead = True
                    return return_points + self.diePoints
            else:
                return 0

        if action == "walk" and self.grounded:
            self.waited = 0
            for platform in platforms:
                platform.move(value * self.speed)
            return 0

        if action == "jump" and self.grounded:
            self.jumpSackLen = len(platform_sack)
            self.waited = 0
            self.grounded = False
            actualValueX = ((12 - 0) * (value[0] - -1) / (1 - -1) + 0)
            actualValueY = ((12 - 0) * (value[1] - -1) / (1 - -1) + 0)

            if actualValueY < 2:
                actualValueY = 2
            if actualValueX < 2:
                actualValueX = 2

            self.jumpMomentum_x = actualValueX
            self.jumpMomentum_y = actualValueY

            self.y -= self.jumpMomentum_y
            self.jumpMomentum_y -= self.gravity
            for platform in platforms:
                platform.move(-self.jumpMomentum_x)
            return self.jumpPoints

        if action == "":
            self.waited += 1
            if self.waited > 5:
                self.isDead = True
                return self.diePoints
            return self.waitingPoints

    def collision_check(self, player_mask, platform) -> bool:
        top_offset = (self.x - platform.x, self.y - platform.y)
        platform_mask = pygame.mask.from_surface(platform.texture)

        collision_point = platform_mask.overlap(player_mask, top_offset)

        if collision_point:
            return True
        return False

    def draw(self, win):
        new_rect = self.texture.get_rect(center=self.texture.get_rect(topleft=(self.x, self.y)).center)

        if self.isDead:
            win.blit(self.deadTexture, new_rect.topleft)
        else:
            win.blit(self.texture, new_rect.topleft)