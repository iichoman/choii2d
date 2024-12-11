import time
from pico2d import *
import gfw
from . import tiledmap


class Gauge:
    def __init__(self, fg_fname, bg_fname):
        self.fg = gfw.image.load(fg_fname)
        self.bg = gfw.image.load(bg_fname)
    def draw(self, x, y, width, rate):
        l = x - width // 2
        b = y - self.bg.h // 2
        self.draw_3(self.bg, l, b, width, 3)
        self.draw_3(self.fg, l, b, round(width * rate), 3)
    def draw_3(self, img, l, b, width, edge):
        img.clip_draw_to_origin(0, 0, edge, img.h, l, b, edge, img.h)
        img.clip_draw_to_origin(edge, 0, img.w - 2 * edge, img.h, l+edge, b, width - 2 * edge, img.h)
        img.clip_draw_to_origin(img.w - edge, 0, edge, img.h, l+width-edge, b, edge, img.h)

class Sprite:
    def __init__(self, filename, x, y):
        self.filename = filename
        if filename is None:
          self.image = None
          self.width, self.height = 0, 0
        else:
          self.image = gfw.image.load(filename)
          self.width, self.height = self.image.w, self.image.h
        self.x, self.y = x, y
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass
    def get_bb(self):
        l = self.x - self.width // 2
        b = self.y - self.height // 2
        r = self.x + self.width // 2
        t = self.y + self.height // 2
        return l, b, r, t
    def __getstate__(self):
        dict = self.__dict__.copy()
        del dict['image']
        return dict
    def __setstate__(self, dict):
        self.__dict__.update(dict)
        # print(f'{self.filename=},')
        Sprite.__init__(self, self.filename, self.x, self.y)

    def __repr__(self):
        return f'{type(self).__name__}({self.filename})'

class AnimSprite(Sprite):
    def __init__(self, filename, x, y, fps, frame_count=0):
        super().__init__(filename, x, y)
        self.fps = fps
        if frame_count == 0: # 정사각형인 경우 0 을 주면 알아서 갯수를 세도록 한다
            frame_count = self.image.w // self.image.h

        if self.image is not None:
          self.width = self.image.w // frame_count
        self.frame_count = frame_count
        self.created_on = time.time()

    # elapsed time 을 구하기 위해 update() 에서 gfw.frame_time 을 누적하지 않는다
    # 그렇게 해도 되긴 하지만, 간단한 반복 애니메이션은 정확한 시간 누적이 필요한게 아니다
    # 오히려 AnimSprite 를 상속하는 객체가 super().update() 를 호출해야만 하는 부담이 생긴다
    def draw(self):
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        self.image.clip_draw(index * self.width, 0, self.width, self.height, self.x, self.y)

class ScoreSprite(Sprite):
    def __init__(self, img_file, right, y):
        super().__init__(img_file, right, y)
        self.digit_width = self.image.w // 10
        self.width = self.digit_width
        self.score = 0
        self.display = 0
    def draw(self):
        x = self.x
        score = self.display
        while score > 0:
            digit = score % 10
            sx = digit * self.digit_width
            # print(type(sx), type(digit), type(self.digit_width))
            self.image.clip_draw(sx, 0, self.digit_width, self.image.h, x, self.y)
            x -= self.digit_width
            score //= 10
    def update(self):
        diff = self.score - self.display;
        if diff == 0: return
        if -10 < diff and diff < 0:
            self.display -= 1
        elif 0 < diff and diff < 10:
            self.display += 1
        else:
            self.display += diff // 10

