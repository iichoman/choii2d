from pico2d import *
import gfw
import player

class Atk_box(gfw.Sprite):
	def __init__(self):
		super().__init__('res/char/char.png', 32, 32)
	def draw(self):
		pass
	def update(self):
		pass
	def get_bb(self):
		return 0,0,500,500
