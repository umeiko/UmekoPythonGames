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
    
    def game_over(self):
        pygame.init()
        score = self.calc_score()
        screen = pygame.display.set_mode((400, 400))
        font = pygame.font.Font(None, 75)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(200, 100))
        score_font = pygame.font.Font(None, 50)
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(200, 200))
        button_font = pygame.font.Font(None, 50)
        button_text = button_font.render("Restart", True, (255, 255, 255))
        button_rect = pygame.Rect(150, 250, 100, 50)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        clock = pygame.time.Clock()
        button_color = (0, 0, 255)
        hover_color = (0, 0, 200)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.__init__()
                        return

            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                current_color = hover_color
            else:
                current_color = button_color
            screen.fill((0, 0, 0))
            screen.blit(text, text_rect)
            screen.blit(score_text, score_text_rect)
            pygame.draw.rect(screen, current_color, button_rect)
            screen.blit(button_text, button_text_rect)
            pygame.display.flip()
            clock.tick(FPS)
    
    def random_gen(self):
        zero_id = []
        for k, i in enumerate(self.num_mat):
            if i == 0:
                zero_id.append(k)
        if len(zero_id) == 0:
            self.game_over()
            return
        idx = random.choice(zero_id)
        self.num_mat[idx] = random.choice([2, 4])
    
    def calc_score(self):
        score = 0
        for i in self.num_mat:
            score += i
        return score

    def moveup(self):
        for colum in range(4):
            idx = [colum + item * 4 for item in range(4)]
            colum_nums = [self.num_mat[i] for i in idx]
            out = self.move_line(colum_nums)
            for k, i in enumerate(idx):
                self.num_mat[i] = out[k]
    
    def movedown(self):
        for colum in range(3, -1, -1):
            idx = [colum + item * 4 for item in range(3, -1, -1)]
            colum_nums = [self.num_mat[i] for i in idx]
            out = self.move_line(colum_nums)
            for k, i in enumerate(idx):
                self.num_mat[i] = out[k]

    def moveleft(self):
        for colum in range(4):
            idx = [colum * 4 + item for item in range(4)]
            colum_nums = [self.num_mat[i] for i in idx]
            out = self.move_line(colum_nums)
            for k, i in enumerate(idx):
                self.num_mat[i] = out[k]
    
    def moveright(self):
        for colum in range(4):
            idx = [colum * 4 + item for item in range(3, -1, -1)]
            colum_nums = [self.num_mat[i] for i in idx]
            out = self.move_line(colum_nums)
            for k, i in enumerate(idx):
                self.num_mat[i] = out[k]
            
    def print_mat(self):
        print("\n", end="")
        for k, i in enumerate(self.num_mat):
            if k % 4 == 0:
                print("\n", end="")
            print(i, end="")

    def move_line(self, inputs:list):
        out = inputs.copy()
        if out[3] == out[2] or out[2] == 0:
            out[2] += out[3]
            out[3] = 0
        if out[2] == out[1] or out[1] == 0:
            out[1] += out[2]
            out[2] = 0
            if out[3] != 0:
                out[2] = out[3]
                out[3] = 0
        if out[0] == out[1] or out[0] == 0:
            out[0] += out[1]
            out[1] = 0
            if out[2] != 0:
                out[1] = out[2]
                out[2] = 0
                if out[3] != 0:
                    out[2] = out[3]
                    out[3] = 0
        return out


    def move(self, direction):
        if direction == UP:
            self.moveup()
        elif direction == DOWN:
            self.movedown()
        elif direction == LEFT:
            self.moveleft()
        elif direction == RIGHT:
            self.moveright()
    
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
                    ACTION = None
                    if event.key == pygame.K_UP:
                        ACTION = UP
                    elif event.key == pygame.K_DOWN:
                        ACTION = DOWN
                    elif event.key == pygame.K_RIGHT:
                        ACTION = RIGHT
                    elif event.key == pygame.K_LEFT:
                        ACTION = LEFT
                    
                    if ACTION != None:
                        cpy = game.num_mat.copy()
                        game.move(ACTION)
                        if  game.num_mat != cpy:
                            game.random_gen()

            game.render(screen)
            pygame.display.flip()
            clock.tick(FPS)


def main():
    game = The2048Game()
    main_loop(game)

if __name__ == '__main__':
	main()
