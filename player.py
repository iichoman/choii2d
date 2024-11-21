#------------------------------------------------------
# state:
#    0 - normal
#    1 - jump
#    2 - hurt
# 공격 범위 시간 0.5초?
# 앞 뒤 각각 0.25초 해야될듯
# 현재 필요한 것: 걷는 모션, 공격(x키), 공격 모션, 
#                기본 소지 아이템(폭탄, 로프 아이템의 사용(c키,s키 ))
#                피해입는거 hurt()? 
#                 혹은 state 변경 - monster에게 닿으면 state를 hurt로 전환, 
#                 몬스터의 공격력만큼 플레이어 체력 감소
#                몬스터 밟기 - 플레이어의 발 히트박스와 몬스터의 머리 히트박스를 추가로 만들어야 할 듯 
#------------------------------------------------------
from pico2d import *
#import random
import gfw

class Player(gfw.Sprite):
    GRAVITY = 12  # 중력 값
    JUMP_POWER = 0 # 점프 힘
    MAX_JUMP_POWER = 3

    def __init__(self):
        super().__init__('res/char/char.png', 128, 128)
        self.time = 0  # 시간 (초 단위)
        self.frame = 0
        self.frame_atk = 0
        self.dx, self.dy = 0, 0  # x, y 방향 속도
        self.speed = 500  # 기본 이동 속도
       
        self.state = 0  # (0: 기본, 1: 점프, 2: 피해, 4: dead)
        self.attack = False
        self.attack_box = (0,0,0,0)
        self.ground_y = 128  # 바닥 위치 (y=0) 수정 필요
        self.move = 0
        self.flip = ' '
        self.image_flipped = load_image('res/char/char_flip.png')

        self.hp = 4
        self.bomb = 4
        self.rope = 4

        self.at = 0

    def draw(self):
        x = self.frame * 128 + 128
        x2 = self.frame * 128
        x3 = self.frame_atk * 128
        move = self.move
        
        screen_pos = self.bg.to_screen(self.x, self.y)
       
        if self.state == 1:
            self.image.clip_composite_draw(x2, 768, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.move == 0:
            self.image.clip_composite_draw(0, 1920, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.move == 1:
            self.image.clip_composite_draw(x, 1920, 128, 128, 0, self.flip, *screen_pos, 128, 128)

        if self.attack == True:
            print("hey")
            self.image.clip_composite_draw(x3, 512, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        #draw_rectangle(*self.attack_box)
        #hw, hh = 32, 48  # 바운딩 박스 크기
        #draw_rectangle(self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10)
    def update(self):
        self.time += gfw.frame_time
        fps, frame_count = 10, 8
        self.frame = round(self.time * fps) % frame_count
        self.frame_atk = round(self.time * fps) % 6

        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time

        # 중력 처리
        if self.state == 1: 
            self.dy -= self.GRAVITY * gfw.frame_time

            #self.y -= self.GRAVITY

        # 착지 수정필요
        if self.y <= self.ground_y:
            self.y = self.ground_y  
            self.state = 0  
        
        self.bg.show(self.x, self.y)
        
        #test code here

        if self.attack == True:
            self.at += 1
            print(self.at)
            if(self.at > 100): 
                self.attack = False
                self.at = 0

        self.attack_box = (self.x + 32, self.y - 10, self.x + 32 + 30, self.y + 10)
        print(self.x,", ",self.y)
        
    def adjust_delta(self, x, y):
        self.dx += x
        self.dy += y
        if self.dx == 0:
            self.move = 0

    def handle_event(self, e):
        dx, dy = self.dx, self.dy
        if e.type == SDL_KEYDOWN:
            
            if e.key == SDLK_LEFT:
                self.time = 0    
                self.adjust_delta(-1, 0)
                self.move = 1
                self.flip = 'h'
            elif e.key == SDLK_RIGHT:
                self.time = 0 
                self.adjust_delta(1, 0)
                self.move = 1
                self.flip = ' '
            elif e.key == SDLK_LSHIFT:
                self.speed = 300
            elif e.key == SDLK_z:  
                self.time = 0
            
                self.JUMP_POWER = 3   
                self.jump()
            elif e.key == SDLK_x:
                self.time = 0
                self.attackk()

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:    
                self.adjust_delta(1, 0)
               
                
            elif e.key == SDLK_RIGHT: 
                self.adjust_delta(-1, 0)
                
                
            elif e.key == SDLK_LSHIFT:
                self.speed = 500

            elif e.key == SDLK_z:
                if(self.dy > 0):
                    self.dy *= 0.5

    def jump(self): 
        if self.state == 0:  
            self.state = 1  
            self.dy = self.JUMP_POWER  

    def attackk(self):
        self.attack = True

    def set_state(self, state):
        self.state = state

    def get_bb(self):
        hw, hh = 32, 48  # 바운딩 박스 크기
        return self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10

    def attack_box(self):
        def get_bb(self):
            return self.x + hw, self.y - 10, self.x + hw + 30, self.y + 10

    def __repr__(self):
        return 'Player'
