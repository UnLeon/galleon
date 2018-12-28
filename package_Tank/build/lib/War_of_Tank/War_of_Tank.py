# -*- encoding = utf-8 -*-
import pygame
import time
import sys
import toel
from pygame.locals import *     # pygame常量
from random import randint

difficulty = 0  # 默认难度


class TankMenue(object):       # 游戏开始界面
    width = 1080
    height = 600
    time_wait = 0
    break_key = False
    menue_rect = [(810, 10), (810, 590), (1070, 590), (1070, 10)]

    def mainMenue(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height), 0, 32)   # 设定屏幕大小，类型(0,RESIZEABLE,FULLSCREEN),32位
        pygame.display.set_caption("坦克大战")      # 设置窗口标题
        while True:
            screen.fill((0, 0, 0))  # color of RGB 填充背景色
            screen.blit(self.write_text()[0], (150, 145))       # draw one image onto another
            for i, text in enumerate(self.write_text1(), 0):             # 显示菜单文字
                screen.blit(text, (820, 20 + i*40))       # draw one image onto another
            if self.time_wait < 50:                             # Enter image blink
                screen.blit(self.write_text()[1], (150, 345))       # draw one image onto another
            elif self.time_wait == 100:
                self.time_wait = 0
            self.time_wait += 1
            pygame.draw.lines(screen, (255, 255, 255), True, self.menue_rect, 1)
            self.get_event(screen)
            if self.break_key:
                TankMain().startGame(screen)
                self.break_key = False
                # return screen
            pygame.display.update()

    def get_event(self, screen):
        global difficulty
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    self.break_key = True
                if event.key == pygame.K_BACKSPACE:
                    TankMain.wave = 0
                if event.key == K_0:        # 调整难度
                    difficulty = 0
                if event.key == K_1:        # 调整难度
                    difficulty = 1
                if event.key == K_2:        # 调整难度
                    difficulty = 2

    def write_text(self):
        font = pygame.font.SysFont("华文楷体", 100)
        text_sf = font.render("War of Tank", True, (255, 0, 0))     # 文字，平滑锯齿,颜色
        font1 = pygame.font.SysFont("华文楷体", 30)
        text_sf1 = font1.render("        ——按ENTER进入游戏——", True, (255, 255, 0))     # 文字，平滑锯齿,颜色
        return text_sf, text_sf1

    def write_text1(self):
        global difficulty
        font = pygame.font.SysFont("华文楷体", 25)
        font1 = pygame.font.SysFont("华文楷体", 20)
        text_sf = font1.render("欢迎来到坦克世界测试版", True, (255, 0, 0))     # 文字，平滑锯齿,颜色
        text_sf1 = font1.render("(测试版就是会有很多bug)", True, (88,87,86))     # 文字，平滑锯齿,颜色
        text_sf2 = font.render("调整难度请按数字0-2", True, (255, 255, 0))     # 文字，平滑锯齿,颜色
        text_sf3 = font.render("当前难度：%d" % difficulty, True, (255, 255, 0))     # 文字，平滑锯齿,颜色
        return text_sf, text_sf1, text_sf2, text_sf3


