from pico2d import *
import gfw
import play 

world = gfw.World(['menu'])

def enter():
	#world.append(menu())
	pass
def exit():
    world.clear()
    print('[main.exit()]')

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')
def handle_event(e):
	if e.type == SDL_KEYDOWN:
		if e.key == SDLK_RETURN:
			gfw.push(play)

if __name__ == '__main__':
    gfw.start_main_module()
