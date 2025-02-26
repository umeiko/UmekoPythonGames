import pygame
import random

UP   = 0
DOWN = 1
LEFT = 2
RIGHT = 3
FPS = 60

NUMBER_0_COLOR = (205, 193, 180)
NUMBER_2_COLOR = (238, 228, 218)
NUMBER_4_COLOR = (237, 224, 200)
NUMBER_8_COLOR = (242, 177, 121)
NUMBER_16_COLOR = (245, 149, 99)
NUMBER_32_COLOR = (246, 124, 95)
NUMBER_64_COLOR = (247, 95, 59)
NUMBER_128_COLOR = (237, 207, 114)
NUMBER_256_COLOR = (237, 204, 97)
NUMBER_512_COLOR = (237, 200, 80)
NUMBER_1024_COLOR = (237, 197, 63)
NUMBER_2048_COLOR = (237, 194, 46)

COLORS = {
    0: NUMBER_0_COLOR,
    2: NUMBER_2_COLOR,
    4: NUMBER_4_COLOR,
    8: NUMBER_8_COLOR,
    16: NUMBER_16_COLOR,
    32: NUMBER_32_COLOR,
    64: NUMBER_64_COLOR,
    128: NUMBER_128_COLOR,
    256: NUMBER_256_COLOR,
    512: NUMBER_512_COLOR,
    1024: NUMBER_1024_COLOR,
    2048: NUMBER_2048_COLOR,
}

class The2048Game():
    def __init__(self):
        randgen = [2 for _ in range(3)] + [4 for _ in range(2)] + [0 for _ in range(11)]
        random.shuffle(randgen)
        self.num_mat = randgen
        self.score = 0
    
    def random_gen(self):
        for i in self.num_mat:
            for j in i:
                if j == 0:
                    return True

    def moveup(self):
        for line in range(2, -1, -1):
            for element in range(4):
                if self.num_mat[line * 4 + element] == self.num_mat[(line + 1) * 4 + element] or self.num_mat[line * 4 + element] == 0:
                    self.num_mat[line * 4 + element] += self.num_mat[(line + 1) * 4 + element]
                    self.num_mat[(line + 1) * 4 + element] = 0
                    if (line+2) < 3:
                        if self.num_mat[(line + 2) * 4 + element] != 0:
                            self.num_mat[(line + 1) * 4 + element] = self.num_mat[(line + 2) * 4 + element]




    def move(self, direction):
        if direction == UP:
            self.moveup()
        # elif direction == DOWN:
        #     self.movedown()
        # elif direction == LEFT:
        #     self.moveleft()
        # elif direction == RIGHT:
    
    def render(self, surf:pygame.Surface):
        surf.fill((187, 173, 160))
        font = pygame.font.Font(None, 55)
        for i in range(4):
            for j in range(4):
                value = self.num_mat[i * 4 + j]
                if value != 0:
                    pygame.draw.rect(surf, COLORS[value], (j * 100 + 5, i * 100 + 5, 90, 90))
                    text = font.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(j * 100 + 50, i * 100 + 50))
                    surf.blit(text, text_rect)
                else:
                    pygame.draw.rect(surf, (205, 193, 180), (j * 100 + 5, i * 100 + 5, 90, 90))


def main_loop(game:The2048Game):
        pygame.init()
        pygame.display.set_caption('2048')
        screen = pygame.display.set_mode((400, 400))
        clock = pygame.time.Clock()
        while True:
            # 事件检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.move(UP)
                    elif event.key == pygame.K_DOWN:
                        game.move(DOWN)
                    elif event.key == pygame.K_RIGHT:
                        game.move(RIGHT)
                    elif event.key == pygame.K_LEFT:
                        game.move(LEFT)

            # 计算更新游戏
            # self.rules_control()
            # 屏幕渲染

            screen.fill(pygame.Color('white'))
            game.render(screen)
            pygame.display.flip()
            clock.tick(FPS)


def main():
    game = The2048Game()
    main_loop(game)

if __name__ == '__main__':
	main()
