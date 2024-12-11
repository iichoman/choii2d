from pico2d import *

import gfw
class Interface(gfw.Sprite):
	def __init__(self, h):
		super().__init__('res/texture/hud.png',100,100)
		self.h = h

	def draw(self):
		player = gfw.top().player
		self.image.clip_draw(64*0,64*4,64,64, 0+70*1, self.h - 50)
		self.image.clip_draw(64*2,64*6,64,64, 0+70*2, self.h - 50)
		self.image.clip_draw(64*3,64*6,64,64, 0+70*3, self.h - 50)
		gfw._system_font.draw(90 + 64*0, self.h - 65, str(player.hp),(255,255,255))
		gfw._system_font.draw(90 + 64*1, self.h - 65, str(player.bomb),(255,255,255))
		gfw._system_font.draw(90 + 64*2, self.h - 65, str(player.rope),(255,255,255))