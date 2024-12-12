from pico2d import *
import gfw
import random
import os 

class Bubble(gfw.Sprite):
	def __init__(self, x=None, y=None):
	#x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
		self.xn =0
		self.yn =0
		if x is not None:
	 		self.xn = x
		if y is not None:
	 		self.yn = y
		super().__init__('res/temp/items.png',300,300)
		self.act = 1
		self.cnt = 0
		self.hp = 1
	def draw(self):
		play = gfw.top()
		screen_pos = play.bg.to_screen(self.x, self.y)

		if self.hp > 0: self.image.clip_draw(128*11, 128*1, 128,128, *screen_pos)
	def update(self):
		if self.hp > 0: 
			self.x = self.xn
			self. y = self.yn
			self.check_collision_with_whip()
			self.check_collision_with_player()
		#print(self.act)
		# 충돌체크
		# 플레이어가 밟거나 채찍에 맞으면 깨짐
		# Door와 상호작용하여 3개가 터지면 Door가 열려야 함
		pass
	def check_collision_with_player(self):
		player = gfw.top().player
		collides = gfw.collides_box(player, self)
		if collides: 
			player.stun = 1
	def check_collision_with_whip(self):
		player = gfw.top().player
		collides = gfw.collides_whip(player.get_atk_bb(), self)


		if collides:
			player.bubbles += 1
			self.hp  -= 1
			self.x = - 9999
	def get_bb(self):
		hw, hh = 32, 32  # 바운딩 박스 크기
		return self.x - hw, self.y - hh, self.x + hw, self.y + hh

