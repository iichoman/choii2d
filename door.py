#door.py
# 바운딩 박스만 가지면 된다 ㅇㅇ 
from pico2d import *
import gfw
import random


class Door(gfw.Sprite):
	def __init__(self):
		super().__init__('res/temp/items.png',-999,-999)
		self.enter = 0
		self.enter_count = 0
		self.next = 0
		self.bub = 0
	def draw(self):
		pass
	def update(self):
		player = gfw.top().player
		collides = gfw.collides_box(player, self)
		if collides:
			if player.bubbles >= 3:
				self.enter = 1
		else:
			self.enter = 0
		if self.enter == 1:
			#player.x = self.x
			#self.enter_count += gfw.frame_time
			#if self.enter_count == 2:
				#gfw.push(stage2)
			
			# 플레이어가 땅에 닿아있을떄만 드가야함
			player.go_to_door= True
		
	def check_collision_with_player(self):
		pass
	def get_bb(self):
		hw, hh = 52, 52  # 바운딩 박스 크기
		return self.x - hw, self.y - hh, self.x + hw, self.y + hh
