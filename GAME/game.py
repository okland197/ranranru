import pygame
import random

pygame.init()

##게임 기본 설정ㄱ-----------------------------------------------------------------------

#프레임 설정을 위한 시간
clock = pygame.time.Clock()
#화면 크기 조절
screen_width = 640
screen_height = 512
#디스플레이 크기 설정
screen = pygame.display.set_mode((screen_width, screen_height))
#원도우 창 위 제목설정
pygame.display.set_caption("테스트")
#현재 프레임 값
fps = 1

##소리 설정ㄱ---------------------------------------------------------------------------

#소리 꺼내오기
background_Sound = pygame.mixer.Sound("Background.wav")
effect_gun_Sound = pygame.mixer.Sound("Gun.wav")
Redzone_war_Sound = pygame.mixer.Sound("Redzone_war.wav")

#소리 설정하기
effect_gun_Sound.set_volume(0.5)
background_Sound.play(-1)

##이미지 불러오기ㄱ----------------------------------------------------------------------

background = pygame.image.load("background.png")
char_attack_sprite = [pygame.image.load("char_Attack1.png"),pygame.image.load("char_Attack2.png")]
wall_sprite = [pygame.image.load("wall1.png")]
Redzone_w_sprite = [pygame.image.load("redzone-warning.png")]
boom_sprite = [pygame.image.load("boom1.png"),pygame.image.load("boom2.png"),pygame.image.load("boom3.png")]

##(주인공)캐릭터 기본 설정 및 슈팅 설정ㄱ---------------------------------------------------

##(주인공)캐릭터ㄱ
#(주인공)캐릭터 이미지 불러오기
char_sprite = [pygame.image.load("char1.png"),pygame.image.load("char2.png")]
#(주인공)캐릭터 이미지 크기 값 불러오기
a = char_sprite[0].get_size()
#(주인공)캐릭터가 최초로 있을 위치 계산
charX = (screen_width/2)-(a[0]/2)
charY = (screen_height/2)-(a[1]/2)
#(주인공)캐릭터가 움직이는 속도
Vspeed = 4
#(주인공)캐릭터가 X방향으로 움직이는 변수
move_X = 0
#(주인공)캐릭터가 Y방향으로 움직이는 변수
move_Y = 0
#특정키 누르는 중이란 것을 표현하기 위한 변수
#왼쪽,오른쪽,아래,위,스페이스
check = [0,0,0,0,0]
#(주인공)캐릭터 애니메이션 프레임 값
chr_s_num = 0
#애니메이션 프레임 값 0 1을 내보내는 값
animation_FP = 0

##슈팅ㄱ
#화면에서 현재 슈팅이 띄어지는 위치들 목록
shot_list = []
#슈팅이 특정이벤트에 의해 지워질 리스트들
del_shot_list = []
#슈팅 애니메이션 프레임 값 (근데 움직이는게 안 보여)
shotFPS = 0

##방해물 설정ㄱ---------------------------------------------------------------------------

#벽 움직이는 속도를 맟추기 위한 변수
wall_FPS = 0
#현재 화면에 있는 벽들 리스트
wall_list = []

##어려운 방해물들 설정ㄱ--------------------------------------------------------------------

##레드존 공격ㄱ
#현재 화면에 몇프레임까지 띄울 것 인지를 표현하기 위한 변수
RedZone_FPS = 0
#현재 화면에 존재하는 레드존 리스트들
RedZone_list = []
#레드존 경고 시작
redzone_war = False
#레드존 폭팔 시작
redzone_Boom = False
#레드존 랜덤 위치를 저장하기 위한 변수
attackX,attackY = [0,0]

#---------------------------------------------------------------------------------------



##함수 설정ㄱ-----------------------------------------------------------------------------

##(주인공)캐릭터 애니메이션이 움직이는 함수ㄱ
def anime(A):
    for i in range(10):
        if i%2 == 0 or i == 0:
            if (A*i) < fps < (A*(i+1)):
                animation_FP = 0
                return animation_FP
    else:
        animation_FP = 1
        return animation_FP

##슈팅 함수ㄱ
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

##방해물 함수ㄱ
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

##레드존 함수ㄱ
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

##(주인공)캐릭터랑 충돌하는 함수ㄱ
def collision_check(A,B,C):
    for i in range(len(C)):
        if B+5 < C[i][1]+64 and C[i][1] < B+31 and C[i][0] < A+31 and A+5 < C[i][0]+64:
            return True
    else:
        return False

#게임 진행 여부----------------------------------------------------------------------------
running = True
#게임 진행--------------------------------------------------------------------------------
while running:
    dt = clock.tick(120)
    animation_FP = anime(15)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    pygame.display.update()

pygame.quit()