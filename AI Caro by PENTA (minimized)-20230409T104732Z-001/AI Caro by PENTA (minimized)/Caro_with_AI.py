import pygame
import random
import numpy as np
import time
import asyncio
import setuptools
pygame.init()
pygame.display.set_caption('Cờ Ca Rô')
icon = pygame.image.load('Data\\icon.png')
pygame.display.set_icon(icon)
resolution_h = 1000
resolution_w = 1500
screen = pygame.display.set_mode((1500,1000),pygame.RESIZABLE)

force_restart = False
now_move_x, now_move_y = 0,0
img = pygame.image.load('Data\\line.png')
imgx = pygame.image.load('Data\\x.png')
clock = pygame.time.Clock()
grey = (150,150,150)
white = (255,255,255)
red = (255,0,0)
BLACK = (0,0,0)
orange = (255,165,0)
yellow = (255,255,0)
green = (0,200,0)
cyan = (255, 87, 51)
checkAI = False
Pwin = False
Pwin_n = False
time_out = False
x = 0
y = 0
w = 50
time_start = False
ingame = True
win = False
check = []

font = pygame.font.SysFont('sans',50)
fontmove = pygame.font.SysFont('sans',200)
fontwin = pygame.font.SysFont('sans',80)
textwinred = fontwin.render('Win' ,True, red)
textwingreen = fontwin.render('Win' ,True, green)
textwinShadow = fontwin.render('Win' ,True, BLACK)
textXwin = fontwin.render('Player' ,True, red)
textXwinShadow = fontwin.render('Player' ,True, BLACK)
textOwin = fontwin.render('Computer' ,True, green)
textOwinShadow = fontwin.render('Computer' ,True, BLACK)
textDraw = fontwin.render('Draw' ,True, cyan)
fonttime = pygame.font.SysFont('sans',150)
textDrawShadow = fontwin.render('Draw' ,True, BLACK)
fontagain = pygame.font.SysFont('sans',100)
textX = font.render('X' ,True, red)
textXyellow = font.render('X' ,True, yellow)
textOyellow = font.render('O' ,True, yellow)
textcombo = font.render('Best Combo:' ,True, yellow)
textcomboshadow = font.render('Best Combo:' ,True, BLACK)
textTotalMove = fontagain.render('Total Move' ,True, BLACK)
again = fontagain.render('Restart' ,True, white)
fontturn = pygame.font.SysFont('sans',65)
X_turn = fontturn.render('Your Turn' ,True, white)
O_turn_1 = fontturn.render('Computer Is' ,True, white)
O_turn_2 = fontturn.render('Thinking...' ,True, white)
textO = font.render('O' ,True, orange)
textO_pre = font.render('O' ,True, green)
running = True
player = 1
played = 0
timeover = False
screen.fill(white)
pygame.draw.rect(screen,white,(1000,0,500,1000))
pygame.draw.rect(screen,BLACK,(1000,250,500,500))
pygame.draw.rect(screen,red,(1000,500,500,250))
screen.blit(X_turn, (1130,510))
table=[[0 for row in range(30)] for col in range(30)]
for i in range(30):
	for z in range(30):
		table[i][z]=-2
	while y < 1000:
		if x >= 1000:
			x = 0
			y = y + w
		while x < 1000:
			pygame.draw.line(screen, BLACK, [x,y] , [x+w,y])
			pygame.draw.line(screen, BLACK, [x,y] , [x,y+w])
			pygame.draw.line(screen, BLACK, [x,y+w] , [x+w,y+w])
			pygame.draw.line(screen, BLACK, [x+w,y] , [x+w,y+w])
			x = x + w
for i in range(1,21):
	for z in range(1,21):
		table[i][z]=-1
	pygame.display.update()
line_check = True
timeoversound = False
x_time = 120
o_time = 120
x_time_sec = round(x_time) % 60
x_time_min = round(x_time) // 60
cs = time.time()
pygame.mixer.music.load("Data\\restart.mp3")
pygame.mixer.music.play()
combo = 0
try:
	with open('Data\\combo.txt','r') as f:
		h_combo = int(f.read())
	f.close()
except Exception:
	with open('Data\\combo.txt','w+') as f:
		f.write('0')
	f.close()
	with open('Data\\combo.txt','r') as f:
		h_combo = int(f.read())
	f.close()


