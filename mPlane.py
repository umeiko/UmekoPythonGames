"""
    一个还挺好玩的飞机大战小游戏
"""
import pygame
import random
import time


def strike_check(pos_A, pos_B, check_dis):
    """碰撞检测"""
    dis = (pos_A[0] - pos_B[0])**2 + (pos_A[1] - pos_B[1])**2
    if dis >= (check_dis ** 2):
        return False
    else:
        return True

# 超出边界后到达屏幕另一端
def circulate_screen(raw_pos, screen_size=(640, 480)):
	new_pos = raw_pos.copy()
	# x方向出界了，从最左边伸出来
	if new_pos[0] > screen_size[0]:
		new_pos[0] -= screen_size[0]
	# x方向出界了，从最右边伸出来
	if new_pos[0] < 0:
		new_pos[0] += screen_size[0]
	# y方向出界了，从最上边伸出来
	if new_pos[1] > screen_size[1]:
		new_pos[1] -= screen_size[1]
	# y方向出界了，从最右边伸出来
	if new_pos[1] < 0:
		new_pos[1] += screen_size[1]
	return new_pos


# 玩家飞机
class Plane:
	def __init__(self, plane_pos=[0, 0], spd=10):
		self.plane_pos  = plane_pos
		# 各个方向上的运行速度
		self.state = [0, 0]
		self.spd   = spd
		self.bullet_spd = 10
		self.enemy_list  =  []
		self.bullet_list =  []


	# 操作飞机
	def turn(self, input_state):
		# [up, down, left, right, stop_x, stop_y]
		if input_state == 0:
			self.state[1] = - self.spd
		elif input_state == 1:
			self.state[1] = self.spd
		elif input_state == 2:
			self.state[0] = self.spd
		elif input_state == 3:
			self.state[0] = - self.spd
		elif input_state == 4:
			self.state[0] = 0
		elif input_state == 5:
			self.state[1] = 0


	# 发射一枚子弹
	def fire(self):
		self.bullet_list.append(self.plane_pos.copy())

	# 生成一个敌人
	def gen_enemy(self, pos=None, screen_size=(640, 480)):
		if pos is None:
			pos = [random.randint(0, screen_size[0]), 0]
		self.enemy_list.append(pos)


	# 刷新各个单位位置
	def fresh_pos(self, screen_size=(640, 480), eat_apple=False):
		# self.plane_pos[0] += self.state[0]
		# self.plane_pos[1] += self.state[1]
		# # 循环屏幕
		# self.plane_pos = circulate_screen(self.plane_pos, screen_size)
		
		# 刷新子弹位置
		for i in self.bullet_list:
			i[1] -= self.bullet_spd
			if i[1] > screen_size[1] or i[1] < 0:
				self.bullet_list.remove(i)

		# 刷新敌人位置
		for i in self.enemy_list:
			i[1] += self.spd
			# 追踪我方
			if i[0] > self.plane_pos[0]:
				i[0] -= 2
			else:
				i[0] += 2
			# if i[1] > screen_size[1] or i[1] < 0:
			# 	self.enemy_list.remove(i)
			i_new = circulate_screen(i, screen_size)
			i[0] += -i[0] + i_new[0]
			i[1] += -i[1] + i_new[1]


	# 检查是否杀敌
	def kill_check(self, bullet_radius, enemy_radius):
		kill_num = 0
		for i in self.enemy_list:
			for j in self.bullet_list:
				if strike_check(i, j, check_dis=bullet_radius+enemy_radius):
					kill_num += 1
					# 防止重复删除
					if i in self.enemy_list:
						self.enemy_list.remove(i)
						self.bullet_list.remove(j)	
		return kill_num

	# 检查是否撞到敌人
	def death_check(self, plane_radius, enemy_radius):
		for i in self.enemy_list:
			if strike_check(i, self.plane_pos, check_dis=plane_radius+enemy_radius):
				return True
		return False		


# pygame 游戏主体
class Plane_game:	
	# 初始化参数
	def __init__(self):
		self.screen_size = (640, 480)
		self.screen = pygame.display.set_mode(size=self.screen_size)
		self.clock  = pygame.time.Clock()
		self.color  = pygame.Color('green')
		self.FPS    = 30
		self.planes = Plane(plane_pos=[self.screen_size[0]/2, self.screen_size[1]],)
		self.planes.spd  =  2
		self.score  = 0
		self.hardness_rate = 98
		self.ini_time      = time.time()
		self.hardness_time = time.time()
		self.spd_time      = time.time()

		self.plane_radius  = 10
		self.bullet_radius = 5
		self.enemy_radius  = 10

	# 绘图函数，画出游戏界面
	def render(self):
		pygame.draw.circle(self.screen, pygame.Color('blue'), self.planes.plane_pos, radius=self.plane_radius)
		
		for i in self.planes.enemy_list:
			pygame.draw.circle(self.screen, pygame.Color('green'), i, radius=self.enemy_radius)
		for i in self.planes.bullet_list:
			pygame.draw.circle(self.screen, pygame.Color('red'), i, radius=self.bullet_radius)

	# 游戏的规则控制
	def rules_control(self):
		self.planes.fresh_pos()
		self.score += self.planes.kill_check(self.bullet_radius, self.enemy_radius)
		
		if random.randint(0, 100) >= self.hardness_rate:
			self.planes.gen_enemy()
		
		if self.planes.death_check(self.plane_radius, self.enemy_radius):
			self.screen.fill(pygame.Color('white'))
			self.render()
			pygame.display.flip()
			print("GAME OVER")
			time.sleep(2)
			self.restart()

		# 每过10秒增加难度
		if time.time() - self.hardness_time >= 10:
			self.hardness_rate -= 1
			self.hardness_time = time.time()
		# 每过10秒增加速度
		if time.time() - self.spd_time >= 20:
			if self.planes.spd <= 20:
				self.planes.spd += 2
			self.spd_time = time.time()

	# 重启游戏
	def restart(self):
		self.score  = 0
		self.planes.enemy_list  =  []
		self.planes.bullet_list =  []
		self.planes.plane_pos   = [self.screen_size[0]/2, self.screen_size[1]]
		self.ini_time = time.time()
		self.hardness_time = time.time()
		self.spd_time      = time.time()
		self.hardness_rate = 98 
		self.planes.spd    = 2


	# 输入事件管理
	def key_event_listen(self):
		# 事件检测
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEMOTION:
				self.planes.plane_pos = list(event.pos)

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.planes.fire()
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					self.planes.turn(5)
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					self.planes.turn(4)


	# 主循环
	def main_loop(self):
		pygame.init()	
		while True:

			# 键盘监听
			self.key_event_listen()
			# 计算更新游戏
			self.rules_control()
			
			# 屏幕渲染
			self.screen.fill(pygame.Color('white'))
			self.render()
			pygame.display.flip()
			self.clock.tick(self.FPS)
			# 在窗口上显示帧率和得分
			pygame.display.set_caption(f"Score:{self.score},  \
				Enemys:{len(self.planes.enemy_list)}, Time:{int(time.time() - self.ini_time)}, \
				FPS:{round(self.clock.get_fps(), 3)},")


def main():
	game = Plane_game()
	game.main_loop()


if __name__ == '__main__':
	main()

