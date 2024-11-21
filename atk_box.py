from pico2d import *
import gfw
import player

class Atk_box(gfw.Sprite):
	def __init__(self):
		super().__init__('res/char/char.png', -999, -999)
		
	def update(self):
		pass