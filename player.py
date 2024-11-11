from pico2d import *
#import random
import gfw
#Boy
class Player(gfw.Sprite):
    GRAVITY = 12  # 중력 값
    JUMP_POWER = 0 # 점프 힘
    MAX_JUMP_POWER = 3
    def __init__(self):
        super().__init__('res/char/char.png', 128, 128)
        self.time = 0  # 시간 (초 단위)
        self.frame = 0
        self.dx, self.dy = 0, 0  # x, y 방향 속도
        self.speed = 500  # 기본 이동 속도
       
        self.state = 0  # (0: 기본, 1: 점프, 2: 피해)
        self.attack = 0
        self.attack_box = 0, 0, 0, 0
        self.ground_y = 128  # 바닥 위치 (y=0) 수정 필요
        self.move = 0
        self.flip = ' '
        self.image_flipped = load_image('res/char/char_flip.png')
    def draw(self):
        x = self.frame * 128 + 128
        x2 = self.frame * 128
        move = self.move
        
        screen_pos = self.bg.to_screen(self.x, self.y)
       
        if self.state == 1:
            self.image.clip_composite_draw(x2, 768, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.move == 0:
            self.image.clip_composite_draw(0, 1920, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.move == 1:
            self.image.clip_composite_draw(x, 1920, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        

    def update(self):
        self.time += gfw.frame_time
        fps, frame_count = 10, 8
        self.frame = round(self.time * fps) % frame_count

        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        
        # 중력 처리
        if self.state == 1: 
            self.dy -= self.GRAVITY * gfw.frame_time
        
        # 착지 수정필요
        if self.y <= self.ground_y:
            self.y = self.ground_y  
            self.state = 0  
            
        
        self.bg.show(self.x, self.y)

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
                while(self.JUMP_POWER < self.MAX_JUMP_POWER):
                    self.JUMP_POWER += 0.1      # 점프키 누른 정도에 따라 점프높이 증가 (마리오)

                self.jump()
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:    
                self.adjust_delta(1, 0)
               
                
            elif e.key == SDLK_RIGHT: 
                self.adjust_delta(-1, 0)
                
                
            elif e.key == SDLK_LSHIFT:
                self.speed = 500

    def jump(self):
        if self.state == 0:  
            self.state = 1  
            self.dy = self.JUMP_POWER  

    def attack(self):
        self.attack = 1
        self.attack_box = self.x + hw, self.y - 10, self.x + hw + 30, self.y + 10

    def set_state(self, state):
        self.state = state

    def get_bb(self):
        hw, hh = 32, 48  # 바운딩 박스 크기
        return self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10

    def __repr__(self):
        return 'Player'