class Background(Sprite):
    def __init__(self, filename):
        cw, ch = get_canvas_width(), get_canvas_height()
        super().__init__(filename, cw // 2, ch // 2)
        self.width = cw
        self.height = ch

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

class VertFillBackground(Background):
    def __init__(self, filename, speed=0):
        super().__init__(filename)
        self.dest_height = self.image.h * get_canvas_width() // self.image.w
        self.speed = speed
        self.scroll = 0
    def update(self):
        self.scroll += self.speed * gfw.frame_time

    def draw(self):
        y = self.scroll % self.dest_height
        if y != 0: y -= self.dest_height
        max_y = get_canvas_height()
        while y < max_y:
            self.image.draw_to_origin(0, y, self.width, self.dest_height)
            y += self.dest_height

class ScrollBackground(Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0, 0)
        self.max_scroll_x = self.width - get_canvas_width()
        self.max_scroll_y = self.height - get_canvas_height()

    def draw(self):
        x, y = round(self.x), round(self.y)
        self.image.clip_draw_to_origin(x, y, get_canvas_width(), get_canvas_height(), 0, 0)

    def scroll(self, dx, dy):
        self.scrollTo(self.x + dx, self.y + dy)

    def scrollTo(self, x, y):
        self.x = clamp(0, x, self.max_scroll_x)
        self.y = clamp(0, y, self.max_scroll_y)

    def show(self, x, y):
        hw, hh = get_canvas_width() // 2, get_canvas_height() // 2
        self.x = clamp(0, x - hw, self.max_scroll_x)
        self.y = clamp(0, y - hh, self.max_scroll_y)

    def to_screen(self, x, y):
        return x - self.x, y - self.y

    def from_screen(self, x, y):
        return x + self.x, y + self.y

    def get_bb(self):
        return 0, 0, 0, 0

class InfiniteScrollBackground(ScrollBackground):
    def __init__(self, filename, margin=0):
        super().__init__(filename)
        self.margin = margin
    def scrollTo(self, x, y):
        self.x, self.y = x, y
    def show(self, x, y):
        cw, ch = get_canvas_width(), get_canvas_height()
        if self.margin > 0:
            if x < self.x + self.margin:
                self.x = x - self.margin
            elif x > self.x + cw - self.margin:
                self.x = x - cw + self.margin
            if y < self.y + self.margin:
                self.y = y - self.margin
            elif y > self.y + ch - self.margin:
                self.y = y - ch + self.margin
            return
        self.x = x - cw // 2
        self.y = y - ch // 2

    def draw(self):
        cw, ch = get_canvas_width(), get_canvas_height()

        # quadrant 3
        q3l = round(self.x) % self.width
        q3b = round(self.y) % self.height
        q3w = clamp(0, self.width - q3l, self.width)
        q3h = clamp(0, self.height - q3b, self.height)
        self.image.clip_draw_to_origin(q3l, q3b, q3w, q3h, 0, 0)

        # quadrant 2
        self.image.clip_draw_to_origin(q3l, 0, q3w, ch - q3h, 0, q3h)

        # quadrant 4
        self.image.clip_draw_to_origin(0, q3b, cw - q3w, q3h, q3w, 0)

        # quadrant 1
        self.image.clip_draw_to_origin(0, 0, cw - q3w, ch - q3h, q3w, q3h)

def _get_folder(filename):
    idx = filename.rfind('/')
    return '.' if idx < 0 else filename[:idx]

class MapBackground(ScrollBackground):
    def __init__(self, filename, tilesize=108, wraps=False, fitsWidth=False, fitsHeight=False, dx=0, dy=0):
        super().__init__(None)
        self.filename = filename
        self.folder = _get_folder(filename)  # 파일 경로에서 폴더명 추출
        with open(filename, 'r') as f:
            mapjson = json.load(f)  # JSON 파일을 읽어서 맵 데이터를 파싱
        self.tmap = tiledmap.map_from_dict(mapjson)  # 맵 데이터를 Map 객체로 변환

        # 모든 타일셋 이미지 로드
        for ts in self.tmap.tilesets:
            ts.tile_image = gfw.image.load(f'{self.folder}/{ts.image}')  # 타일셋 이미지 파일을 로드
            print(f"Loading tileset image: {ts.image}")

        # 화면 크기에 맞게 타일 크기를 조정할 옵션 (미사용 상태)
        if fitsWidth:
            #tilesize = math.ceil(get_canvas_width() / self.tmap.width)
            pass
        elif fitsHeight:
            #tilesize = math.ceil(get_canvas_height() / self.tmap.height)
            pass

        self.tilesize = tilesize  # 타일 크기 설정
        self.wraps = wraps  # 맵이 반복될지 여부
        self.x, self.y = 0, 0  # 맵의 초기 스크롤 위치
        self.scroll_dx, self.scroll_dy = dx, dy  # 스크롤 속도 설정
        
        # 모든 레이어를 리스트로 저장
        self.layers = self.tmap.layers

        # 첫 번째 타일셋에 대한 설정 (타일셋의 행 계산)
        #self.ts = self.tmap.tilesets[0]  # 첫 번째 타일셋
        #self.ts.rows = math.ceil(self.ts.tilecount / self.ts.columns)  # 타일셋의 세로 방향 타일 갯수 계산

        # 스크롤 한계를 설정 (맵 크기에 맞춰 스크롤을 제한)
        self.max_scroll_x = self.tmap.width * self.tilesize
        self.max_scroll_y = self.tmap.height * self.tilesize

        self.BubbleCount = 0
    def set_scroll_speed(self, dx, dy):
        """스크롤 속도를 설정하는 함수"""
        self.scroll_dx, self.scroll_dy = dx, dy
    def total_width(self):
        return self.tmap.width * self.tilesize
    def total_height(self):
        return self.tmap.height  * self.tilesize
    def update(self):
        """스크롤 속도에 맞게 스크롤 위치를 업데이트하는 함수"""
        self.x += gfw.frame_time * self.scroll_dx  # 프레임 시간에 따른 스크롤 업데이트
        self.y += gfw.frame_time * self.scroll_dy  # 프레임 시간에 따른 스크롤 업데이트
        #self.check_player_landing()
        #self.test()

    def show(self, x, y):
        hw, hh = get_canvas_width() // 2, get_canvas_height() // 2
        self.x = clamp(-500, x - hw, self.max_scroll_x)
        self.y = clamp(-9999, y - hh, self.max_scroll_y)
    
    def draw(self):
        LC, RC = 0, 0
        UC, DC = 0, 0
        BBC = 0 
        """맵을 그리는 함수. 모든 레이어를 순차적으로 그립니다."""
        cw, ch = get_canvas_width(), get_canvas_height()  # 화면 크기

        # 현재 스크롤 위치에 맞춰 시작 좌표를 계산
        sx, sy = round(self.x), -round(self.y)

        # 맵이 반복되는 경우 (wraps가 True인 경우) 스크롤 위치가 맵의 끝을 넘어가면 다시 처음으로 돌아가도록 처리
        if self.wraps:
            map_total_width = self.tmap.width * self.tilesize
            map_total_height = self.tmap.height * self.tilesize
            sx %= map_total_width
            if sx < 0:
                sx += map_total_width
            sy %= map_total_height
            if sy < 0:
                sy += map_total_width

        # 그릴 타일의 시작 위치 (타일 기준)
        tile_x = sx // self.tilesize  # 시작 타일의 x 좌표
        tile_y = sy // self.tilesize  # 시작 타일의 y 좌표

        # 화면 상에 그려질 타일의 좌측 상단 위치를 계산
        beg_x = -(sx % self.tilesize)
        beg_y = -(sy % self.tilesize)

        # 모든 레이어를 그리기 위한 반복문
        
        for layer in self.layers:
            #layer = self.layers[]
            dst_left, dst_top = beg_x, ch - beg_y  # 타일을 그릴 위치 설정
            ty = tile_y  # 타일 y 좌표 초기화
            while dst_top > 0:
                tx = tile_x  # 타일 x 좌표 초기화
                left = dst_left
                while left < cw:
                    t_index = ty * layer.width + tx  # 현재 타일의 인덱스를 계산
                    
                    if t_index >= len(layer.data):
                        t_index = 1
                    #print(t_index)
                        
                    #t_index = 600  # 현재 타일의 인덱스를 계산
                    #print(layer.name,t_index)
                    tile = layer.data[t_index]  # 해당 타일 번호를 가져옴

                    #print(layer.name, len(layer.data))
                    

                    
                    if tile == 0:  # 타일이 0이면 빈 타일이므로 스킵
                        tx += 1
                        left += self.tilesize
                        continue
                
                    # 모든 타일셋을 순차적으로 검색
                    world = gfw.top().world
                    
                    for ts in self.tmap.tilesets:
                        ts.rows = math.ceil(ts.tilecount / ts.columns)

                        # 해당 타일셋에서 타일 번호를 찾기
                        if tile >= ts.firstgid and tile < ts.firstgid + ts.tilecount:
                            if ts.tile_image is None:
                                print(f"Skipping tile {tile} due to missing tileset image.")
                                continue  # 이미지가 없는 경우 해당 타일을 건너뜀

                            sx = (tile - ts.firstgid) % ts.columns  # 타일셋에서의 x 좌표
                            sy = (tile - ts.firstgid) // ts.columns  # 타일셋에서의 y 좌표
                            src_left = ts.margin + sx * (ts.tilewidth + ts.spacing)  # 타일 이미지의 좌측 위치
                            src_botm = ts.margin + (ts.rows - sy - 1) * (ts.tileheight + ts.spacing)  # 타일 이미지의 하단 위치

                            dst_botm = dst_top - self.tilesize  # 화면 상의 타일 하단 위치
                            # 타일 그리기 (타일셋 이미지에서 해당 타일을 잘라서 화면에 그리기)

                            if layer.name == 'bubble':
                                             

                                # bubble의 초기위치 -999,-999
                                # bubble이 살아있고 bubble 타일을 찾으면 bubble의 위치를 타일 위치로 옮긴다.
                                # 몬스터도 같은방식으로 생성해볼까
                                # 몬스터는 죽어있는채로 생성(플레이어 감지가 작동하지 않도록)
                                # 몬스터와 플레이어 사이에 벽이 있으면 감지할 수 없어야 하는데.....
                                # 거리 비교해서 감지 거리를 갱신하기로 하자 
                                pass
                            else:
                                ts.tile_image.clip_draw_to_origin(
                                    src_left, src_botm, ts.tilewidth, ts.tileheight,
                                    left, dst_botm, self.tilesize, self.tilesize
                                )
                            break  # 타일셋을 찾으면 더 이상 검색하지 않음
                    #print(layer.name)
                    #if tile != 0 :  # 빈 타일이 아니면
                    
                    #monster = gfw.top().monster
                    
                    player = gfw.top().player
                    #bbs = gfw.top().bubble1
                    #bubble1 = world.objects_at(world.layer.bubble1)
                    bubble1 = gfw.top().bubble1
                    bubble2 = gfw.top().bubble2
                    bubble3 = gfw.top().bubble3
                    # bubbles를 3개로 고정하고 각각 상태를 따로 관리해야하나
                    # 지금 문제가 한번에 세개가 다 그게됨 
                    # 아마도 루프가 계속 도니까 1,2,3번 모두 act를 0으로 만드는
                    # BBC가 0이었다가 1인경우, 2인경우, 3인경우 
                    # 1이었다가 0이 되는 경우 

                    if layer.name == 'bubble':
                        #tileB = layer.data[t_index]
                        print(tile)
                        if bubble1.act == 1:
                            bubble1.x = left + player.x - 350
                            bubble1.y = dst_botm + player.y - 250
                            bubble1.act = 0
                            self.BubbleCount = 1
                        else:
                            if bubble2.act == 1:
                                bubble2.x = left + player.x - 350
                                bubble2.y = dst_botm + player.y - 250
                                bubble2.act = 0
                            else:
                                if bubble3.act == 1:
                                    bubble3.x = left + player.x - 350
                                    bubble3.y = dst_botm + player.y - 250
                                    bubble3.act = 0
                    #print(bubble1.x, bubble2.x, bubble1.y, bubble2.y)
                    #print(bubble1.act,bubble2.act,bubble3.act)
                    #if round(bubble1.x) == round(bubble2.x) and round(bubble1.y) == round(bubble2.y):
                    #    bubble2.act = 2
                    #if bubble2.x == bubble3.x and bubble2.y == bubble3.y:
                    #    bubble3.act = 1
                    #print(BBC)
                    # 방울 이거 정 안되면 하드코딩으로 해야될 듯
                    # 아니 그냥 하드코딩 하는게 더 좋을 듯 - 시간이 없음 
                 
                    
                    if layer.name == 'terrain':
                        
                        
                        # 타일 위치를 (left, dst_top)에서 시작
                        # 타일 크기는 self.tilesize

                        tl, tb, tr, tt = round(left + self.x), round(dst_top - self.tilesize + self.y), round(left + self.tilesize + self.x), round(dst_top + self.y)
                       

                        # 플레이어 타일충돌 여기에    
                        tile_bb = tl, tb, tr, tt
                        l_bb = tl, tb+5, tl, tt-5
                        b_bb = tl+5, tb, tr-5, tb
                        r_bb = tr, tb+5, tr, tt-5
                        t_bb = tl+5, tt, tr-5, tt
                        #
                        player = gfw.top().player
                        pl, pb, pr, pt = player.get_bb()
                        rpl, rpb, rpr, rpt = round(pl), round(pb), round(pr), round(pt)
                        p_bb = rpl, rpb, rpr, rpt

                        collides = gfw.collides_bb(tile_bb, p_bb)
                        lcollides = gfw.collides_bb(l_bb, p_bb)
                        bcollides = gfw.collides_bb(b_bb, p_bb)
                        rcollides = gfw.collides_bb(r_bb, p_bb)
                        tcollides = gfw.collides_bb(t_bb, p_bb)
                      
                        #gfw.draw_rectangle(left, dst_top - self.tilesize, left + self.tilesize, dst_top)
                        
                        #gfw.draw_rectangle(*tile_bb)
                        gfw.draw_rectangle(*l_bb)
                        gfw.draw_rectangle(*b_bb)
                        gfw.draw_rectangle(*r_bb)
                        gfw.draw_rectangle(*t_bb)

                        gfw.draw_rectangle(*p_bb)
                        
                        if tcollides:
                            #if player.state == 1:
                                player.Dblock = True
                                DC += 1
                                player.dy = 0
                                if rpb < tt :
                                    
                                    player.y += tt-rpb
                                #player.y = dst_top + self.y + 58 
                                
                                player.state = 0
                                #print("???")
                                #print(gfw.frame_time)
                                #gfw.draw_rectangle(left, dst_top - self.tilesize, left + self.tilesize, dst_top)
                        
                        elif rcollides:
                            player.dx = 0
                            LC += 1
                            player.Lblock = True
                            if rpb < tt:

                                if rpl < tr:
                                    player.x += tr - rpl

                        elif lcollides:
                            player.dx = 0
                            RC += 1
                            player.Rblock = True
                            if rpb < tt:

                                if rpr > tl :
                                    player.x -=  rpr - tl
                            
                        elif bcollides:
                            player.dy = 0 
                            if rpt > tb:
                                    player.y -= rpt - tb + 1
                        
                        #self.tilePlayer    # 왜 플레이어는 함수로 만들면 덜덜 떨리는거? 
                                            #일단 사용하지 않음
                        
                        self.tileMonster(tl, tb, tr, tt, RC, LC, UC, DC) # 몬스터 왜자꾸 바닥 뚫는지??
                        

                    left += self.tilesize  # 다음 타일을 그릴 위치로 이동
                    tx += 1
                    if tx >= layer.width:  # 한 줄을 다 그리면
                        if not self.wraps:  # wraps가 False이면 반복하지 않음
                            break
                        tx -= layer.width  # wraps가 True이면 다음 줄의 첫 번째 타일로 이동
                dst_top -= self.tilesize  # 화면 상의 y 좌표를 한 칸 아래로 이동
                ty += 1
                if ty >= layer.height:  # 모든 타일을 다 그렸으면
                    if not self.wraps:  # wraps가 False이면 반복하지 않음
                        break
                    ty -= layer.height  # wraps가 True이면 다시 첫 번째 줄로 돌아감
        #print(player.Lblock)
        if RC == 0:
            player.Rblock = False
        if LC == 0:
            player.Lblock = False
        if DC == 0:
            player.Dblock = False
    def tilePlayer(self, tl, tb, tr, tt, RC, LC, UC, DC):

        tile_bb = tl, tb, tr, tt
        l_bb = tl, tb+5, tl, tt-5
        b_bb = tl+5, tb, tr-5, tb
        r_bb = tr, tb+5, tr, tt-5
        t_bb = tl+5, tt, tr-5, tt
        #
        player = gfw.top().player
        pl, pb, pr, pt = player.get_bb()
        rpl, rpb, rpr, rpt = round(pl), round(pb), round(pr), round(pt)
        p_bb = rpl, rpb, rpr, rpt

        collides = gfw.collides_bb(tile_bb, p_bb)
        lcollides = gfw.collides_bb(l_bb, p_bb)
        bcollides = gfw.collides_bb(b_bb, p_bb)
        rcollides = gfw.collides_bb(r_bb, p_bb)
        tcollides = gfw.collides_bb(t_bb, p_bb)
      
        #gfw.draw_rectangle(left, dst_top - self.tilesize, left + self.tilesize, dst_top)
        
        #gfw.draw_rectangle(*tile_bb)
        gfw.draw_rectangle(*l_bb)
        gfw.draw_rectangle(*b_bb)
        gfw.draw_rectangle(*r_bb)
        gfw.draw_rectangle(*t_bb)

        gfw.draw_rectangle(*p_bb)
        
        if tcollides:
            #if player.state == 1:
                player.Dblock = True
                DC += 1
                player.dy = 0
                if rpb < tt :
                    
                    player.y += tt-rpb
                #player.y = dst_top + self.y + 58 
                
                player.state = 0
                #print("???")
                #print(gfw.frame_time)
                #gfw.draw_rectangle(left, dst_top - self.tilesize, left + self.tilesize, dst_top)
        
        elif rcollides:
            player.dx = 0
            LC += 1
            player.Lblock = True
            if rpb < tt:

                if rpl < tr:
                    player.x += tr - rpl

        elif lcollides:
            player.dx = 0
            RC += 1
            player.Rblock = True
            if rpb < tt:

                if rpr > tl :
                    player.x -=  rpr - tl
            
        elif bcollides:
            player.dy = 0 
            if rpt > tb:
                    player.y -= rpt - tb + 1   
    def tileMonster(self, tl, tb, tr, tt, RC, LC, UC, DC):
        tile_bb = tl, tb, tr, tt
        l_bb = tl, tb+5, tl, tt-5
        b_bb = tl+5, tb, tr-5, tb
        r_bb = tr, tb+5, tr, tt-5
        t_bb = tl+5, tt, tr-5, tt

        #
        #monster = gfw.top().monster
        world = gfw.top().world
        monsters = world.objects_at(world.layer.monster)
        for monster in monsters:
            pl, pb, pr, pt = monster.get_bb()
            rpl, rpb, rpr, rpt = round(pl), round(pb), round(pr), round(pt)
            p_bb = rpl, rpb, rpr, rpt

            collides = gfw.collides_bb(tile_bb, p_bb)
            lcollides = gfw.collides_bb(l_bb, p_bb)
            bcollides = gfw.collides_bb(b_bb, p_bb)
            rcollides = gfw.collides_bb(r_bb, p_bb)
            tcollides = gfw.collides_bb(t_bb, p_bb)
          
            #gfw.draw_rectangle(left, dst_top - self.tilesize, left + self.tilesize, dst_top)
            
            #gfw.draw_rectangle(*tile_bb)
            gfw.draw_rectangle(*l_bb)
            gfw.draw_rectangle(*b_bb)
            gfw.draw_rectangle(*r_bb)
            gfw.draw_rectangle(*t_bb)

            gfw.draw_rectangle(*p_bb)
            
            if tcollides:
                #if monster.state == 1:
                    monster.Dblock = True
                    DC += 1
                    monster.dy = 0
                    if rpb < tt :
                        
                        monster.y += tt-rpb
                    #monster.y = dst_top + self.y + 58 
                    
                    #monster.state = 0
                    #print("???")
                    #print(gfw.frame_time)
                    #gfw.draw_rectangle(left, dst_top - self.tilesize, left + self.tilesize, dst_top)
            
            elif rcollides:
                monster.dx = 0
                LC += 1
                monster.Lblock = True
                if rpb < tt:

                    if rpl < tr:
                        monster.x += tr - rpl

            elif lcollides:
                monster.dx = 0
                RC += 1
                monster.Rblock = True
                if rpb < tt:

                    if rpr > tl :
                        monster.x -=  rpr - tl
                
            elif bcollides:
                monster.dy = 0 
                if rpt > tb:
                        monster.y -= rpt - tb + 1   


