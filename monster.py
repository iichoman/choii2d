from pico2d import *
import random
import gfw

class Monster(gfw.Sprite):
	def __init__(self):
		super().__init__('res/mobs/monsters01.png', 128, 128)
        self.time = 0  # 시간 (초 단위)
        self.frame = 0
        self.dx, self.dy = 0, 0  # x, y 방향 이동
        self.speed = 300
        self.hp = 3
        self.damage = 1
        self.flip = random.randint(0,1)
        self.state = 0

    def update:
        

    # monster의 방향이 player를 향하고 y좌표가 같으며 player와의 거리가 감지dist 이하일때
    # 10초 동안 보고있는 방향으로 돌진한다.
    # 벽을 만나면 방향을 전환한다.
    # 아이템을 만나면 넘어진다.
    