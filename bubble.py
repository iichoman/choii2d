from pico2d import *
import gfw
import random
import os 

class Bubble(gfw.Sprite):
	def __init__(self):
		#x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
		x, y = 300, 300
		super().__init__('res/temp/items.png',x,y)
		self.act = 1
		self.cnt = 0
	def draw(self):
		play = gfw.top()
		screen_pos = play.bg.to_screen(self.x, self.y)

		self.image.clip_draw(128*11, 128*1, 128,128, *screen_pos)
	def update(self):
		print(self.cnt)
		# 충돌체크
		# 플레이어가 밟거나 채찍에 맞으면 깨짐
		# Door와 상호작용하여 3개가 터지면 Door가 열려야 함
		pass
	def get_bb(self):
		hw, hh = 32, 32  # 바운딩 박스 크기
		return self.x - hw, self.y - hh, self.x + hw, self.y + hh

