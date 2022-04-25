import pygame
import random

pygame.init()

background_Sound = pygame.mixer.Sound("Background.wav")
effect_gun_Sound = pygame.mixer.Sound("Gun.wav")
Redzone_war_Sound = pygame.mixer.Sound("Redzone_war.wav")
effect_gun_Sound.set_volume(0.5)
background_Sound.play(-1)



screen_width = 640
screen_height = 512

screen = pygame.display.set_mode((screen_width, screen_height)) #디스플레이 설정

pygame.display.set_caption("테스트") #게임 제목

background = pygame.image.load("background.png") #이미지 로드

char_sprite = [pygame.image.load("char1.png"),pygame.image.load("char2.png")]
char_attack_sprite = [pygame.image.load("char_Attack1.png"),pygame.image.load("char_Attack2.png")]
wall_sprite = [pygame.image.load("wall1.png")]
Redzone_w_sprite = [pygame.image.load("redzone-warning.png")]
boom_sprite = [pygame.image.load("boom1.png"),pygame.image.load("boom2.png"),pygame.image.load("boom3.png")]

clock = pygame.time.Clock()

a = char_sprite[0].get_size()

charX = (screen_width/2)-(a[0]/2)
charY = (screen_height/2)-(a[1]/2)

move_X = 0 #움직이는 방향
move_Y = 0 #움직이는 방향
check = [0,0,0,0,0] #누르고 있는 중

Vspeed = 4
chr_s_num = 0
fps = 1

shot_list = []
del_shot_list = []
shotFPS = 0

#올라가는 벽
wall_FPS = 0
wall_list = []

#레드존 공격
RedZone_FPS = 0
RedZone_list = []
redzone_war = False
redzone_Boom = False
attackX,attackY = [0,0]





animation_FP = 0

def anime(A):
    for i in range(10):
        if i%2 == 0 or i == 0:
            if (A*i) < fps < (A*(i+1)):  # 주인공 애니메이션
                animation_FP = 0
                return animation_FP
    else:
        animation_FP = 1
        return animation_FP

def shooting(A):
    global shotFPS

    if check[4] == 1:
        if shotFPS == 15:
            effect_gun_Sound.play()
            shotFPS = 1
        if shotFPS == 1:
            effect_gun_Sound.play()
            shot_list.append([charX, charY])
        shotFPS += 1

    for i in range(len(shot_list)):
        shot_list[i][1] += A
        if not shot_list[i][1] > screen_height:
            screen.blit(char_attack_sprite[animation_FP], (shot_list[i][0], shot_list[i][1]))
        else:
            del_shot_list.append(shot_list[i])

    for i in range(len(shot_list)):
        if collision_check(shot_list[i][0], shot_list[i][1], wall_list) == True:
            del_shot_list.append(shot_list[i])

    if not shot_list == []:
        for i in range(len(del_shot_list)):
            try:
                shot_list.remove(del_shot_list[i])
                del_shot_list.remove(del_shot_list[i])
            except:
                try:
                    del_shot_list.remove(del_shot_list[i])
                except:
                    return


def wall_move(A,B,C):
    global wall_FPS

    wall_random_junbok = []
    wall_FPS += 1

    Re = 0

    for i in range(C):
        if wall_FPS == A:
            RD = random.randint(0, 9)

            while RD in wall_random_junbok:
                RD = random.randint(0, 9)

            wall_random_junbok.append(RD)

            wall_list.append([RD*64, screen_height])
            screen.blit(wall_sprite[0], (wall_list[len(wall_list)-1][0], wall_list[len(wall_list)-1][1]))
            Re += 1
        if C == Re:
            wall_FPS = 0

    if not wall_list == []:
        for i in range(len(wall_list)):
            wall_list[i][1] -= B
            screen.blit(wall_sprite[0], (wall_list[i][0], wall_list[i][1]))

        for i in range(C):
            if wall_list[i][1] < -64:
                del wall_list[i]

