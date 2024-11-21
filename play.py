from pico2d import * 
from gfw import *
from player import Player
from atk_box import Atk_box

world = World(['bg', 'player', 'atk_box'])

canvas_width = 1024
canvas_height = 768
#canvas_width = 1280
#canvas_height = 960
shows_bounding_box = False
shows_object_count = True

def enter():
    global bg, player, atk_box

    #bg = ScrollBackground('res/maps/bg_cave.png')
    bg = ScrollBackground('res/maps/ttt.png')
    
    world.append(bg, world.layer.bg)
    world.bg = bg    

    player = Player()
    player.bg = bg
    world.append(player, world.layer.player)

    atk_box = Atk_box()
    atk_box.bg = bg 
    world.append(atk_box, world.layer.atk_box)
    # test
    
def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_1:
            print(world.objects)
            return
        elif e.key == SDLK_2:
            shows_bounding_box = True
            #if shows_bounding_box == False: 
            #    shows_bounding_box = True
            #else: 
            #    shows_bounding_box = False
    

    player.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

