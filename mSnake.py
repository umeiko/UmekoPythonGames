"""
    一个还挺好玩的贪吃蛇小游戏
"""

import pygame
import random


# 蛇和苹果的数组逻辑
class Snake:
	def __init__(self, ini_pos=[0, 0], ini_dir=3):
		self.pos_list  = [ini_pos]
		# [0,1,2,3] --> [up, down, left, right]
		self.dir       = ini_dir
		self.apple_pos = None
		self.snake_radius = 5
		# self.distance  = self.snake_radius * 2
		self.gen_apple()

	# 修改蛇的前进方向
	def turn(self, input_dir):
		if self.dir == 0 and input_dir == 1:
			return self.dir
		elif self.dir == 1 and input_dir == 0:
			return self.dir
		elif self.dir == 2 and input_dir == 3:
			return self.dir
		elif self.dir == 3 and input_dir == 2:
			return self.dir
		else:
			self.dir = input_dir

	# 刷新蛇的位置
	def fresh_pos(self, screen_size=(640, 480), eat_apple=False):
		# 生成一个新的头部
		head_pos = self.pos_list[0].copy()
		self.pos_list.insert(0, head_pos)
		# 刷新头部的位置
		if self.dir == 2:
			self.pos_list[0][0] += self.snake_radius * 0.8
		if self.dir == 3:
			self.pos_list[0][0] -= self.snake_radius * 0.8
		if self.dir == 1:
			self.pos_list[0][1] += self.snake_radius * 0.8
		if self.dir == 0:
			self.pos_list[0][1] -= self.snake_radius * 0.8

		# x方向出界了，从最左边伸出来
		if self.pos_list[0][0] > screen_size[0]:
			self.pos_list[0][0] -= screen_size[0]
		# x方向出界了，从最右边伸出来
		if self.pos_list[0][0] < 0:
			self.pos_list[0][0] += screen_size[0]
		# y方向出界了，从最上边伸出来
		if self.pos_list[0][1] > screen_size[1]:
			self.pos_list[0][1] -= screen_size[1]
		# y方向出界了，从最右边伸出来
		if self.pos_list[0][1] < 0:
			self.pos_list[0][1] += screen_size[1]

		# 没有吃苹果的时候，删除尾部
		if not eat_apple:
			self.pos_list.pop(-1)


	# 检查有没有吃到苹果
	def apple_check(self, check_dis=15):
		dis = pow(abs(self.pos_list[0][0] - self.apple_pos[0]), 2) + pow(abs(self.pos_list[0][1] - self.apple_pos[1]), 2)
		if dis >= check_dis ** 2:
			return False
		else:
			return True

	# 检查有没有撞到身体
	def snake_check(self):
		for i in self.pos_list[3:]:
			dis = pow(abs(self.pos_list[0][0] - i[0]), 2) + pow(abs(self.pos_list[0][1] - i[1]), 2)
			if dis <= self.snake_radius ** 2:
				return True
		return False

	# 检查苹果的生成位置是否合法(不要生成到蛇的身体里面)
	def gen_check(self, apple_pos, check_dis=15):
		for i in self.pos_list:
			dis = pow(abs(apple_pos[0] - i[0]), 2) + pow(abs(apple_pos[1] - i[1]), 2)
			# 如果位置不合法
			if dis <= check_dis ** 2:
				return False
		return True

	# 在正确的位置生成一个苹果
	def gen_apple(self, screen_size=(640, 480), apple_radius=10):
		check_dis = apple_radius + self.snake_radius
		correct_apple = False
		# 检查苹果的生成位置是否合法
		while not correct_apple:
			# 随机生成苹果位置
			apple_pos = [random.randint(0, screen_size[0]), random.randint(0, screen_size[1])]
			# 检查苹果的生成位置是否合法
			correct_apple = self.gen_check(apple_pos, check_dis=check_dis)
		self.apple_pos = apple_pos


# pygame 游戏主体
class Snake_game:	
    # 初始化参数
    def __init__(self):
        self.screen_size = (640, 480)
        self.screen = pygame.display.set_mode(size=self.screen_size)
        self.clock = pygame.time.Clock()
        self.color = pygame.Color('green')
        self.init_FPS    = 20
        self.FPS_upper = 1.03
        self.FPS   = self.init_FPS
        self.max_FPS      = 35
        self.Snake_radius = 25
        self.snake = Snake(ini_pos=[int(self.screen_size[0]/2), int(self.screen_size[1]/2)])
        self.snake.snake_radius = self.Snake_radius
        self.apple_eaten = False
        self.apple_radius = 10

    # 绘图函数，画出游戏界面
    def snake_render(self):
        pygame.draw.circle(self.screen, pygame.Color('blue'), self.snake.pos_list[0], radius=self.Snake_radius)
        pygame.draw.circle(self.screen, pygame.Color('red'), self.snake.apple_pos, radius=self.apple_radius)
        
        if len(self.snake.pos_list) > 1:
            ini_G = 255
            for i in self.snake.pos_list[1:]:
                ini_G = ini_G - 5 if ini_G > 0 else 0
                pygame.draw.circle(self.screen, pygame.Color((0, ini_G, 0)), i, radius=self.Snake_radius)
	
	# 游戏的规则控制
    def rules_control(self):
        # 刷新蛇的位置
        self.snake.fresh_pos(eat_apple=self.apple_eaten)
        
        # 碰撞了就输掉
        if self.snake.snake_check():
            # self.snake_render()
            # pygame.display.flip()
            self.clock.tick(0.5)
            print("you lose")
            self.reset()
            return None
        
        # 吃到苹果就生成新苹果
        self.apple_eaten = self.snake.apple_check(check_dis=self.apple_radius+self.Snake_radius)
        if self.apple_eaten:
            self.FPS = self.FPS * self.FPS_upper if self.FPS < self.max_FPS else self.max_FPS
            self.apple_radius = random.randint(7, 15)
            self.snake.gen_apple(apple_radius=self.apple_radius)
        
        # 刚开始游戏时蛇长一些
        if len(self.snake.pos_list) <= 3:
            self.apple_eaten = True

    def reset(self):
        self.FPS = self.init_FPS
        self.snake.pos_list.clear()
        self.snake.pos_list.append([int(self.screen_size[0]/2), int(self.screen_size[1]/2)])
    
    # 主循环
    def main_loop(self):
        pygame.init()	
        while True:
            # 事件检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.turn(0)
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn(1)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn(2)
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn(3)

            # 计算更新游戏
            self.rules_control()
            
            # 屏幕渲染
            self.screen.fill(pygame.Color('white'))
            self.snake_render()
            pygame.display.flip()
            self.clock.tick(self.FPS)
            # 在窗口上显示帧率和得分
            pygame.display.set_caption(f"Score:{len(self.snake.pos_list)-3}, FPS: {round(self.clock.get_fps(), 3)}")


def main():
    game = Snake_game()
    game.main_loop()


if __name__ == '__main__':
	main()