def RedZone(A,B):
    global RedZone_FPS
    global redzone_war
    global redzone_Boom
    global attackX,attackY

    if redzone_war == False:
        if RedZone_FPS == A:
            H = random.randint(1, 8)
            V = random.randint(1, 6)
            attackX,attackY = [H*64,V*64]
            redzone_war = True
            RedZone_FPS = 0
            Redzone_war_Sound.play()
        else:
            RedZone_FPS += 1

    attack_list = [[attackX, attackY], [attackX + 64, attackY], [attackX - 64, attackY], [attackX, attackY + 64]
        , [attackX, attackY - 64], [attackX + 64, attackY + 64], [attackX - 64, attackY - 64],
                   [attackX + 64, attackY - 64], [attackX - 64, attackY + 64], [attackX + 128, attackY],
                   [attackX, attackY + 128], [attackX - 128, attackY], [attackX, attackY - 128]]

    if redzone_war == True and redzone_Boom == False:
        if not RedZone_FPS == B:
            RedZone_FPS += 1
            for i in attack_list:
                screen.blit(Redzone_w_sprite[0], (i))
        else:
            redzone_Boom = True
            RedZone_FPS = 0

    if redzone_Boom == True:
        RedZone_FPS += 1

        for i in [[0,0],[0,20],[1,40],[2,60],[1,80],[2,100],[2,120]]:
            if fps > i[1]:
                fp = i[0]

        if 360 > RedZone_FPS > 30:
            for num in [0]:
                screen.blit(boom_sprite[fp], attack_list[num])
        if 390 > RedZone_FPS > 60:
            for num in [1,2,3,4]:
                screen.blit(boom_sprite[fp], attack_list[num])
        if 420 > RedZone_FPS > 90:
            for num in [5,6,7,8,9,10,11,12]:
                screen.blit(boom_sprite[fp], attack_list[num])
        if 420 < RedZone_FPS:
            redzone_war = False
            redzone_Boom = False
            RedZone_FPS = 0

def collision_check(A,B,C):
    for i in range(len(C)):
        if B+5 < C[i][1]+64 and C[i][1] < B+31 and C[i][0] < A+31 and A+5 < C[i][0]+64:
            return True
    else:
        return False

running = True #게임 진행 여부

while running:
    dt = clock.tick(120)
    animation_FP = anime(15)
    screen.blit(background, (0, 0))  # 배경 그리기

    for event in pygame.event.get(): #pygame 이벤트 속성을 가져온다
        if event.type == pygame.QUIT: #창끄는 버튼입력을 받았을 경우
            running = False #진행 끄기s
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_4:
                check[0] = 1
                move_X = -Vspeed
            if event.key == pygame.K_KP_6:
                check[1] = 1
                move_X = Vspeed
            if event.key == pygame.K_KP_5:
                check[2] = 1
                move_Y = Vspeed
            if event.key == pygame.K_KP_8:
                check[3] = 1
                move_Y = -Vspeed
            if event.key == pygame.K_SPACE:
                check[4] = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_KP_4:
                check[0] = 0
                if check[1] == 1:
                    move_X = Vspeed
                else:
                    move_X = 0
            if event.key == pygame.K_KP_6:
                check[1] = 0
                if check[0] == 1:
                    move_X = -Vspeed
                else:
                    move_X = 0
            if event.key == pygame.K_KP_5:
                check[2] = 0
                if check[3] == 1:
                    move_Y = Vspeed
                else:
                    move_Y = 0
            if event.key == pygame.K_KP_8:
                check[3] = 0
                if check[2] == 1:
                    move_Y = -Vspeed
                else:
                    move_Y = 0
            if event.key == pygame.K_SPACE:
                check[4] = 0
                shotFPS = 1

    charX += move_X
    charY += move_Y

    if charX < 0:
        charX = 0
    if charX > screen_width-a[0]:
        charX = screen_width-a[0]

    if charY < 0:
        charY = 0
    if charY > screen_height-a[1]:
        charY = screen_height-a[1]

    RedZone(500,300)

    if collision_check(charX,charY,wall_list) == True:
        charX = -500
        charY = -500

    Chracter = screen.blit(char_sprite[animation_FP], (charX, charY))


    shooting(5)

    wall_move(100, 2, 3)

    if fps > 120:
        fps = 1
    else:
        fps += 1

    pygame.display.update() #업데이트 하기


pygame.quit()