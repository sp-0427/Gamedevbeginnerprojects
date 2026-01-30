import pygame
from sys import exit
from random import choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        p1 = pygame.image.load('assets/images/player1.png').convert_alpha()
        p2 = pygame.image.load('assets/images/player2.png').convert_alpha()
        self.p = [p1,p2]
        self.p_index = 0
        self.image = self.p[self.p_index]
        self.rect = self.image.get_rect(midbottom = (100,400))
        self.keys = pygame.key.get_pressed()

    def input(self):
        if keys[pygame.K_a]:
            self.rect.x -= 2.9
            self.p_index = 0
        self.image = self.p[self.p_index]
        if keys[pygame.K_d]:
            self.rect.x += 2.9
            self.p_index = 1
        self.image = self.p[self.p_index]

    def wall_collide(self):
        if self.rect.right > 600 :
            self.rect.right = 600
        if self.rect.left < 0:
            self.rect.left = 0

    def reset(self):
        if keys[pygame.K_r]:
            self.image = self.p[self.p_index]
            self.rect = self.image.get_rect(midbottom = (100,400))
        if mous[0]:
            if r_rect.collidepoint(mouse_pos):
                self.image = self.p[self.p_index]
                self.rect = self.image.get_rect(midbottom = (100,400))

    def update(self):
        self.input()
        self.wall_collide()
        self.reset()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,tree):
        super().__init__()
        self.image = pygame.image.load('assets/images/apple.png').convert_alpha()
        self.grav = 0
        self.y_pos = 90
        self.rect = self.image.get_rect(midbottom = (90,self.y_pos))
        t1 = 90
        t2 = 240
        t3 = 390
        t4 = 540
        if tree == t1:
            self.rect = self.image.get_rect(midbottom = (t1,self.y_pos))
        if tree == t2:
            self.rect = self.image.get_rect(midbottom = (t2,self.y_pos))
        if tree == t3:
            self.rect = self.image.get_rect(midbottom = (t3,self.y_pos))
        if tree == t4:
            self.rect = self.image.get_rect(midbottom = (t4,self.y_pos))

    def anime_state(self):
        self.grav += 0.02
        self.rect.y += self.grav
    
    def destroy(self):
        if self.rect.y > 350:
            self.kill()

    def update(self):
        self.anime_state()
        self.destroy()

p = False
class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/images/pausebg.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))

score = 0
def disp_score():
    global score
    ap = pygame.image.load('assets/images/applesc.png').convert_alpha()
    ap_rect = ap.get_rect(topright = (500,10))
    screen.blit(ap,ap_rect)
    score_surf = txt_font.render(f' {score}',True,(0,0,0))
    score_rect = score_surf.get_rect(topright = (550,5))
    screen.blit(score_surf,score_rect)
    collide = pygame.sprite.spritecollide(player.sprite, obstacle, True)
    for block in collide:
        score += 1

pygame.init()

pygame.display.set_caption('Apple Catch')

game = 1

#text & font
txt_font = pygame.font.Font('assets/font/JMH Typewriter-Bold.ttf',40)

screen = pygame.display.set_mode((600,400))
im = pygame.image.load('assets/images/Bg.png')

#home screen
pl = pygame.image.load('assets/images/player2.png').convert_alpha()
play_rect = pl.get_rect(center = (300,200))

#title
title = txt_font.render('Apple Catch',True,(140,0,25))
title_rect = title.get_rect(center = (300,80))

#start
re = txt_font.render('Press SPACE to start',True,(140,0,25))
re_rect = re.get_rect(center = (300,330))

#continue
con = txt_font.render('CONTINUE (C)',True,(140,0,25))
con_rect = con.get_rect(center = (300,130))

#restart
r = txt_font.render('RESTART (R)',True,(140,0,25))
r_rect = r.get_rect(center = (300,210))

#quit
qu = txt_font.render('QUIT (Q)',True,(140,0,25))
qu_rect = qu.get_rect(center = (300,290))

#pause
paus = pygame.image.load('assets/images/pause.png').convert_alpha()
paus_rect = paus.get_rect(topleft = (10,10))

#game state for now
game_active = False

#group
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.GroupSingle()

pause = pygame.sprite.GroupSingle()
pause.add(Pause())

def restart():
    obstacle.empty()

#obs timer
a_catch = pygame.USEREVENT+1
pygame.time.set_timer(a_catch,900)

#tree's x
t1 = 90
t2 = 240
t3 = 390
t4 = 540

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == a_catch:
            obstacle.add(Obstacle(choice([t1,t2,t3,t4])))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                p = True
            if p == True:
                if event.key == pygame.K_c:
                    p = False
                if event.key == pygame.K_q:
                    exit()
                if event.key == pygame.K_r:
                    game = 0
                    score = 0
                    restart()
            else:
                game_active

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if paus_rect.collidepoint(event.pos):
                p = True
                pause.draw(screen)
                pause.update()
            if con_rect.collidepoint(event.pos):
                p = False
            if qu_rect.collidepoint(event.pos):
                exit()
            if r_rect.collidepoint(event.pos):
                game = 0
                score = 0
                restart()

        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True

    screen.blit(im,(0,0))
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if game == 0:
        game = 1
        p = False

    mous = pygame.mouse.get_pressed()

    if game_active:
        screen.blit(paus,paus_rect)
        player.draw(screen)
        if p == True:
            pause.draw(screen)
            pause.update()
            screen.blit(con,con_rect)
            screen.blit(r,r_rect)
            screen.blit(qu,qu_rect)

        else:
            player.update()
            obstacle.draw(screen)
            obstacle.update()
        scre = disp_score()
        

    else:
        screen.fill((209,255,107))
        screen.blit(title,title_rect)
        screen.blit(pl,play_rect)
        screen.blit(re,re_rect)

    pygame.display.update()