while running:

	if combo > h_combo:
		with open('Data\\combo.txt','w') as f:
			f.write(str(combo))
		f.close()
		h_combo = combo
	
	img = pygame.image.load('Data\\line.png')
	imgx = pygame.image.load('Data\\x.png')
	
		
	if win == False and time_start == True:
		csnow = time.time() - cs
		x_time = x_time - csnow
		csnow = 0
		cs = time.time()
		x_time_sec = round(x_time) % 60
		x_time_min = round(x_time) // 60
		pygame.draw.rect(screen,red,(1050,590,400,150))
		texttime = fonttime.render(f'{x_time_min}:{x_time_sec}' ,True, green)
		texttimeShadow = fonttime.render(f'{x_time_min}:{x_time_sec}' ,True, BLACK)
		screen.blit(texttimeShadow,(1132,562))
		screen.blit(texttime,(1130,560))

		pygame.display.update()


	if x_time_sec == 0 and x_time_min == 0:
		win = True
		line_check = False
		timeover = True
		x_time_sec = -1
		x_time_min = -1


		



	if time_start == False:
		x_time_sec = round(x_time) % 60
		x_time_min = round(x_time) // 60
		pygame.draw.rect(screen,red,(1050,590,400,150))
		texttime = fonttime.render(f'{x_time_min}:{x_time_sec}' ,True, green)
		texttimeShadow = fonttime.render(f'{x_time_min}:{x_time_sec}' ,True, BLACK)
		screen.blit(texttimeShadow,(1132,562))
		screen.blit(texttime,(1130,560))
		pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN and win == False:
			cs = time.time()
			time_start = True

			a = (mouse_x - (mouse_x % 50 )) // 50 +1
			b = (mouse_y - (mouse_y % 50)) // 50 +1
			if player == 1 and (([mouse_x - (mouse_x % 50 ) + 10,mouse_y - (mouse_y % 50) -2] ) not in check) and mouse_x <= 1000:
				played = played + 1
				pygame.mixer.music.load("Data\\Xclick.mp3")
				pygame.mixer.music.play()
				
				
				pygame.draw.rect(screen,BLACK,(1000,250,500,500))
				pygame.draw.rect(screen,green,(1000,250,500,250))
				
				screen.blit(O_turn_1, (1030+70,550-250))
				screen.blit(O_turn_2, (1080+60,550-170))
				screen.blit(textX, (mouse_x - (mouse_x % 50 ) +10 ,mouse_y - (mouse_y % 50) -2 ))
				pygame.display.update()
				check.append([mouse_x - (mouse_x % 50 ) + 10,mouse_y - (mouse_y % 50) -2])
				table[a][b] = 1

				##########################
				if table[a-1][b] == 1 and table[a-2][b] == 1 and table[a-3][b] == 1 and table[a-4][b] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a-1][b] == 1 and table[a-2][b] == 1 and table[a-3][b] == 1 and table[a+1][b] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a-1][b] == 1 and table[a-2][b] == 1 and table[a+1][b] == 1 and table[a+2][b] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a-1][b] == 1 and table[a+1][b] == 1 and table[a+2][b] == 1 and table[a+3][b] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a+1][b] == 1 and table[a+2][b] == 1 and table[a+3][b] == 1 and table[a+4][b] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)

				if table[a][b-1] == 1 and table[a][b-2] == 1 and table[a][b-3] == 1 and table[a][b-4] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a][b-1] == 1 and table[a][b-2] == 1 and table[a][b-3] == 1 and table[a][b+1] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a][b-1] == 1 and table[a][b-2] == 1 and table[a][b+1] == 1 and table[a][b+2] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a][b-1] == 1 and table[a][b+1] == 1 and table[a][b+2] == 1 and table[a][b+3] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a][b+1] == 1 and table[a][b+2] == 1 and table[a][b+3] == 1 and table[a][b+4] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)

				if table[a-1][b-1] == 1 and table[a-2][b-2] == 1 and table[a-3][b-3] == 1 and table[a-4][b-4] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a-1][b-1] == 1 and table[a-2][b-2] == 1 and table[a-3][b-3] == 1 and table[a+1][b+1] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a-1][b-1] == 1 and table[a-2][b-2] == 1 and table[a+1][b+1] == 1 and table[a+2][b+2] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a-1][b-1] == 1 and table[a+3][b+3] == 1 and table[a+1][b+1] == 1 and table[a+2][b+2] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a+4][b+4] == 1 and table[a+3][b+3] == 1 and table[a+1][b+1] == 1 and table[a+2][b+2] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a+1][b-1] == 1 and table[a+2][b-2] == 1 and table[a+3][b-3] == 1 and table[a+4][b-4] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a+1][b-1] == 1 and table[a+2][b-2] == 1 and table[a+3][b-3] == 1 and table[a-1][b+1] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a+1][b-1] == 1 and table[a+2][b-2] == 1 and table[a-2][b+2] == 1 and table[a-1][b+1] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a+1][b-1] == 1 and table[a-3][b+3] == 1 and table[a-2][b+2] == 1 and table[a-1][b+1] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if table[a-4][b+4] == 1 and table[a-3][b+3] == 1 and table[a-2][b+2] == 1 and table[a-1][b+1] == 1:
					pygame.draw.rect(screen,green,(1080,0,340,200))
					screen.blit(textXwinShadow,(1152,22))
					screen.blit(textwinShadow,(1172,102))
					screen.blit(textXwin,(1150,20))
					screen.blit(textwinred,(1170,100))
					win = True
					combo = combo + 1
					pygame.display.update()
					time.sleep(1)
				if win == False:
					player = 0


				time.sleep(int(np.random.randint(7))/10+0.3)
			
			checkAI = False
			Pwin_n = False
			pygame.draw.rect(screen,BLACK,(1000,250,500,500))
			pygame.draw.rect(screen,red,(1000,500,500,250))
			screen.blit(X_turn, (1130,510))

			if player == 0 and win == False:
				player = 1
				csnow = time.time() - cs
				o_time = o_time - csnow
				csnow = 0
				cs = time.time()
				o_time_sec = round(o_time) % 60
				o_time_min = round(o_time) // 60

				
				while checkAI == False:
					
					random = np.random.randint(8)
					checkAI = True

					if random == 0 and (mouse_x <50 or mouse_y < 50):
						checkAI = False
					if random == 1 and mouse_y < 50:
						checkAI= False
					if random == 2 and (mouse_x > 950 or mouse_y < 50):
						checkAI = False
					if random == 3 and mouse_x < 50:
						checkAI = False
					if random == 4 and mouse_x > 950:
						checkAI = False
					if random == 5 and (mouse_x <50 or mouse_y > 950):
						checkAI = False
					if random == 6 and mouse_y > 950:
						checkAI = False
					if random == 7 and (mouse_x > 950 or mouse_y > 950):
						checkAI = False

					############################################# 
						#AI ngang
				if table[a-1][b] == 1 and table[a-2][b] == 1:
					random = 4
				if table[a+1][b] == 1 and table[a+2][b] == 1:
					random = 3
				if table[a-1][b] == 1 and table[a+2][b] == 1 and table[a+3][b] == 1:
					random = 4
				if table[a-1][b] == 1 and table[a+1][b] == 1:
					random = 8
				if table[a-1][b] == 1 and table[a+2][b] == 1:
					random = 4
				if table[a+1][b] == 1 and table[a-2][b] == 1:
					random = 3
				if table[a-1][b] == -1 and table[a-2][b] == 1 and table[a-3][b] == 1:
					random = 3
				if table[a+1][b] == -1 and table[a+2][b] == 1 and table[a+3][b] == 1:
					random = 4
				if table[a+1][b] == 1 and table[a+3][b] == 1 and table[a+2][b] == -1:
					random = 9
				if table[a-1][b] == 1 and table[a-2][b] == -1 and table[a-3][b] == 1:
					random = 8
				if table[a-1][b] == 1 and table[a+1][b] == 1 and table[a+2][b] == 1 and table[a+3][b] == 0:
					random = 8
				if table[a+1][b] == 1 and table[a-1][b] == 1 and table[a-2][b] == 1 and table[a-3][b] == 0:
					random = 9
					##################################################
						#AI Doc
				if table[a][b-1] == 1 and table[a][b-2] == 1:
					random = 6
				if table[a][b+1] == 1 and table[a][b+2] == 1:
					random = 1
				if table[a][b-1] == 1 and table[a][b+2] == 1 and table[a][b+3] == 1:
					random = 6
				if table[a][b-1] == 1 and table[a][b+1] == 1:
					random = 10
				if table[a][b-1] == 1 and table[a][b+2] == 1:
					random = 6
				if table[a][b+1] == 1 and table[a][b-2] == 1:
					random = 1
				if table[a][b+1] == 1 and table[a][b+3] == 1 and table[a][b+2] == -1:
					random = 11
				if table[a][b-1] == 1 and table[a][b-2] == -1 and table[a][b-3] == 1:
					random = 10
				if table[a][b-1] == -1 and table[a][b-2] == 1 and table[a][b-3] == 1:
					random = 1
				if table[a][b+1] == -1 and table[a][b+2] == 1 and table[a][b+3] == 1:
					random = 6
				if table[a][b-1] == 1 and table[a][b+1] == 1 and table[a][b+2] == 1 and table[a][b+3] == 0:
					random = 10
				if table[a][b+1] == 1 and table[a][b-1] == 1 and table[a][b-2] == 1 and table[a][b-3] == 0:
					random = 11
					##################################################
						#AI \
				if table[a-1][b-1] == 1 and table[a-2][b-2] == 1:
					random = 7
				if table[a+1][b+1] == 1 and table[a+2][b+2] == 1:
					random = 0
				if table[a-1][b-1] == 1 and table[a+2][b+2] == 1 and table[a+3][b+3] == 1:
					random = 7
				if table[a-1][b-1] == 1 and table[a+1][b+1] == 1:
					random = 12
				if table[a-1][b-1] == 1 and table[a+2][b+2] == 1:
					random = 7
				if table[a+1][b+1] == 1 and table[a-2][b-2] == 1:
					random = 0
				if table[a-1][b-1] == -1 and table[a-2][b-2] == 1 and table[a-3][b-3] == 1:
					random = 0
				if table[a+1][b+1] == -1 and table[a+2][b+2] == 1 and table[a+3][b+3] == 1:
					random = 7
				if table[a+1][b+1] == 1 and table[a+3][b+3] == 1 and table[a+2][b+2] == -1:
					random = 13
				if table[a-1][b-1] == 1 and table[a-2][b-2] == -1 and table[a-3][b-3] == 1:
					random = 12
				if table[a-1][b-1] == 1 and table[a+1][b+1] == 1 and table[a+2][b+2] == 1 and table[a+3][b+3] == 0:
					random = 12
				if table[a+1][b+1] == 1 and table[a-1][b-1] == 1 and table[a-2][b-2] == 1 and table[a-3][b-3] == 0:
					random = 13
					##################################################
						#AI /
				if table[a-1][b+1] == 1 and table[a-2][b+2] == 1:
					random = 2
				if table[a+1][b-1] == 1 and table[a+2][b-2] == 1:
					random = 5
				if table[a-1][b+1] == 1 and table[a+2][b-2] == 1 and table[a+3][b-3] == 1:
					random = 2
				if table[a-1][b+1] == 1 and table[a+1][b-1] == 1:
					random = 14
				if table[a-1][b+1] == 1 and table[a+2][b-2] == 1:
					random = 2
				if table[a+1][b-1] == 1 and table[a-2][b+2] == 1:
					random = 5
				if table[a-1][b+1] == -1 and table[a-2][b+2] == 1 and table[a-3][b+3] == 1:
					random = 5
				if table[a+1][b-1] == -1 and table[a+2][b-2] == 1 and table[a+3][b-3] == 1:
					random = 2
				if table[a+1][b-1] == 1 and table[a+3][b-3] == 1 and table[a+2][b-2] == -1:
					random = 15
				if table[a-1][b+1] == 1 and table[a-2][b+2] == -1 and table[a-3][b+3] == 1:
					random = 14
				if table[a-1][b+1] == 1 and table[a+1][b-1] == 1 and table[a+2][b-2] == 1 and table[a+3][b-3] == 0:
					random = 14
				if table[a+1][b-1] == 1 and table[a-1][b+1] == 1 and table[a-2][b+2] == 1 and table[a-3][b+3] == 0:
					random = 15
				##############################################################
				if table[a-1][b] == 1 and table[a-2][b] == 1 and table[a-3][b] == 1:
					random = 4
					Pwin = True
				if table[a+1][b] == 1 and table[a+2][b] == 1 and table[a+3][b] == 1:
					random = 3
					Pwin = True
				if table[a][b-1] == 1 and table[a][b-2] == 1 and table[a][b-3] == 1:
					random = 6
					Pwin = True
				if table[a][b+1] == 1 and table[a][b+2] == 1 and table[a][b+3] == 1:
					random = 1
					Pwin = True
				if table[a-1][b-1] == 1 and table[a-2][b-2] == 1 and table[a-3][b-3] == 1:
					random = 7
					Pwin = True
				if table[a+1][b+1] == 1 and table[a+2][b+2] == 1 and table[a+3][b+3] == 1:
					random = 0
					Pwin = True
				if table[a+1][b-1] == 1 and table[a+2][b-2] == 1 and table[a+3][b-3] == 1:
					random = 5
					Pwin = True
				if table[a-1][b+1] == 1 and table[a-2][b+2] == 1 and table[a-3][b+3] == 1:
					random = 2
					Pwin = True

				#################################################################	
				if random == 0:
					mouse_x = mouse_x - 50
					mouse_y = mouse_y - 50
				if random == 1:
					mouse_y = mouse_y - 50
				if random == 2:
					mouse_x = mouse_x + 50
					mouse_y = mouse_y - 50
				if random == 3:
					mouse_x = mouse_x - 50
				if random == 4:
					mouse_x = mouse_x + 50
				if random == 5:
					mouse_y = mouse_y + 50
					mouse_x = mouse_x - 50
				if random == 6:
					mouse_y = mouse_y + 50
				if random == 7:
					mouse_y = mouse_y + 50
					mouse_x = mouse_x + 50
				if random == 8:
					mouse_x = mouse_x - 100
				if random == 9:
					mouse_x = mouse_x + 100
				if random == 10:
					mouse_y = mouse_y - 100
				if random == 11:
					mouse_y = mouse_y + 100
				if random == 12:
					mouse_x = mouse_x - 100
					mouse_y = mouse_y - 100
				if random == 13:
					mouse_x = mouse_x + 100
					mouse_y = mouse_y + 100
				if random == 14:
					mouse_x = mouse_x - 100
					mouse_y = mouse_y + 100
				if random == 15:
					mouse_x = mouse_x + 100
					mouse_y = mouse_y - 100

				a = (mouse_x - (mouse_x % 50 )) // 50 +1
				b = (mouse_y - (mouse_y % 50)) // 50 +1

				while table[a][b] == -2 or table[a][b] == 1 or table[a][b] == 0:
					random = np.random.randint(8)
					
					checkAI = False
					if random == 0:
						mouse_x = mouse_x - 50
						mouse_y = mouse_y - 50
					if random == 1:
						mouse_y = mouse_y - 50
					if random == 2:
						mouse_x = mouse_x + 50
						mouse_y = mouse_y - 50
					if random == 3:
						mouse_x = mouse_x - 50
					if random == 4:
						mouse_x = mouse_x + 50
					if random == 5:
						mouse_y = mouse_y + 50
						mouse_x = mouse_x - 50
					if random == 6:
						mouse_y = mouse_y + 50
					if random == 7:
						mouse_y = mouse_y + 50
						mouse_x = mouse_x + 50
					while checkAI == False:
						
						checkAI = True
						

						
						if random == 0 and (mouse_x <50 or mouse_y < 50):
							checkAI = False
							mouse_x = mouse_x + 100
							mouse_y = mouse_y + 100
						if random == 1 and mouse_y < 50:
							checkAI= False
							mouse_y = mouse_y + 100
						if random == 2 and (mouse_x > 950 or mouse_y < 50):
							checkAI = False
							mouse_x = mouse_x - 100
							mouse_y = mouse_y + 100
						if random == 3 and mouse_x < 50:
							checkAI = False
							mouse_x = mouse_x + 100
						if random == 4 and mouse_x > 950:
							checkAI = False
							mouse_x = mouse_x - 100
						if random == 5 and (mouse_x <50 or mouse_y > 950):
							checkAI = False
							mouse_x = mouse_x + 100
							mouse_y = mouse_y - 100
						if random == 6 and mouse_y > 950:
							checkAI = False
							mouse_y = mouse_y - 100
						if random == 7 and (mouse_x > 950 or mouse_y > 950):
							checkAI = False
							mouse_x = mouse_x - 100
							mouse_y = mouse_y - 100
					
					a = (mouse_x - (mouse_x % 50 )) // 50 +1
					b = (mouse_y - (mouse_y % 50)) // 50 +1

					
				Pwin = False
				Pwin_n = False
				for yy in range(21):
					count = 0
					for xx in range(21):
						if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy]==1 and table[xx-1][yy] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy]==1 and table[xx+4][yy] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]==1 and table[xx][yy-1] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]==1 and table[xx][yy+4] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]== -1 and table[xx][yy-1] == -1  and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]==1 and table[xx-1][yy-1] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]==1 and table[xx+4][yy+4] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == -1  and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy-1] == 1 and table[xx+2][yy-2] == 1 and table[xx+3][yy-3]==1 and table[xx-1][yy+1] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy-1] == 1 and table[xx+2][yy-2] == 1 and table[xx+3][yy-3]==1 and table[xx+4][yy-4] == -1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy-1] == 1 and table[xx+2][yy-2] == 1 and table[xx+3][yy-3] == -1 and table[xx-1][yy+1] == -1  and Pwin == False:
							Pwin_n = True
							break_check = True
							break

						if table[xx][yy] == 1 and table[xx+1][yy] == -1 and table[xx+2][yy] == 1 and table[xx+3][yy]==1 and table[xx+4][yy] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == -1 and table[xx+3][yy]== 1 and table[xx+4][yy] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy]== -1 and table[xx+4][yy] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == -1 and table[xx][yy+2] == 1 and table[xx][yy+3]== 1 and table[xx][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == -1 and table[xx][yy+3]== 1 and table[xx][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]== -1 and table[xx][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy] == -1 and table[xx+2][yy] == 1 and table[xx+3][yy]== 1 and table[xx+4][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == -1 and table[xx+3][yy]== 1 and table[xx+4][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == -1 and table[xx][yy+2] == 1 and table[xx][yy+3]== 1 and table[xx][yy+4] == -1 and table[xx][yy-1] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == -1 and table[xx][yy+3]== 1 and table[xx][yy+4] == -1 and table[xx][yy-1] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break

						if table[xx][yy] == 1 and table[xx+1][yy+1] == -1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]==1 and table[xx+4][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == -1 and table[xx+3][yy+3]== 1 and table[xx+4][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+1] == 1 and table[xx+3][yy+1]== -1 and table[xx+4][yy+1] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx-1][yy+1] == -1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3]==1 and table[xx-4][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == -1 and table[xx-3][yy+3]== 1 and table[xx-4][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3]== -1 and table[xx-4][yy+4] == 1:
							Pwin = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy+1] == -1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]== 1 and table[xx+4][yy+4] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == -1 and table[xx+3][yy+3]== 1 and table[xx+4][yy+4] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx-1][yy+1] == -1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3]== 1 and table[xx-4][yy+4] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
						if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == -1 and table[xx-3][yy+3]== 1 and table[xx-4][yy+4] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
							Pwin_n = True
							break_check = True
							break
					if break_check == True:
						break_check = False
						break


				if Pwin == False and Pwin_n == False:
					for yy in range(21):
						count = 0
						for xx in range(21):
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == -1 and table[xx+3][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
								mouse_x = (xx+2)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == -1 and table[xx+2][yy] == 1 and table[xx+3][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
								mouse_x = (xx+1)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == -1 and table[xx][yy+3] == -1 and table[xx][yy-1] == -1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == -1 and table[xx][yy+2] == 1 and table[xx][yy+3] == -1 and table[xx][yy-1] == -1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == -1 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx+2)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == -1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx+1)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == -1 and table[xx-3][yy+3] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx-2)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx-1][yy+1] == -1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break

							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy] == 1 and table[xx-1][yy] == -1 and Pwin == False:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy] == -1 and table[xx-1][yy] == 1 and Pwin == False:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3] == 1 and table[xx][yy-1] == -1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy-1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3] == -1 and table[xx][yy-1] == 1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3] == 1 and table[xx-1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy-1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == 1 and Pwin == False:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3] == 1 and table[xx+1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx+1)*50 - 1
								mouse_y = (yy-1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3] == -1 and table[xx+1][yy-1] == 1 and Pwin == False:
								mouse_x = (xx-3)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
						if break_check == True:
							break_check = False
							break

				for yy in range(21):
					count = 0
					for xx in range(21):
						if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == 0 and table[xx+3][yy]==0 and table[xx-1][yy] == -1:
							mouse_x = (xx-1)*50 - 1
							mouse_y = yy*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == 0 and table[xx+3][yy]==0 and table[xx+4][yy] == -1:
							mouse_x = (xx+4)*50 - 1
							mouse_y = (yy)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == 0 and table[xx][yy+3]==0 and table[xx][yy-1] == -1:
							mouse_y = (yy-1)*50 - 1
							mouse_x = xx*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == 0 and table[xx][yy+3]==0 and table[xx][yy+4] == -1:
							mouse_y = (yy+4)*50 - 1
							mouse_x = (xx)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3]==0 and table[xx-1][yy-1] == -1:
							mouse_x = (xx-1)*50 - 1
							mouse_y = (yy-1)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3]==0 and table[xx+4][yy+4] == -1:
							mouse_x = (xx+4)*50 - 1
							mouse_y = (yy+4)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy-1] == 0 and table[xx+2][yy-2] == 0 and table[xx+3][yy-3]==0 and table[xx-1][yy+1] == -1:
							mouse_x = (xx-1)*50 - 1
							mouse_y = (yy+1)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy-1] == 0 and table[xx+2][yy-2] == 0 and table[xx+3][yy-3]==0 and table[xx+4][yy-4] == -1:
							mouse_x = (xx+4)*50 - 1
							mouse_y = (yy-4)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy] == -1 and table[xx+2][yy] == 0 and table[xx+3][yy]==0 and table[xx+4][yy] == 0:
							mouse_x = (xx+1)*50 - 1
							mouse_y = yy*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == -1 and table[xx+3][yy]== 0 and table[xx+4][yy] == 0:
							mouse_x = (xx+2)*50 - 1
							mouse_y = yy*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == 0 and table[xx+3][yy]== -1 and table[xx+4][yy] == 0:
							mouse_x = (xx+3)*50 - 1
							mouse_y = yy*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx][yy+1] == -1 and table[xx][yy+2] == 0 and table[xx][yy+3]==0 and table[xx][yy+4] == 0:
							mouse_x = xx*50 - 1
							mouse_y = (yy+1)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == -1 and table[xx][yy+3]== 0 and table[xx][yy+4] == 0:
							mouse_x = xx*50 - 1
							mouse_y = (yy+2)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == 0 and table[xx][yy+3]== -1 and table[xx][yy+4] == 0:
							mouse_x = xx*50 - 1
							mouse_y = (yy+3)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy+1] == -1 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3]==0 and table[xx+4][yy+4] == 0:
							mouse_x = (xx+1)*50 - 1
							mouse_y = (yy+1)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == -1 and table[xx+3][yy+3]== 0 and table[xx+4][yy+4] == 0:
							mouse_x = (xx+2)*50 - 1
							mouse_y = (yy+2)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+1] == 0 and table[xx+3][yy+1]== -1 and table[xx+4][yy+1] == 0:
							mouse_x = (xx+3)*50 - 1
							mouse_y = (yy+3)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx-1][yy+1] == -1 and table[xx-2][yy+2] == 0 and table[xx-3][yy+3]==0 and table[xx-4][yy+4] == 0:
							mouse_x = (xx-1)*50 - 1
							mouse_y = (yy+1)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx-1][yy+1] == 0 and table[xx-2][yy+2] == -1 and table[xx-3][yy+3]== 0 and table[xx-4][yy+4] == 0:
							mouse_x = (xx-2)*50 - 1
							mouse_y = (yy+2)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx-1][yy+1] == 0 and table[xx-2][yy+2] == 0 and table[xx-3][yy+3]== -1 and table[xx-4][yy+4] == 0:
							mouse_x = (xx-3)*50 - 1
							mouse_y = (yy+3)*50 - 1
							Pwin = False
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == 0 and table[xx+3][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
							mouse_x = (xx+3)*50 - 1
							mouse_y = (yy)*50 - 1
							Pwin_n = False
							break_check = True
							break
						
						if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == 0 and table[xx][yy+3]== -1 and table[xx][yy-1] == -1  and Pwin == False:
							mouse_y = (yy+3)*50 - 1
							mouse_x = (xx)*50 - 1
							Pwin_n = False
							break_check = True
							break
						
						if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
							mouse_x = (xx+3)*50 - 1
							mouse_y = (yy+3)*50 - 1
							Pwin_n = False
							break_check = True
							break
						
						if table[xx][yy] == 0 and table[xx+1][yy-1] == 0 and table[xx+2][yy-2] == 0 and table[xx+3][yy-3] == -1 and table[xx-1][yy+1] == -1 and Pwin == False:
							mouse_x = (xx+3)*50 - 1
							mouse_y = (yy-3)*50 - 1
							Pwin_n = False
							break_check = True
							break

						
						if table[xx][yy] == 0 and table[xx+1][yy] == -1 and table[xx+2][yy] == 0 and table[xx+3][yy]== 0 and table[xx+4][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
							mouse_x = (xx+1)*50 - 1
							mouse_y = yy*50 - 1
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == -1 and table[xx+3][yy]== 0 and table[xx+4][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
							mouse_x = (xx+2)*50 - 1
							mouse_y = yy*50 - 1
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx][yy+1] == -1 and table[xx][yy+2] == 0 and table[xx][yy+3]== 0 and table[xx][yy+4] == -1 and table[xx][yy-1] == -1 and Pwin == False:
							mouse_x = xx*50 - 1
							mouse_y = (yy+1)*50 - 1
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == -1 and table[xx][yy+3]== 0 and table[xx][yy+4] == -1 and table[xx][yy-1] == -1 and Pwin == False:
							mouse_x = xx*50 - 1
							mouse_y = (yy+2)*50 - 1
							Pwin_n = False
							break_check = True
							break

						

						if table[xx][yy] == 0 and table[xx+1][yy+1] == -1 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3]== 0 and table[xx+4][yy+4] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
							mouse_x = (xx+1)*50 - 1
							mouse_y = (yy+1)*50 - 1
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == -1 and table[xx+3][yy+3]== 0 and table[xx+4][yy+4] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
							mouse_x = (xx+2)*50 - 1
							mouse_y = (yy+2)*50 - 1
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx-1][yy+1] == -1 and table[xx-2][yy+2] == 0 and table[xx-3][yy+3]== 0 and table[xx-4][yy+4] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
							mouse_x = (xx-1)*50 - 1
							mouse_y = (yy+1)*50 - 1
							Pwin_n = False
							break_check = True
							break
						if table[xx][yy] == 0 and table[xx-1][yy+1] == 0 and table[xx-2][yy+2] == -1 and table[xx-3][yy+3]== 0 and table[xx-4][yy+4] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
							mouse_x = (xx-2)*50 - 1
							mouse_y = (yy+2)*50 - 1
							Pwin_n = False
							break_check = True
							break

						if Pwin_n == False:
							if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == -1 and table[xx+3][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
								mouse_x = (xx+2)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx+1][yy] == -1 and table[xx+2][yy] == 0 and table[xx+3][yy] == -1 and table[xx-1][yy] == -1 and Pwin == False:
								mouse_x = (xx+1)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == -1 and table[xx][yy+3] == -1 and table[xx][yy-1] == -1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx][yy+1] == -1 and table[xx][yy+2] == 0 and table[xx][yy+3] == -1 and table[xx][yy-1] == -1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == -1 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx+2)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx+1][yy+1] == -1 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx+1)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx-1][yy+1] == 0 and table[xx-2][yy+2] == -1 and table[xx-3][yy+3] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx-2)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx-1][yy+1] == -1 and table[xx-2][yy+2] == 0 and table[xx-3][yy+3] == -1 and table[xx+1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break

							if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == 0 and table[xx+3][yy] == 1 and table[xx-1][yy] == -1 and Pwin == False:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == 0 and table[xx+3][yy] == -1 and table[xx-1][yy] == 1 and Pwin == False:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == 0 and table[xx][yy+3] == 1 and table[xx][yy-1] == -1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy-1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == 0 and table[xx][yy+3] == -1 and table[xx][yy-1] == 1 and Pwin == False:
								mouse_x = (xx)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3] == 1 and table[xx-1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy-1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == 1 and Pwin == False:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx-1][yy+1] == 0 and table[xx-2][yy+2] == 0 and table[xx-3][yy+3] == 1 and table[xx+1][yy-1] == -1 and Pwin == False:
								mouse_x = (xx+1)*50 - 1
								mouse_y = (yy-1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 0 and table[xx-1][yy+1] == 0 and table[xx-2][yy+2] == 0 and table[xx-3][yy+3] == -1 and table[xx+1][yy-1] == 1 and Pwin == False:
								mouse_x = (xx-3)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
					if break_check == True:
						break_check = False
						break

				



				if Pwin == True or Pwin_n == True:
					for yy in range(21):
						count = 0
						for xx in range(21):
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy]== 1 and table[xx-1][yy] == -1:
								mouse_x = (xx-1)*50 - 1
								mouse_y = yy*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy]== 1 and table[xx+4][yy] == -1:
								mouse_x = (xx+4)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy] == -1 and table[xx-1][yy] == -1:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]== 1 and table[xx][yy-1] == -1:
								mouse_y = (yy-1)*50 - 1
								mouse_x = xx*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]== 1 and table[xx][yy+4] == -1:
								mouse_y = (yy+4)*50 - 1
								mouse_x = (xx)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]== -1 and table[xx][yy-1] == -1:
								mouse_y = (yy+3)*50 - 1
								mouse_x = (xx)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]== 1 and table[xx-1][yy-1] == -1:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy-1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]== 1 and table[xx+4][yy+4] == -1:
								mouse_x = (xx+4)*50 - 1
								mouse_y = (yy+4)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3] == -1 and table[xx-1][yy-1] == -1:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy-1] == 1 and table[xx+2][yy-2] == 1 and table[xx+3][yy-3]== 1 and table[xx-1][yy+1] == -1:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy-1] == 1 and table[xx+2][yy-2] == 1 and table[xx+3][yy-3]== 1 and table[xx+4][yy-4] == -1:
								mouse_x = (xx+4)*50 - 1
								mouse_y = (yy-4)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy-1] == 1 and table[xx+2][yy-2] == 1 and table[xx+3][yy-3] == -1 and table[xx-1][yy+1] == -1:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy-3)*50 - 1
								break_check = True
								break

							if table[xx][yy] == 1 and table[xx+1][yy] == -1 and table[xx+2][yy] == 1 and table[xx+3][yy]== 1 and table[xx+4][yy] == 1:
								mouse_x = (xx+1)*50 - 1
								mouse_y = yy*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == -1 and table[xx+3][yy]== 1 and table[xx+4][yy] == 1:
								mouse_x = (xx+2)*50 - 1
								mouse_y = yy*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy]== -1 and table[xx+4][yy] == 1:
								mouse_x = (xx+3)*50 - 1
								mouse_y = yy*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == -1 and table[xx][yy+2] == 1 and table[xx][yy+3]== 1 and table[xx][yy+4] == 1:
								mouse_x = xx*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == -1 and table[xx][yy+3]== 1 and table[xx][yy+4] == 1:
								mouse_x = xx*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]== -1 and table[xx][yy+4] == 1:
								mouse_x = xx*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == -1 and table[xx+2][yy] == 1 and table[xx+3][yy]== 1 and table[xx+4][yy] == -1 and table[xx-1][yy] == -1:
								mouse_x = (xx+1)*50 - 1
								mouse_y = yy*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == -1 and table[xx+3][yy]== 1 and table[xx+4][yy] == -1 and table[xx-1][yy] == -1:
								mouse_x = (xx+2)*50 - 1
								mouse_y = yy*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == -1 and table[xx][yy+2] == 1 and table[xx][yy+3]== 1 and table[xx][yy+4] == -1 and table[xx][yy-1] == -1:
								mouse_x = xx*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == -1 and table[xx][yy+3]== 1 and table[xx][yy+4] == -1 and table[xx][yy-1] == -1:
								mouse_x = xx*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break

							if table[xx][yy] == 1 and table[xx+1][yy+1] == -1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]==1 and table[xx+4][yy+4] == 1:
								mouse_x = (xx+1)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == -1 and table[xx+3][yy+3]== 1 and table[xx+4][yy+4] == 1:
								mouse_x = (xx+2)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+1] == 1 and table[xx+3][yy+1]== -1 and table[xx+4][yy+1] == 1:
								mouse_x = (xx+3)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx-1][yy+1] == -1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3]==1 and table[xx-4][yy+4] == 1:
								mouse_x = (xx-1)*50 - 1
								mouse_y = (yy+1)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == -1 and table[xx-3][yy+3]== 1 and table[xx-4][yy+4] == 1:
								mouse_x = (xx-2)*50 - 1
								mouse_y = (yy+2)*50 - 1
								break_check = True
								break
							if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3]== -1 and table[xx-4][yy+4] == 1:
								mouse_x = (xx-3)*50 - 1
								mouse_y = (yy+3)*50 - 1
								break_check = True
								break
						if break_check == True:
							break_check = False
							break


				break_check = False


				a = (mouse_x - (mouse_x % 50 )) // 50+1
				b = (mouse_y - (mouse_y % 50)) // 50+1
				pre_move_x, pre_move_y = now_move_x, now_move_y
				now_move_x, now_move_y = mouse_x - (mouse_x % 50 ) +10, mouse_y - (mouse_y % 50) -2

				if ([mouse_x - (mouse_x % 50 ) + 10,mouse_y - (mouse_y % 50) -2] ) not in check:
					pygame.mixer.music.load("Data\\Oclick.mp3")
					pygame.mixer.music.play()
					played = played + 1
					player = 1
					
					checkAI = False
					screen.blit(textO, (now_move_x,now_move_y))
					if pre_move_x == 0 and pre_move_y == 0:
						pass
					else:	
						screen.blit(textO_pre, (pre_move_x,pre_move_y))
					pygame.display.update()
					check.append([mouse_x - (mouse_x % 50 ) +10, mouse_y - (mouse_y % 50) -2])
					table[a][b] = 0

					##################################################
					if table[a-1][b] == 0 and table[a-2][b] == 0 and table[a-3][b] == 0 and table[a-4][b] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-1][b] == 0 and table[a-2][b] == 0 and table[a-3][b] == 0 and table[a+1][b] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-1][b] == 0 and table[a-2][b] == 0 and table[a+1][b] == 0 and table[a+2][b] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-1][b] == 0 and table[a+1][b] == 0 and table[a+2][b] == 0 and table[a+3][b] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a+1][b] == 0 and table[a+2][b] == 0 and table[a+3][b] == 0 and table[a+4][b] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a][b-1] == 0 and table[a][b-2] == 0 and table[a][b-3] == 0 and table[a][b-4] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a][b-1] == 0 and table[a][b-2] == 0 and table[a][b-3] == 0 and table[a][b+1] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a][b-1] == 0 and table[a][b-2] == 0 and table[a][b+1] == 0 and table[a][b+2] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a][b-1] == 0 and table[a][b+1] == 0 and table[a][b+2] == 0 and table[a][b+3] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a][b+1] == 0 and table[a][b+2] == 0 and table[a][b+3] == 0 and table[a][b+4] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-1][b-1] == 0 and table[a-2][b-2] == 0 and table[a-3][b-3] == 0 and table[a-4][b-4] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-1][b-1] == 0 and table[a-2][b-2] == 0 and table[a-3][b-3] == 0 and table[a+1][b+1] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-1][b-1] == 0 and table[a-2][b-2] == 0 and table[a+1][b+1] == 0 and table[a+2][b+2] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-1][b-1] == 0 and table[a+3][b+3] == 0 and table[a+1][b+1] == 0 and table[a+2][b+2] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a+4][b+4] == 0 and table[a+3][b+3] == 0 and table[a+1][b+1] == 0 and table[a+2][b+2] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a+1][b-1] == 0 and table[a+2][b-2] == 0 and table[a+3][b-3] == 0 and table[a+4][b-4] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a+1][b-1] == 0 and table[a+2][b-2] == 0 and table[a+3][b-3] == 0 and table[a-1][b+1] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a+1][b-1] == 0 and table[a+2][b-2] == 0 and table[a-2][b+2] == 0 and table[a-1][b+1] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a+1][b-1] == 0 and table[a-3][b+3] == 0 and table[a-2][b+2] == 0 and table[a-1][b+1] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					if table[a-4][b+4] == 0 and table[a-3][b+3] == 0 and table[a-2][b+2] == 0 and table[a-1][b+1] == 0:
						pygame.draw.rect(screen,cyan,(1080,0,340,200))
						screen.blit(textOwinShadow,(1102,7))
						screen.blit(textwinShadow,(1182,102))
						screen.blit(textOwin,(1100,5))
						screen.blit(textwingreen,(1180,100))
						win = True
						combo = 0
						pygame.display.update()
						time.sleep(1)
					cs = time.time()
			#for i in range(30):
			#	print()
			#	for z in range(30):
			#		print(table[z][i],end=' ')
			#print()
		break_check = False
		if played >= 300:
			win = True
			line_check = False
			screen.blit(textDrawShadow,(1052,21))
			screen.blit(textDraw,(1050,20))

		

	if win == True:
		

		if timeover == True:
			timeover = False
			pygame.draw.rect(screen,red,(1001,250,500,500))
			pygame.draw.rect(screen,red,(1000,200,500,100))
			pygame.draw.rect(screen,orange,(1000,300,500,450))
			pygame.mixer.music.load("Data\\outoftime.mp3")
			pygame.mixer.music.play()
			pygame.draw.rect(screen,cyan,(1080,0,340,200))
			screen.blit(textOwinShadow,(1102,7))
			screen.blit(textwinShadow,(1182,102))
			screen.blit(textOwin,(1100,5))
			screen.blit(textwingreen,(1180,100))
			text_out_of_time = font.render('Player Out Of Time' ,True, white)
			text_out_of_time_shadow = font.render('Player Out Of Time' ,True, BLACK)
			screen.blit(text_out_of_time_shadow,(1072,222))
			screen.blit(text_out_of_time,(1070,220))
			

			
		if line_check == True:
			pygame.draw.rect(screen,red,(1001,250,500,500))
			pygame.draw.rect(screen,red,(1000,200,500,100))
			pygame.draw.rect(screen,orange,(1000,300,500,450))
			text_check = font.render('Check In Line' ,True, white)
			text_check_shadow = font.render('Check In Line' ,True, BLACK)
			screen.blit(text_check_shadow,(1102,222))
			screen.blit(text_check,(1100,220))

		

		screen.blit(textTotalMove,(1050,350))
		textMove = fontmove.render(str(played) ,True, BLACK)
		screen.blit(textMove,(1120,480))
		break_check = False
		if line_check == True:
			for yy in range(21):
				for xx in range(21):
					if table[xx][yy] == 0 and table[xx+1][yy] == 0 and table[xx+2][yy] == 0 and table[xx+3][yy]==0 and table[xx+4][yy] == 0:
						img = pygame.transform.rotate(img,90)
						screen.blit(img, ((xx-1)*50,(yy-1)*50 + 20))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break
					if table[xx][yy] == 0 and table[xx][yy+1] == 0 and table[xx][yy+2] == 0 and table[xx][yy+3]==0 and table[xx][yy+4] == 0:
						screen.blit(img, ((xx-1)*50 + 18,(yy-1)*50))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break
					if table[xx][yy] == 0 and table[xx+1][yy+1] == 0 and table[xx+2][yy+2] == 0 and table[xx+3][yy+3]==0 and table[xx+4][yy+4] == 0:
						imgx = pygame.transform.rotate(imgx,45)
						screen.blit(imgx, ((xx-1)*50 + 10,(yy-1)*50 + 15))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break
					if table[xx][yy] == 0 and table[xx-1][yy+1] == 0 and table[xx-2][yy+2] == 0 and table[xx-3][yy+3]==0 and table[xx-4][yy+4] == 0:
						imgx = pygame.transform.rotate(imgx,135)
						screen.blit(imgx, ((xx-5)*50 + 5,(yy-1)*50 + 15))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break


					if table[xx][yy] == 1 and table[xx+1][yy] == 1 and table[xx+2][yy] == 1 and table[xx+3][yy]== 1 and table[xx+4][yy] == 1:
						img = pygame.transform.rotate(img,90)
						screen.blit(img, ((xx-1)*50,(yy-1)*50 + 20))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break
					if table[xx][yy] == 1 and table[xx][yy+1] == 1 and table[xx][yy+2] == 1 and table[xx][yy+3]== 1 and table[xx][yy+4] == 1:
						screen.blit(img, ((xx-1)*50 + 18,(yy-1)*50))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break
					if table[xx][yy] == 1 and table[xx+1][yy+1] == 1 and table[xx+2][yy+2] == 1 and table[xx+3][yy+3]== 1 and table[xx+4][yy+4] == 1:
						imgx = pygame.transform.rotate(imgx,45)
						screen.blit(imgx, ((xx-1)*50 + 10,(yy-1)*50 + 15))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break
					if table[xx][yy] == 1 and table[xx-1][yy+1] == 1 and table[xx-2][yy+2] == 1 and table[xx-3][yy+3]== 1 and table[xx-4][yy+4] == 1:
						imgx = pygame.transform.rotate(imgx,135)
						screen.blit(imgx, ((xx-5)*50 + 5,(yy-1)*50 + 15))
						break_check = True
						pygame.mixer.music.load("Data\\checkinline.mp3")
						pygame.mixer.music.play()
						break

				if break_check == True:
					break
		line_check = False
	pygame.draw.rect(screen,green,(1001,750,500,80))
	pygame.draw.rect(screen,orange,(1400,750,101,80))
	screen.blit(textcomboshadow,(1052,762))
	screen.blit(textcombo,(1050,760))
	texthcombo = font.render(str(h_combo) ,True, yellow)
	texthcomboshadow = font.render(str(h_combo) ,True, BLACK)
	textnowcombo = font.render(str(combo) ,True, yellow)
	textnowcomboshadow = font.render(str(combo) ,True, BLACK)
	screen.blit(texthcomboshadow,(1302,762))
	screen.blit(texthcombo,(1300,760))
	screen.blit(textnowcomboshadow,(1442 - len(str(combo))*10,762))
	screen.blit(textnowcombo,(1440 - len(str(combo))*10,760))



	again_green = fontagain.render('Restart' ,True, green)
	pygame.draw.rect(screen,BLACK,(1100,780+50,300,150))
	screen.blit(again,(1110,790+50))
	pygame.display.update()
	if pygame.display.Info().current_w != resolution_w or pygame.display.Info().current_h != resolution_h:
		resolution_w = pygame.display.Info().current_w
		resolution_h = pygame.display.Info().current_h
		force_restart = True
	if event.type == pygame.MOUSEBUTTONDOWN or force_restart == True:
		if mouse_x >= 1100 and mouse_x <= 1100 + 300 and mouse_y >= 780+50 and mouse_y <= 780+150 or force_restart == True:
			force_restart = False
			pygame.mixer.music.load("Data\\restart.mp3")
			pygame.mixer.music.play()
			timeover = False
			time_out = False
			time_start = False
			x_time = 120
			o_time = 120
			x_time_sec = round(x_time) % 60
			x_time_min = round(x_time) // 60
			cs = time.time()
			played = 0
			now_move_x, now_move_y = 0,0
			player = 1
			screen.blit(again_green,(1110,790+50))
			pygame.display.update()
			time.sleep(0.2)
			line_check = True
			win = False
			x = 0
			y = 0
			check = []
			screen.fill(white)
			pygame.draw.rect(screen,white,(1000,0,500,1000))
			pygame.draw.rect(screen,BLACK,(1000,250,500,500))
			pygame.draw.rect(screen,red,(1000,500,500,250))
			screen.blit(X_turn, (1130,510))
			table=[[0 for row in range(30)] for col in range(30)]
			for i in range(30):
				for z in range(30):
					table[i][z]=-2
				while y < 1000:
					if x >= 1000:
						x = 0
						y = y + w
					while x < 1000:
						pygame.draw.line(screen, BLACK, [x,y] , [x+w,y])
						pygame.draw.line(screen, BLACK, [x,y] , [x,y+w])
						pygame.draw.line(screen, BLACK, [x,y+w] , [x+w,y+w])
						pygame.draw.line(screen, BLACK, [x+w,y] , [x+w,y+w])
						x = x + w
			for i in range(1,21):
				for z in range(1,21):
					table[i][z]=-1
				pygame.display.update()
					

		if event.type == pygame.QUIT:
			running = False