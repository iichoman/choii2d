from pico2d import * 
from gfw import *
from player import Player
from monster import Monster
from door import Door 
from bubble import Bubble
from interface import Interface
# map test
#from settings import *
#from level import Level
#level = Level(level_data, surface)

world = World(['bg', 'player', 'monster', 'HUD', 'door', 'bubble', 
    'bubble1', 'bubble2', 'bubble3', 'trap', 'test'])

#canvas_width = 800
#canvas_height = 600
canvas_width = 1280
canvas_height = 960
shows_bounding_box = True
shows_object_count = True

def enter():
    global bg, player, monster, door, bubble, bubble1, bubble2, bubble3, trap

    global test     #test layer

    loaded = world.load(' ')
    print(f'{loaded=} world object count={world.count()}')
    if loaded: # wohi = 0 rld.count() > 0:
        player = list(world.objects_at(world.layer.player))[0]
        bg = player.bg
        world.bg = bg
        return
    #bg = gfw.MapBackground2('res/desert.tmj', fitsWidth=False, fitsHeight=False)
    bg = gfw.MapBackground('res/cave1-2.json', fitsWidth=False, fitsHeight=False)
    #bg = ScrollBackground('res/maps/ttt.png')
    
    world.append(bg, world.layer.bg)
    world.bg = bg    

    #for i in rzange(1):
    #    world.append(Bubble(), world.layer.bubble)
    #    world.append(Bubble(), world.layer.bubble)
    #       world.append(Bubble(), world.layer.bubble)
    
    world.append(Bubble(), world.layer.bubble)
    world.append(Bubble(), world.layer.bubble)
    world.append(Bubble(), world.layer.bubble)

    door = Door()
    door.bg = bg
    world.append(door, world.layer.door)

    bubble1 = Bubble()
    bubble1.bg = bg 
    world.append(bubble1, world.layer.bubble1)

    bubble2 = Bubble()
    bubble2.bg = bg 
    world.append(bubble2, world.layer.bubble2)

    bubble3 = Bubble()
    bubble3.bg = bg 
    world.append(bubble3, world.layer.bubble3)

    player = Player(x = 500, y = 500)
    #player = Player()
    player.bg = bg
    world.append(player, world.layer.player)

    # 몬스터 생성 그냥 랜덤하게? 흠..
    # 방울도 이거처럼 x, y값 하드코딩하면 되기는 함 ㅇㅇ  
    #world.append(Monster(x=700, y=500), world.layer.monster)
    #world.append(Monster(x=900, y=500), world.layer.monster)
    #world.append(Monster(x=800, y=500), world.layer.monster)
    
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

