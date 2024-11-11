from pico2d import * 
from gfw import *
from player import Player


world = World(['bg', 'player'])

#canvas_width = 1024
#canvas_height = 768
canvas_width = 1280
canvas_height = 960
shows_bounding_box = True
shows_object_count = True

def enter():
    global bg, player

   

    #bg = ScrollBackground('res/maps/bg_cave.png')
    bg = ScrollBackground('res/maps/ttt.png')
    
    world.append(bg, world.layer.bg)
    world.bg = bg    

    player = Player()
    player.bg = bg
    world.append(player, world.layer.player)

def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return

    player.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