class TankMain(object):
    game_rect = [(10, 10), (10, 590), (800, 590), (800, 10)]
    game_rect_l = game_rect[0][0]
    game_rect_u = game_rect[0][1]
    game_rect_d = game_rect[1][1]
    game_rect_r = game_rect[2][0]
    tank_rect = [560, 360]
    my_Tank_missile_list = []
    my_Tank = None
    enemy_list = pygame.sprite.Group()
    enemy_missile_list = pygame.sprite.Group()
    explode_list = []
    wave = -1
    wall_list = pygame.sprite.Group()

    def __init__(self):
        self.return_sig = False

    def startGame(self, screen):
        if not TankMain.my_Tank:
            TankMain.my_Tank = My_Tank(screen, self.tank_rect[0], self.tank_rect[1])        # 创建我方坦克
        TankMain.my_Tank.move_sig = 0
        wall1 = Wall(screen, (self.game_rect_l + 190), (self.game_rect_u + 100), 400, 10)   # 创建墙
        self.wall_list.add(wall1)
        while True:
            if len(self.enemy_list) == 0:
                TankMain.wave += 1
                for i in range(1, randint(6, 9)):  # 创建敌方坦克
                    self.enemy_list.add(Enemy_Tank(screen))

            screen.fill((0, 0, 0))  # color of RGB 填充背景色
            pygame.draw.lines(screen, (255, 255, 255), True, TankMenue.menue_rect, 1)
            pygame.draw.lines(screen, (255, 255, 255), True, self.game_rect, 1)
            for i, text in enumerate(self.write_text(), 0):             # 显示菜单文字
                screen.blit(text, (820, 20 + i*40))       # draw one image onto another

            self.get_event(self.my_Tank, screen)
            for wall in self.wall_list:
                wall.display()
            if self.my_Tank.live:               # 显示我方坦克
                self.my_Tank.display()
                self.my_Tank.tank_move()
                self.my_Tank.hit_wall()
            for enemy in self.enemy_list:       # 显示敌方坦克
                if enemy.live:
                    enemy.display()
                    enemy.random_move()
                    enemy.hit_wall()
                    enemy.random_fire()
                else:
                    self.enemy_list.remove(enemy)

            for mm in self.my_Tank_missile_list:        # 显示我方炮弹
                if mm.live:
                    mm.display()
                    mm.missile_move()
                    mm.hit_tank()
                    mm.hit_wall()
                else:
                    self.my_Tank_missile_list.remove(mm)
            for em in self.enemy_missile_list:          # 显示敌方炮弹
                if em.live:
                    em.display()
                    em.missile_move()
                    em.hit_tank()
                    em.hit_wall()
                else:
                    self.enemy_missile_list.remove(em)

            for ex in self.explode_list:
                if ex.live:
                    ex.display()
                else:
                    self.explode_list.remove(ex)

            if self.return_sig:
                break
            time.sleep(0.008)
            pygame.display.update()

    def get_event(self, my_Tank, screen):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_sig = True
                    # sys.exit()
                if event.key == K_SPACE:
                    if my_Tank.live:
                        m = my_Tank.fire()
                        m.own = "player"
                        self.my_Tank_missile_list.append(my_Tank.fire())
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    my_Tank.direction = "U"
                    my_Tank.move_sig += 1
                if event.key == pygame.K_DOWN:
                    my_Tank.direction = "D"
                    my_Tank.move_sig += 1
                if event.key == pygame.K_LEFT:
                    my_Tank.direction = "L"
                    my_Tank.move_sig += 1
                if event.key == pygame.K_RIGHT:
                    my_Tank.direction = "R"
                    my_Tank.move_sig += 1
                if event.key == pygame.K_r and not my_Tank.live:
                    TankMain.my_Tank.live = Tank.live
                if event.key == pygame.K_RETURN and not my_Tank.live:
                    TankMain.my_Tank = My_Tank(screen, self.tank_rect[0], self.tank_rect[1])  # 创建我方坦克
                    TankMain.my_Tank.live = Tank.live
                    self.wave = 0
            if event.type == pygame.KEYUP:
                if my_Tank.move_sig > 0 and (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    my_Tank.move_sig -= 1

    def write_text(self):
        font = pygame.font.SysFont("华文楷体", 25)
        text_sf = font.render("已消灭敌方坦克群：%d" % TankMain.wave, True, (255, 0, 0))     # 文字，平滑锯齿,颜色
        text_sf1 = font.render("敌方坦克数量：%d" % len(self.enemy_list), True, (255, 255, 0))     # 文字，平滑锯齿,颜色
        text_sf2 = font.render("我方炮弹数量：%d" % len(self.my_Tank_missile_list), True, (255, 255, 0))     # 文字，平滑锯齿,颜色
        text_sf3 = font.render("我方坦克生命：%d" % TankMain.my_Tank.live, True, (255, 255, 0))     # 文字，平滑锯齿,颜色
        return text_sf, text_sf1, text_sf2, text_sf3


class BaseItem(pygame.sprite.Sprite):
    image = None
    images = dict()
    direction = None
    rect = None

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

    def display(self):
        self.image = self.images[self.direction]
        self.screen.blit(self.image, self.rect)


class Tank(BaseItem):
    # 定义类属性，所有对象拥有的公共属性
    images = []
    image = None
    tank_own = "mine"
    move_sig = 0
    tank_speed = 1
    live = 6

    def __init__(self, screen, left, top):
        super().__init__(screen)
        self.live = Tank.live
        self.direction = "U"
        self.tank_image("01")
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left

    def tank_image(self, sig):
        self.images = dict()
        self.images["U"] = pygame.image.load("image\\tank\image" + sig + "_U.gif")
        self.images["D"] = pygame.image.load("image\\tank\image" + sig + "_D.gif")
        self.images["L"] = pygame.image.load("image\\tank\image" + sig + "_L.gif")
        self.images["R"] = pygame.image.load("image\\tank\image" + sig + "_R.gif")
        self.image = self.images[self.direction]

    def tank_move(self):
        self.size = self.image.get_size()
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if self.move_sig:
            if self.direction == "U" and self.rect.top > TankMain.game_rect_u:
                self.rect.top -= self.tank_speed
            if self.direction == "D" and self.rect.top < TankMain.game_rect_d - self.size[1]:
                self.rect.top += self.tank_speed
            if self.direction == "L" and self.rect.left > TankMain.game_rect_l:
                self.rect.left -= self.tank_speed
            if self.direction == "R" and self.rect.left < TankMain.game_rect_r - self.size[0]:
                self.rect.left += self.tank_speed

    def fire(self):
        m = Missile(self.screen, self)
        return m

    def hit_wall(self):
        hit_event = pygame.sprite.spritecollide(self, TankMain.wall_list, False)
        if hit_event:
            # TankMain.my_Tank.move_sig = 0
            self.rect.left = self.oldleft
            self.rect.top = self.oldtop


class My_Tank(Tank):

    def __init__(self, screen, left, top):
        super().__init__(screen, left, top)
        self.tank_speed = 2
        global difficulty
        if difficulty == 0:
            self.live = Tank.live
        elif difficulty == 1:
            self.live = Tank.live - 2
        elif difficulty == 2:
            self.live = Tank.live - 4
        else:
            self.live = 999

    def fire(self):
        m = Missile(self.screen, self)
        m.own = "player"
        return m


class Enemy_Tank(Tank):
    global difficulty

    def __init__(self, screen):
        super().__init__(screen, randint(1, 15)*50, TankMain.game_rect_u+5)
        self.tank_own = "enemy"
        self.tank_image("01")
        self.step = randint(80, 200)
        self.random_direction()
        self.tank_speed = TankMain.wave + 1

    def random_direction(self):
        m = randint(0, 4)
        if m == 4:
            self.move_sig = 0
        elif m == 3:
            self.direction = "U"
            self.move_sig = 1
        elif m == 2:
            self.direction = "D"
            self.move_sig = 1
        elif m == 1:
            self.direction = "L"
            self.move_sig = 1
        elif m == 0:
            self.direction = "R"
            self.move_sig = 1

    def random_move(self):
        if self.step == 0:
            self.random_direction()
            self.step = randint(80, 200)
        else:
            self.tank_move()
            self.step -= 1

    def random_fire(self):
        if difficulty == 1:
            f = randint(0, 810)
        elif difficulty == 2:
            f = randint(0, 820)
        else:
            f = randint(0, 800)
        if f >= 790:
            m = self.fire()
            # m.own = "enemy"   默认设置
            TankMain.enemy_missile_list.add(m)
        else:
            return


class Missile(BaseItem):
    image = None

    def __init__(self, screen, tank):
        super().__init__(screen)
        self.own = "enemy"
        self.tank = tank
        self.live = True
        if self.own == "enemy":
            self.speed = TankMain.wave + 4
        else:
            self.speed = 5
        self.direction = tank.direction
        self.images = dict()
        self.missile_image("01")
        self.size = self.image.get_size()
        self.width = self.size[0]
        self.height = self.size[1]
        self.rect = self.image.get_rect()
        self.rect.top = tank.rect.top + (tank.size[1] - self.height)/2
        self.rect.left = tank.rect.left + (tank.size[0] - self.width)//2

    def missile_image(self, sig):
        self.images["U"] = pygame.image.load("image\\missile\missile" + sig + "_U.gif")
        self.images["D"] = pygame.image.load("image\\missile\missile" + sig + "_D.gif")
        self.images["L"] = pygame.image.load("image\\missile\missile" + sig + "_L.gif")
        self.images["R"] = pygame.image.load("image\\missile\missile" + sig + "_R.gif")
        self.image = self.images[self.direction]

    def missile_move(self):
        self.size = self.image.get_size()
        if self.live:
            if self.direction == "U":
                if self.rect.top > TankMain.game_rect_u:
                    self.rect.top -= self.speed
                else:
                    self.live = False
            if self.direction == "D":
                if self.rect.top < TankMain.game_rect_d - self.size[1]:
                    self.rect.top += self.speed
                else:
                    self.live = False
            if self.direction == "L":
                if self.rect.left > TankMain.game_rect_l:
                    self.rect.left -= self.speed
                else:
                    self.live = False
            if self.direction == "R":
                if self.rect.left < TankMain.game_rect_r - self.size[0]:
                    self.rect.left += self.speed
                else:
                    self.live = False

    def hit_tank(self):
        if self.own == "player":        # 我方炮弹击中敌方
            hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_list, False)
            for enemy in hit_list:
                enemy.live = False
                self.live = False
                explode = Explode(self.screen, enemy.rect)      # 产生爆炸效果
                TankMain.explode_list.append(explode)
        elif self.own == "enemy":       # 敌方炮弹击中我方
            if TankMain.my_Tank.live:
                hit_event = pygame.sprite.collide_rect(self, TankMain.my_Tank)
                if hit_event:
                    TankMain.my_Tank.live -= 1
                    self.live = False
                    explode = Explode(self.screen, TankMain.my_Tank.rect)
                    TankMain.explode_list.append(explode)

    def hit_wall(self):
        hit_event = pygame.sprite.spritecollide(self, TankMain.wall_list, False)
        if hit_event:
            self.live = False


