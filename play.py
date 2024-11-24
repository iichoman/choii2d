from pico2d import * 
from gfw import *
from player import Player
from monster import Monster

# map test
#from settings import *
#from level import Level
#level = Level(level_data, surface)

world = World(['bg', 'player', 'monster'])

canvas_width = 1920
canvas_height = 1080
#canvas_width = 1280
#canvas_height = 960
shows_bounding_box = True
shows_object_count = True

def enter():
    global bg, player

    loaded = world.load(' ')
    print(f'{loaded=} world object count={world.count()}')
    if loaded: # world.count() > 0:
        player = list(world.objects_at(world.layer.player))[0]
        bg = player.bg
        world.bg = bg
        return
    
    bg = gfw.MapBackground('res/earth3.json', fitsWidth=True, fitsHeight=True)
    #bg = ScrollBackground('res/maps/ttt.png')
    
    world.append(bg, world.layer.bg)
    world.bg = bg    

    player = Player()
    player.bg = bg
    world.append(player, world.layer.player)

    monster = Monster()
    monster.bg = bg
    world.append(monster, world.layer.monster)
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

