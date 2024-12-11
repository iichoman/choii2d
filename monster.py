from pico2d import *
import random
import gfw

class Monster(gfw.Sprite):
    GRAVITY = 12  # 중력 값
    FRICTION = 10
    def __init__(self, x = None, y = None):
        super().__init__('res/mobs/monstersbasic02.png', 500, 100)
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

        self.time = 0
        self.frame = 0
        self.dx, self.dy = 0, 0  # x, y 방향 이동
        self.speed = 300
        self.hp = 3
        self.damage = 1
        self.flip = 'h'
        self.state = 0          # 0정지 1이동 2돌진 3스턴 4사망

        self.Dblock = 0
        self.Ublock = 0
        self.Lblock = 0
        self.Rblock = 0
        #self.stand = 0  -   # 평소에 stand = 1, 
                            # 엎드리거나 stun 되어 누웠을때 stand = 0

        self.stun_time = 0
    def draw(self):
        play = gfw.top()
        screen_pos = play.bg.to_screen(self.x, self.y)
        

        #정지
        if self.state == 0: 
            self.image.clip_composite_draw(0, 1280, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        
        #이동
        elif self.state == 1:
            pass
        
        #돌진
        elif self.state == 2:
            self.image.clip_composite_draw(self.run_frame, 128*9, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        
        #스턴
        elif self.state == 3:
            self.image.clip_composite_draw(128*11, 1280, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        elif self.state == 4:
            self.image.clip_composite_draw(128*11, 1280, 128, 128, 0, self.flip, *screen_pos, 128, 128)
        
    def update(self):
        if self.dx >= 108:
            self.dx = 107
        if self.dy >= 108:
            self.dy = 107
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        self.time += gfw.frame_time

        fps = 10
        self.run_frame = round(self.time * fps*2) % 8 * 128

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
        
        # 타일 충돌 
        if not self.Dblock:
            player = gfw.top().player
            if player.x - 640 <= self.x and self.x <= player.x + 640 and player.y - 480 <= self.y <= player.y + 480:
                self.dy -= self.GRAVITY * gfw.frame_time
            else:
                self.dy = 0


        # 사망
        elif self.state == 0:
            self.dx = 0 # dead
        #print(self.hp)
        self.check_collision_with_whip()
        self.sense_player()
        if self.hp > 0:
            self.check_collision_with_player()

    
    def check_collision_with_player(self):
        player = gfw.top().player
        collides = gfw.collides_box(player, self)
        if collides:
            if self.state != 3:
                player.hurt(obj = self)
            #self.state = 3


    def check_collision_with_whip(self):
        player = gfw.top().player
        collides = gfw.collides_whip(player.get_atk_bb(), self)
        collides_H = gfw.collides_whip(self.get_bb_head(), player)
        if collides:
            self.stun()
            if player.x < self.x:
                self.dx = 3
            else:
                self.dx = -3
        elif collides_H:
            if player.invincible == False and self.state != 3 and self.state != 4:
                self.stun()
                if player.x < self.x:
                    self.dx = 3
                else:
                    self.dx = -3
                player.dy = 2

    def sense_player(self):
        player = gfw.top().player
        #print(self.y, round(player.y))
        if player.y <= self.y+48 and self.y-48 <= player.y :
            if self.state == 0 or self.state == 1:
                if player.x < self.x and self.flip == 'h':
                    if self.x - player.x < 500:
                        print('??')
                        self.run()
                elif self.x < player.x and self.flip == ' ':
                    if player.x - self.x < 500:
                        print('?')
                        self.run()

    def run(self):
        self.state = 2
        self.speed = 500
        if self.flip == ' ':
            self.dx = 1
        else:
            self.dx = -1
    def stun(self):
        player = gfw.top().player
        if self.state != 3:
            self.state = 3
            self.hurt()

    def hurt(self):
        self.hp -= 1
    def get_bb_head(self):
        hw, hh = 32, 48  # 바운딩 박스 크기
        return self.x - hw + 10, self.y + hh - 10, self.x + hw - 10, self.y + hh 
    def get_bb(self):
        hw, hh = 32, 48  # 바운딩 박스 크기
        return self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10
    # monster의 방향이 player를 향하고 y좌표가 같으며 player와의 거리가 감지dist 이하일때
    # 10초 동안 보고있는 방향으로 돌진한다.
    # 벽을 만나면 방향을 전환한다.
    # 아이템을 만나면 넘어진다.

class Bat(gfw.Sprite):
    def __init__(self, x = None, y = None):
        super().__init__('res/mobs/monstersbasic01.png', 500, 100)
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

        self.time = 0
        self.frame = 0
        self.dx, self.dy = 0, 0  # x, y 방향 이동
        self.speed = 300
        self.hp = 1
        self.damage = 1
        self.flip = 'h'
        self.state = 0          # 0정지 1이동 2돌진 3스턴 4사망

        self.Dblock = 0
        self.Ublock = 0
        self.Lblock = 0
        self.Rblock = 0

        self.fly_frame = 0
        #self.stand = 0  -   # 평소에 stand = 1, 
                            # 엎드리거나 stun 되어 누웠을때 stand = 0

    def draw(self):
        play = gfw.top()
        screen_pos = play.bg.to_screen(self.x, self.y)
        if self.hp <= 0:
            pass
        elif self.state == 0:
            self.image.clip_composite_draw(128*6, 128*15, 128, 128, 0, self.flip, *screen_pos, 100, 100)
        elif self.state == 1:
            self.image.clip_composite_draw(self.fly_frame + 128 * 6, 128*14, 128, 128, 0, self.flip, *screen_pos, 100, 100)
        pass
    def update(self):

        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        self.time += gfw.frame_time
        fps = 10
        self.fly_frame = round(self.time * fps*2) % 6 * 128

        player = gfw.top().player
        if player.y <= self.y:
            self.state = 1
        if self.state == 1:
            self.attack()
        if self.hp > 0:
            self.check_collision_with_whip()
            self.check_collision_with_player()
        if self.hp <= 0:
            self.x = 99999
    def attack(self):
        player = gfw.top().player
        if player.x - 640 <= self.x and self.x <= player.x + 640 and player.y - 480 <= self.y <= player.y + 480:
            if player.y >= self.y:
                self.dy = 1
            else:
                self.dy = -1
            if player.x >= self.x:
                self.flip = ' '
                self.dx = 1
            else:
                self.flip = 'h'
                self.dx = -1
    def get_bb(self):
        hw, hh = 24, 24  # 바운딩 박스 크기
        return self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10

    def get_bb_head(self):
        hw, hh = 24, 24  # 바운딩 박스 크기
        return self.x - hw + 10, self.y + hh - 10, self.x + hw - 10, self.y + hh 

    def check_collision_with_player(self):
        player = gfw.top().player
        collides = gfw.collides_box(player, self)
        if collides:
            if self.state != 3:
                player.hurt(obj = self)
            #self.state = 3


    def check_collision_with_whip(self):
        player = gfw.top().player
        collides = gfw.collides_whip(player.get_atk_bb(), self)
        collides_H = gfw.collides_whip(self.get_bb_head(), player)
        if collides:
            self.hp -= 1
            if player.x < self.x:
                self.dx = 3
            else:
                self.dx = -3
        elif collides_H:
            if player.invincible == False and self.state != 3 and self.state != 4:
                self.hp -= 1
                if player.x < self.x:
                    self.dx = 3
                else:
                    self.dx = -3
                player.dy = 2

class Spider(gfw.Sprite):
    GRAVITY = 12
    def __init__(self, x = None, y = None):
        super().__init__('res/mobs/monstersbasic01.png', 500, 100)
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

        self.time = 0
        self.fall_time = 0
        self.frame = 0
        self.dx, self.dy = 0, 0  # x, y 방향 이동
        self.speed = 300
        self.hp = 1
        self.damage = 1
        self.flip = 'h'
        self.state = 0          # 0정지 1이동 2돌진 3스턴 4사망

        self.Dblock = 0
        self.Ublock = 0
        self.Lblock = 0
        self.Rblock = 0
        self.turn = False

        self.jump = 0
        self.JUMP_T = 0
        #self.stand = 0  -   # 평소에 stand = 1, 
                            # 엎드리거나 stun 되어 누웠을때 stand = 0

    def draw(self):
        play = gfw.top()
        screen_pos = play.bg.to_screen(self.x, self.y)
        if self.hp <= 0:
            pass
        elif self.state == 0:
            self.image.clip_composite_draw(128*8, 128*12, 128, 128, 0, self.flip, *screen_pos, 100, 100)
        elif self.state == 1:
            self.image.clip_composite_draw(self.fall_frame + 128*8, 128*12, 128, 128, 0, self.flip, *screen_pos, 100, 100)
            pass
        elif self.state == 2:
            self.image.clip_composite_draw(128*0, 128*12, 128, 128, 0, self.flip, *screen_pos, 100, 100)
        pass
    def update(self):

        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        
        fps = 10
        if not self.turn:
            self.fall_frame = round(self.fall_time * fps) % 5 * 128
        self.jump_frame = round(self.time * fps*2) % 4 * 128
        player = gfw.top().player
        if player.y <= self.y and self.x - 20 <= player.x and player.x <= self.x + 20:
            self.time = 0
            self.state = 1
        if self.state == 1:
            if not self.turn:
                self.fall_time += gfw.frame_time
            
            self.fall()
            #print(self.dy)
            

        if self.fall_frame == 512:
            self.turn = True
        print(self.dy)
        if -0.1 <= self.dy and self.dy <= 0.1 and self.turn == True:
                self.state = 2

        if self.state == 2:
            self.jump = 1
            self.attack()
            if player.x - 640 <= self.x and self.x <= player.x + 640 and player.y - 480 <= self.y <= player.y + 480:
                self.dy -= self.GRAVITY * gfw.frame_time
            if -0.1 <= self.dy and self.dy <= 0.1:
                self.dx = 0
        if self.hp > 0:
            self.check_collision_with_whip()
            self.check_collision_with_player()
        if self.hp <= 0:
            self.x = 99999
    def fall(self):
 
        if not self.Dblock:
            player = gfw.top().player
            if player.x - 640 <= self.x and self.x <= player.x + 640 and player.y - 480 <= self.y <= player.y + 480:
                self.dy -= self.GRAVITY * gfw.frame_time
            else:
                self.dy = 0
            #self.state = 2
    def attack(self):
        player = gfw.top().player
        if player.x - 640 <= self.x and self.x <= player.x + 640 and player.y - 480 <= self.y <= player.y + 480:
            
            if self.jump == 1:
                self.JUMP_T += gfw.frame_time
                if self.JUMP_T >= 2:
                    self.y += 5
                    self.dy = 3
                    if player.x >= self.x:
                        self.flip = ' '
                        self.dx = 3
                    else:
                        self.flip = 'h'
                        self.dx = -3
                    self.jump = 0
                    self.JUMP_T = 0

            
    def get_bb(self):
        hw, hh = 24, 24  # 바운딩 박스 크기
        return self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10

    def get_bb_head(self):
        hw, hh = 24, 24  # 바운딩 박스 크기
        return self.x - hw + 10, self.y + hh - 10, self.x + hw - 10, self.y + hh 

    def check_collision_with_player(self):
        player = gfw.top().player
        collides = gfw.collides_box(player, self)
        if collides:
            if self.state != 3:
                player.hurt(obj = self)
            #self.state = 3


    def check_collision_with_whip(self):
        player = gfw.top().player
        collides = gfw.collides_whip(player.get_atk_bb(), self)
        collides_H = gfw.collides_whip(self.get_bb_head(), player)
        if collides:
            self.hp -= 1
            if player.x < self.x:
                self.dx = 3
            else:
                self.dx = -3
        elif collides_H:
            if player.invincible == False and self.state != 3 and self.state != 4:
                self.hp -= 1
                if player.x < self.x:
                    self.dx = 3
                else:
                    self.dx = -3
                player.dy = 2
class Sonic(gfw.Sprite):
    pass
    # 플레이어 발견시 상태를 돌진으로 하고 개빨리 굴러감,
    # 벽에 부딪힐 떄 까지 구른다
    # 구르기 상태에서 부닺힌 객체는 스턴, 데미지, 위로 튕김 ㅇㅇ
    # 몬스터 종류마다 충돌시 y값 튀는 정도를 다르게 설정하면 좋을 듯 ?? dho



