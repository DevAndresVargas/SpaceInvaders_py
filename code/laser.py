import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,max_height,laser_sound):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.max_height = max_height

        # Audio
        laser_sound.play()

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y > self.max_height + 50 :
            self.kill()

    def update(self):
        self.rect.y -= self.speed
        self.destroy()
