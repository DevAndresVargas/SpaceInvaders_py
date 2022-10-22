import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,max_width,speed):
        super().__init__()
        self.image = pygame.image.load('../graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_width = max_width

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

    def constraint(self):
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.right >= self.max_width:
            self.rect.right = self.max_width

    def update(self):
        self.get_input()
        self.constraint()
