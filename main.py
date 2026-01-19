import pygame as py
import random
py.init()

screen=py.display.set_mode((800,600))
run=True
score=0

bg=py.image.load('space.jpg')

py.display.set_caption("Space Invaders")
logo=py.image.load('spaceship.png')
py.display.set_icon(logo)

playerImg=py.image.load('rsz_1rsz_arcade-game.png')
plX=370
plY=480
plX_change=0
plY_change=0

enemyImg=[]
enX=[]
enY=[]
enX_change=[]
enY_change=[]
num=6
for i in range(num):
    enemyImg.append(py.image.load('rsz_monster.png'))
    enX.append(random.randint(0,736))
    enY.append(random.randint(30,150))
    enX_change.append(0.6)
    enY_change.append(30)

bullet=py.image.load('rsz_bullet.png')
bX=0
bY=480
bX_change=0
bY_change=2
b_state="ready"

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire(x,y):
    global b_state
    b_state="fire"
    screen.blit(bullet,(x+16,y+10))

font1=py.font.Font("freesansbold.ttf",60)
def game_over():
    scr=font1.render("GAME OVER",True,(255,255,255))
    screen.blit(scr,(230,250))

def collision(enemyX, enemyY, bulletX, bulletY):
    enemy_rect = enemyImg[0].get_rect(topleft=(enemyX, enemyY))
    bullet_rect = bullet.get_rect(topleft=(bulletX, bulletY))
    return enemy_rect.colliderect(bullet_rect)

clock = py.time.Clock()
start_time = py.time.get_ticks()

font=py.font.Font("freesansbold.ttf",32)
scX=10
scY=10

def get_score(x,y):
    scr=font.render("Score:"+str(score),True,(255,255,255))
    screen.blit(scr,(x,y))

#gameloop
while run:
    screen.fill((0,0,40))
    screen.blit(bg,(0,0))

    for event in py.event.get():
        if event.type==py.QUIT:
            run=False
        if event.type==py.KEYDOWN:
            if event.key==py.K_LEFT:
                plX_change=-0.8
            elif event.key==py.K_RIGHT:
                plX_change=0.8
            elif event.key==py.K_UP:
                plY_change=-0.1
            elif event.key==py.K_DOWN:
                plY_change=0.1
            elif event.key==py.K_SPACE:
                if b_state is "ready":
                    b_sound=py.mixer.Sound('laser.wav')
                    b_sound.play()
                    bX=plX
                    fire(bX,bY)
        if event.type==py.KEYUP:
            if event.key==py.K_LEFT or event.key==py.K_RIGHT:
                plX_change=0
            if event.key==py.K_UP or event.key==py.K_DOWN:
                plY_change=0

    plX+=plX_change
    #plY+=plY_change
    if plX<=0:
        plX=0
    elif plX>=736: 
        plX=736

    for i in range(num):
        enX[i]+=enX_change[i]
        if enY[i]>440:
            for j in range(num):
                enY[j]=2000
            game_over()
        if enX[i]<=0:
            enX_change[i]=0.6
            enY[i]+=enY_change[i]
        elif enX[i]>=736:
            enX_change[i]=-0.6
            enY[i]+=enY_change[i]

        if b_state is "fire":
            coll=collision(enX[i],enY[i],bX,bY)
            if coll:
                c_sound=py.mixer.Sound('explosion.wav')
                c_sound.play()
                bY=480
                b_state="ready"
                score+=1
                enX[i]=random.randint(0,736)
                enY[i]=random.randint(30,150)

        enemy(enX[i],enY[i],i)

    if bY<=0:
        bY=480
        b_state="ready"
    if b_state is "fire":
        fire(bX,bY)
        bY-=bY_change

    player(plX,plY)
    get_score(scX,scY)
    py.display.update()

