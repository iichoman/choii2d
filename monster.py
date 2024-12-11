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
        
    def update(self):
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
            self.dy -= self.GRAVITY * gfw.frame_time


        # 사망
        elif self.state == 0:
            self.dx = 0 # dead
        #print(self.hp)
        self.check_collision_with_whip()
        self.sense_player()
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
        if collides:
            self.stun()
            if player.x < self.x:
                self.dx = 3
            else:
                self.dx = -3

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
    def get_bb(self):
        hw, hh = 32, 48  # 바운딩 박스 크기
        return self.x - hw, self.y - hh - 10, self.x + hw, self.y + hh - 10
    # monster의 방향이 player를 향하고 y좌표가 같으며 player와의 거리가 감지dist 이하일때
    # 10초 동안 보고있는 방향으로 돌진한다.
    # 벽을 만나면 방향을 전환한다.
    # 아이템을 만나면 넘어진다.
class Bat(gfw.Sprite):
    pass
class Spider(gfw.Sprite):
    pass
class Sonic(gfw.Sprite):
    pass
    # 플레이어 발견시 상태를 돌진으로 하고 개빨리 굴러감,
    # 벽에 부딪힐 떄 까지 구른다
    # 구르기 상태에서 부닺힌 객체는 스턴, 데미지, 위로 튕김 ㅇㅇ
    # 몬스터 종류마다 충돌시 y값 튀는 정도를 다르게 설정하면 좋을 듯 

# 각 객체들을 몬스터로 추상화하기:
    # hp 뭐 그런거 등등 상속 
    # 행동패턴 추상화
    # 플레이어 한테 밟히는거도 상속 - 이거 빨리 만들어야함!!! 
    # 플레이어 클래스에서 playerfootbox 만들고 foot박스랑 몬스터 위쪽 좌표(left rigt top)
    # 충돌 시 플레이어 약간 점프 (dy값을 변경해야함 가산하면 안됨) 

