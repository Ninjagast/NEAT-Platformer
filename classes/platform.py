class Platform:

    def __init__(self, pos: tuple, texture):
        self.x = pos[0]
        self.y = pos[1]
        self.texture = texture
        self.width = self.texture.get_width()


    def draw(self, win):
        new_rect = self.texture.get_rect(center=self.texture.get_rect(topleft=(self.x, self.y)).center)
        win.blit(self.texture, new_rect.topleft)

    def move(self, x_value):
        self.x += x_value