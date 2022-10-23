import pygame, sys
from player import Player
import obstacle

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
        self.create_multiple_obstacles(self.obstacle_x_positions,x_init = screen_width / 15,y_init = 480)

    def create_obstacle(self,x_init,y_init, offset_x):
        for row_index,row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_init + col_index * self.block_size + offset_x
                    y = y_init + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,offset,x_init,y_init):
        for offset_x in offset:
            self.create_obstacle(x_init,y_init,offset_x)

    def run(self):
        self.player.update()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        # update all sprite groups
        # draw all sprite groups


if __name__ == "__main__":
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        screen.fill((30,30,30))
        game.run()
        pygame.display.flip()
        clock.tick(60)
