#------------------------------------------------------
# state:
#    0 - normal
#    1 - jump
#    2 - hurt(stunned)
#    3 - dead
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
    FRICTION = 10 # 마찰력
    JUMP_POWER = 0 # 점프 힘
    MAX_JUMP_POWER = 3

    def __init__(self):
        super().__init__('res/char/char.png', 300, 500)
        self.time_move = 0  # 시간 (초 단위)
        self.time_atk = 0
        self.time_jump = 0
        self.frame = 0
        self.frame_move = 0
        self.frame_atk = 0
        self.frame_jump = 0
        self.dx, self.dy = 0, 0  # x, y 방향 속도

        self.speed = 500  # 기본 이동 속도
        self.Lblock = False
        self.Rblock = False
        self.state = 0  # (0: 기본, 1: 점프, 2: 피해, 3: 스턴, 4: dead)

        self.LeftToggles = False
        self.RightToggles = False
       #self.stand = 0  -   # 평소에 stand = 1, 
                            # 엎드리거나 stun 되어 누웠을때 stand = 0
        self.stun_time = 0
                            
        self.attack = False
        #self.attack_box = (0,0,0,0)
        #self.ground_y = 128  # 바닥 위치 (y=0) 수정 필요
        self.ground_y = float('-inf')
        self.on_grounds = False
        #self.foot = self.y - 58

        self.move = 0
        self.flip = ' '
        self.image_flipped = load_image('res/char/char_flip.png')

        self.hp = 4
        self.bomb = 4
        self.rope = 4

        self.whip_x = 0
        self.whip_y = 0

        self.stop = False
    def draw(self):
        frame_move = self.frame_move * 128 + 128
        frame_jump = self.frame_jump * 128
        frame_atk = self.frame_atk * 128
        #move = self.move
        
        screen_pos = self.bg.to_screen(self.x, self.y)

        if self.attack == True:
            # 채찍 그리기
            self.image.clip_composite_draw(frame_atk + 1280, 384, 128, 128, 0, self.flip, self.whip_x, self.whip_y, 96, 96)
            # 공격 모션
            self.image.clip_composite_draw(frame_atk, 1408, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.state == 1:
            self.image.clip_composite_draw(frame_jump, 768, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.move == 0:
            self.image.clip_composite_draw(0, 1920, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.move == 1:
            self.image.clip_composite_draw(frame_move, 1920, 128, 128, 0, self.flip, *screen_pos, 128, 128)

        # 공격박스 그리기 테스트
        draw_rectangle(*self.get_draw_atk_bb())
        
    def update(self):
        
        #print(self.state)
        if self.dy == 0 and self.dx == 0:
            self.move = 0
        else:
            self.move = 1
        self.time_move += gfw.frame_time
        self.time_jump += gfw.frame_time
        self.time_atk += gfw.frame_time

        fps = 10

        self.frame_move = round(self.time_move * fps*2) % 8

        self.frame_jump = round(self.time_jump * fps) % 8

        if self.attack == True:
            self.frame_atk = round(self.time_atk * fps*1.5) % 7
        self.dx = 0

        if self.RightToggles:
            self.dx = 1.5
        if self.LeftToggles:
            self.dx = -1.5
        
        
        self.x += self.dx * self.speed * gfw.frame_time 
        self.y += self.dy * self.speed * gfw.frame_time

        # 중력 처리  
        #if self.state != 0:
        self.dy -= self.GRAVITY * gfw.frame_time

        if self.dy != 0:
            self.state = 1
            
     
        #print(self.frame_jump)

        # 죽음
        if 0 >= self.hp:
            self.state = 4

        #마찰력 처리
        if self.state == 3 or self.state == 4:
            self.stun_time += gfw.frame_time
            if self.state == 3 and self.stun_time >= 5:
                self.state = 0
                self.stun_time = 0
            if 0.05 >= self.dx and self.dx >= -0.05:
            #if self.dx == 0:
                self.dx = 0
            elif self.dx > 0:
                self.dx -= self.FRICTION * gfw.frame_time
            elif self.dx < 0:
                self.dx += self.FRICTION * gfw.frame_time
        
        # 착지 수정필요
        #if self.y <= self.ground_y:
            #self.y = self.ground_y  
            #self.state = 0  
        
        self.bg.show(self.x, self.y)
        
       

        # 방향(flip)
        if not self.attack:
            if self.dx > 0:
                self.flip = ' '
            elif self.dx < 0:
                self.flip = 'h'
        if self.attack == True:
            if(self.frame_atk == 6 ): 
                self.attack = False

                self.frame_atk = 0
  

        self.attack_box = (self.x + 32, self.y - 10, self.x + 32 + 30, self.y + 10)

        # 채찍xy
        sx, sy = self.bg.to_screen(self.x, self.y)
        if(self.attack == True):
            if(self.flip == ' '):
                if(2 >= self.frame_atk):
                    self.whip_x = sx - 64
                    self.whip_y = sy + 32
                elif(self.frame_atk == 3):
                    self.whip_x = sx + 32
                    self.whip_y = sy + 24
                elif(self.frame_atk > 3):
                    self.whip_x = sx + 64
                    self.whip_y = sy - 32

            elif(self.flip == 'h'):
                if(2 >= self.frame_atk):
                    self.whip_x = sx + 64
                    self.whip_y = sy + 32
                elif(self.frame_atk == 3):
                    self.whip_x = sx - 32
                    self.whip_y = sy + 24
                elif(self.frame_atk > 3):
                    self.whip_x = sx - 64
                    self.whip_y = sy - 32
        #else:
            #self.whip_x = -999
            #self.whip_y = -999

        #test code here
        #print(self.x,", ",self.y)
        #print(self.frame_atk)                   
        #print (self.whip_x,", ",self.whip_y)
    def adjust_delta(self, x, y):
        if not self.stop:
            self.dx += x
        self.dy += y


    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            
            if e.key == SDLK_LEFT:
                self.LeftToggles = True
            elif e.key == SDLK_RIGHT: 
                self.RightToggles = True
            elif e.key == SDLK_LSHIFT:
                self.speed = 300
            elif e.key == SDLK_z:  
                
                self.JUMP_POWER = 3
                self.jump()
            elif e.key == SDLK_x:
                if(self.attack == False):
                    self.time_atk = 0
                    self.attack = True

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:   
                self.LeftToggles = False

            elif e.key == SDLK_RIGHT: 
                self.RightToggles = False
                

            elif e.key == SDLK_LSHIFT:
                self.speed = 500

            elif e.key == SDLK_z:
                if(self.dy > 0):
                    self.dy *= 0.5

    def jump(self): 
        self.ground_y = float('-inf')
        if self.state == 0:
            self.time_jump = 0  
            self.state = 1  
            self.dy = self.JUMP_POWER  

    def set_state(self, state):
        self.state = state

    def get_bb(self):
        hw, hh = 32, 48  # 바운딩 박스 크기
        return self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10
    def get_atk_bb(self):
        bw,bh = 48,32
        fw,fh = 48,24
        if self.attack == True:
            if self.flip == ' ':
                if 3 >= self.frame_atk:
                    return self.x - bw - 64, self.y - bh + 32, self.x + bw - 64, self.y + bh + 32
                elif self.frame_atk > 3:
                    return self.x - fw + 64, self.y - fh - 24, self.x + fw + 64, self.y + fh - 24
            else:
                if 3 >= self.frame_atk:
                    return self.x - bw + 64, self.y - bh + 32, self.x + bw + 64, self.y + bh + 32
                elif self.frame_atk > 3:
                    return self.x - fw - 64, self.y - fh - 24, self.x + fw - 64, self.y + fh - 24    
        else: 
            return 0,0,0,0
    def get_draw_atk_bb(self):
        bw,bh = 48,32
        fw,fh = 48,24
        sx, sy = self.bg.to_screen(self.x, self.y)
        if self.attack == True:
            if self.flip == ' ':
                if 3 >= self.frame_atk:
                    return sx - bw - 64, sy - bh + 32, sx + bw - 64, sy + bh + 32
                elif self.frame_atk > 3:
                    return sx - fw + 64, sy - fh - 24, sx + fw + 64, sy + fh - 24
            else:
                if 3 >= self.frame_atk:
                    return sx - bw + 64, sy - bh + 32, sx + bw + 64, sy + bh + 32
                elif self.frame_atk > 3:
                    return sx - fw - 64, sy - fh - 24, sx + fw - 64, sy + fh - 24
                return 0,0,0,0
            #return self.x - hw - 32, self.y - hh, self.x + hw - 32, self.y + hh
        else: 
            return 0,0,0,0

    def __repr__(self):
        return 'Player'
