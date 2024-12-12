from pico2d import * 
from gfw import *
from player import Player
from monster import Monster, Bat, Spider, Sonic, Arrow
from door import Door 
from bubble import Bubble
from interface import Interface

import nextstage2
import gameover
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
#canvas_width = 1920
#canvas_height = 1680
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
    bg = gfw.MapBackground('res/cave1-2.json')
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

    player = Player(x = 3880, y = 380)
    #player = Player()
    player.bg = bg
    world.append(player, world.layer.player)


    # 방울도 이거처럼 x, y값 하드코딩하면 되기는 함 ㅇㅇ  

    world.append(Monster(x=513, y=265), world.layer.monster)
    world.append(Monster(x=564, y=-490), world.layer.monster)
    world.append(Monster(x=2107, y=-490), world.layer.monster)
    #world.append(Monster(x=3911, y=-1470), world.layer.monster)
    #world.append(Monster(x=3290, y=-800), world.layer.monster)
    #world.append(Monster(x=2434, y=-1750), world.layer.monster)

    world.append(Bat(x=2400, y=640), world.layer.monster)
    world.append(Bat(x=1893, y=-430), world.layer.monster)
    world.append(Bat(x=2323, y=-1600), world.layer.monster)
    #world.append(Bat(x=3320, y=-495), world.layer.monster)
    #world.append(Bat(x=3300, y=-1750), world.layer.monster)
    #world.append(Bat(x=1680, y=-1550), world.layer.monster)

    # 거미 
    world.append(Spider(x=850, y=270), world.layer.monster)
    world.append(Spider(x=2650, y=-240), world.layer.monster)
    world.append(Spider(x=3400, y=-1750), world.layer.monster)
    world.append(Spider(x=1200, y=-1300), world.layer.monster)

    world.append(Sonic(x=2745, y=500), world.layer.monster)
    world.append(Sonic(x=1142, y=-490), world.layer.monster)
    world.append(Sonic(x=338, y=-1350), world.layer.monster)
    
    world.append(Arrow(x=1465, y= -490), world.layer.monster)
    world.append(Arrow(x=2800, y= -1500), world.layer.monster)
    world.append(Arrow(x=1899, y= -1630), world.layer.monster)
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
        elif e.key == SDLK_p:
            gfw.push(stage2)
    if player.hp <= 0:
        gfw.push(gameover)
    if player.next_stage == True:
        gfw.push(nextstage2)
    player.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

