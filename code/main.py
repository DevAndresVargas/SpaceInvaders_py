import pygame, sys
from player import Player
import obstacle
from alien import Alien,Extra
from random import choice,randint
from laser import Laser

class Game:
    def __init__(self):
        # Player Setup
        player_sprite = Player((screen_width / 2, screen_height),screen_width,5,8)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) \
                                     for num in range(self.obstacle_amount)]

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40,80)


        self.create_multiple_obstacles(self.obstacle_x_positions,x_init =\
                                       screen_width / 15,y_init = 480)


    def create_obstacle(self,x_init,y_init, offset_x):
        for row_index,row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_init + col_index * self.block_size + offset_x
                    y = y_init + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(251,59,100),x,y)
                    self.blocks.add(block)


    def create_multiple_obstacles(self,offset,x_init,y_init):
        for offset_x in offset:
            self.create_obstacle(x_init,y_init,offset_x)


    def alien_setup(self,rows,cols,x_distance = 60,y_distance = 40,\
                    x_offset = 70,y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                match row_index:
                    case 0:
                        color = 'yellow'
                    case 1:
                        color = 'green'
                    case 2:
                        color = 'green'
                    case _:
                        color = 'red'

                alien_sprite = Alien(color,x,y)
                self.aliens.add(alien_sprite)


    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)


    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance


    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,-6,screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),screen_width))
            self.extra_spawn_time = randint(400,800)

    def collision_checks(self):

        # player lasers
        if self.player.sprite.lasers:
           for laser in self.player.sprite.lasers:

               # obstacle collissions
               if pygame.sprite.spritecollide(laser,self.blocks,True):
                   laser.kill()

               # aliens collissions
               if pygame.sprite.spritecollide(laser,self.aliens,True):
                   laser.kill()

               # extra collissions
               if pygame.sprite.spritecollide(laser,self.extra,True):
                   laser.kill()

        # alien lasers
        if self.alien_lasers:
           for laser in self.alien_lasers:

               # obstacle collissions
               if pygame.sprite.spritecollide(laser,self.blocks,True):
                   laser.kill()

               # aliens collissions
               if pygame.sprite.spritecollide(laser,self.player,False):
                   laser.kill()
                   print('hit')

        # aliens
        if self.aliens:
            for alien in self.aliens:
               pygame.sprite.spritecollide(alien,self.blocks,True)

               if pygame.sprite.spritecollide(alien,self.player,False):
                   pygame.quit()
                   sys.exit()

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        # update all sprite groups
        # draw all sprite groups


if __name__ == "__main__":
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER :
                game.alien_shoot()


        screen.fill((30,30,30))
        game.run()
        pygame.display.flip()
        clock.tick(60)
