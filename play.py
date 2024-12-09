from pico2d import * 
from gfw import *
from player import Player
from monster import Monster
from bubble import Bubble
from interface import Interface
# map test
#from settings import *
#from level import Level
#level = Level(level_data, surface)

world = World(['bg', 'player', 'monster', 'HUD', 'bubble'])

canvas_width = 800
canvas_height = 600
#canvas_width = 1280
#canvas_height = 960
shows_bounding_box = True
shows_object_count = True

def enter():
    global bg, player, monster, bubble

    loaded = world.load(' ')
    print(f'{loaded=} world object count={world.count()}')
    if loaded: # wohi = 0 rld.count() > 0:
        player = list(world.objects_at(world.layer.player))[0]
        bg = player.bg
        world.bg = bg
        return
    #bg = gfw.MapBackground2('res/desert.tmj', fitsWidth=False, fitsHeight=False)
    bg = gfw.MapBackground('res/cave1-1.json', fitsWidth=False, fitsHeight=False)
    #bg = ScrollBackground('res/maps/ttt.png')
    
    world.append(bg, world.layer.bg)
    world.bg = bg    

    #for i in range(1):
    #    world.append(Bubble(), world.layer.bubble)
    #    world.append(Bubble(), world.layer.bubble)
    #       world.append(Bubble(), world.layer.bubble)
    
    world.append(Bubble(), world.layer.bubble)
    world.append(Bubble(), world.layer.bubble)
    world.append(Bubble(), world.layer.bubble)
    
    player = Player()
    player.bg = bg
    world.append(player, world.layer.player)

    monster = Monster()
    monster.bg = bg
    world.append(monster, world.layer.monster)
    # test
    HUD = Interface(h = canvas_height)
    HUD.bg = bg 
    world.append(HUD, world.layer.HUD)
    
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

