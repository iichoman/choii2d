#stage4.py
#stage3.py
from pico2d import * 
from gfw import *
from player import Player
from monster import Monster, Bat, Spider, Sonic, Arrow
from door import Door 
from bubble import Bubble
from interface import Interface
import gameover
import nextstage
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
        player.cosmic = 1
        bg = player.bg
        world.bg = bg
        return
    #bg = gfw.MapBackground2('res/desert.tmj', fitsWidth=False, fitsHeight=False)
    bg = gfw.MapBackground('res/cosmic-1.json')
    #bg = ScrollBackground('res/maps/ttt.png')
    
    world.append(bg, world.layer.bg)
    world.bg = bg    

    #for i in rzange(1):
    #    world.append(Bubble(), world.layer.bubble)
    #    world.append(Bubble(), world.layer.bubble)
    #       world.append(Bubble(), world.layer.bubble)
    
    #world.append(Bubble(x=2110,y=-2430), world.layer.bubble)
    #world.append(Bubble(), world.layer.bubble)
    #0000000000world.append(Bubble(), world.layer.bubble)

    door = Door()
    door.bg = bg
    door.bub = 3
    world.append(door, world.layer.door)

    bubble1 = Bubble(x=2550, y= -1850)
    bubble1.bg = bg 
    world.append(bubble1, world.layer.bubble1)

    bubble2 = Bubble(x=2855, y=2970)
    bubble2.bg = bg 
    world.append(bubble2, world.layer.bubble2)

    bubble3 = Bubble(x=5050, y=-2090)
    bubble3.bg = bg 
    world.append(bubble3, world.layer.bubble3)

    player = Player(x = 2110, y = -2000)
    #player = Player()
    player.bg = bg
    world.append(player, world.layer.player)

    # 몬스터 생성 그냥 랜덤하게?
    # 방울도 이거처럼 x, y값 하드코딩하면 되기는 함 ㅇㅇ  

    world.append(Monster(x=1804, y=-810), world.layer.monster)
    #world.append(Monster(x=564, y=-490), world.layer.monster)
    #world.append(Monster(x=2300, y=-810), world.layer.monster)
    #world.append(Monster(x=3911, y=-1470), world.layer.monster)
    #world.append(Monster(x=3290, y=-800), world.layer.monster)
    #world.append(Monster(x=2434, y=-1750), world.layer.monster)

    world.append(Bat(x=4378, y=-1900), world.layer.monster)
    world.append(Bat(x=4480, y=-2300), world.layer.monster)
    #world.append(Bat(x=3320, y=-495), world.layer.monster)
    #world.append(Bat(x=3300, y=-1750), world.layer.monster)
    #world.append(Bat(x=1680, y=-1550), world.layer.monster)

    # 거미 
    world.append(Spider(x=2430, y=960), world.layer.monster)
    world.append(Spider(x=3946, y=-2060), world.layer.monster)
    #world.append(Spider(x=3400, y=-1750), world.layer.monster)
    #world.append(Spider(x=1990, y=-1550), world.layer.monster)

    world.append(Sonic(x=1584, y=-3000), world.layer.monster)
    world.append(Sonic(x=3892, y=-1100), world.layer.monster)
    world.append(Sonic(x=2761, y=-2200), world.layer.monster)
    world.append(Sonic(x=5249, y=-2800), world.layer.monster)
    #world.append(Arrow(x=1780, y=-2650), world.layer.monster)
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
    player.cosmic = 1
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

    if player.next_stage == True:
        gfw.push(nextstage)
    player.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