class Explode(BaseItem):

    def __init__(self, screen, rect):
        super().__init__(screen)
        self.live = True
        self.rect = rect
        self.images = [pygame.image.load("image\\missile\explode.gif"),
                       pygame.image.load("image\\missile\explode.gif")]
        self.step = 0

    def display(self):
        if self.live:
            if self.step == 10:       # 最后一张图片显示了
                self.live = False
            else:
                if self.step <= 5:
                    self.image = self.images[0]
                else:
                    self.image = self.images[1]
                self.image = pygame.transform.scale(self.image, ((20+self.step*5), (20+self.step*5)))
                self.screen.blit(self.image, self.rect)
                self.step += 1
        else:
            pass
            # pygame.transform.scale(Surface, (width, height), DestSurface=None)(缩放)
            # pygame.transform.rotate(Surface, angle)(旋转)
            # pygame.transform.flip(Surface, xbool, ybool)(水平和垂直翻转)，xbool = > True为水平翻转，ybool = > True为垂直翻转


class Wall(BaseItem):

    def __init__(self, screen, left, top, width, height):
        super().__init__(screen)
        self.rect = Rect(left, top, width, height)
        self.color = (255, 255, 255)
        self.hit_event = False

    def display(self):
        self.screen.fill(self.color, self.rect, True)


if __name__ == "__main__":
    try:
        toel.AutoBackup("H:\Learn\Project", "G:\Projects")
    except Exception:
        try:
            toel.AutoBackup("I:\Learn\Project", "D:\Projects")
        except Exception:
            pass
TankMenue().mainMenue()
