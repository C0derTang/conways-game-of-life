import pygame
import sys

play = False
WIDTH, HEIGHT = 1200, 800
BACKGROUND = (199,199,199)
FPS = 999
CELL_SIZE = 12
GM_WIDTH, GM_HEIGHT = 1200, 720
COLS, ROWS = GM_WIDTH//CELL_SIZE, GM_HEIGHT//CELL_SIZE

def get_events():
	global running
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		b.click(event)
		if not play:
			if pygame.mouse.get_pressed()[0]:
				mouse_pos = pygame.mouse.get_pos()
				if mouse_on_grid(mouse_pos):
					click_cell(mouse_pos, 0)
			if pygame.mouse.get_pressed()[2]:
				mouse_pos = pygame.mouse.get_pos()
				if mouse_on_grid(mouse_pos):
					click_cell(mouse_pos, 1)


def update():
	game_window.update()
	game_window.evaluate()


def draw():
	window.fill(BACKGROUND)
	game_window.draw()
	b.show(window)

def mouse_on_grid(pos):
	return pos[0] > WIDTH/2 - GM_WIDTH/2 and pos[0] < WIDTH - (WIDTH/2 - GM_WIDTH/2) and pos[1] > HEIGHT-(GM_HEIGHT+20) and pos[1] < HEIGHT - 20


vec = pygame.math.Vector2

class Game_window:
	def __init__(self, screen):
		self.screen = screen
		self.width, self.height = GM_WIDTH, GM_HEIGHT		
		self.pos = vec(WIDTH/2 - self.width/2, HEIGHT-(self.height+20))
		self.image = pygame.Surface((self.width, self.height))
		self.rect = self.image.get_rect()
		self.rows = ROWS
		self.cols = COLS
		self.grid = [[Cell(self.image,x, y) for x in range(self.cols)] for y in range(self.rows)]

	def update(self):
		global play, die, live
		self.rect.topleft = self.pos
		if play:
			for row in self.grid:
				for cell in row:
					cell.alive_neighbors = 0
					cell.get_neighbors(self.grid)

			for row in self.grid:
				for cell in row:
					cell.update()

	def evaluate(self):
		for row in self.grid:
			for cell in row:
				if cell.alive_neighbors < 2 and cell.alive:
					cell.alive = False
				elif cell.alive_neighbors > 3 and cell.alive:
					cell.alive = False				
				elif (cell.alive_neighbors == 2 or cell.alive_neighbors == 3) and cell.alive:
					pass
				elif cell.alive_neighbors == 3 and not cell.alive:
					cell.alive = True



	def draw(self):
		self.image.fill((102,102,102))
		for row in self.grid:
			for cell in row:
				cell.draw()

		self.screen.blit(self.image, (self.pos.x, self.pos.y))

class Cell:
	def __init__(self, surface, grid_x, grid_y):
		self.alive = False
		self.surface = surface
		self.grid_x = grid_x
		self.grid_y = grid_y
		self.image = pygame.Surface((CELL_SIZE,CELL_SIZE))
		self.rect = self.image.get_rect()
		self.neighbors = []
		self.alive_neighbors = 0

	def update(self):
		self.rect.topleft = (self.grid_x*CELL_SIZE, self.grid_y*CELL_SIZE)
		self.alive_neighbors = 0
		for cell in self.neighbors:
			if cell.alive:
				self.alive_neighbors += 1


	def draw(self):
		if self.alive:
			self.image.fill((0,0,0))
		else:
			self.image.fill((0,0,0))
			pygame.draw.rect(self.image, (255,255,255), (1,1,18,18))

		self.surface.blit(self.image, (self.grid_x*CELL_SIZE, self.grid_y*CELL_SIZE))

	def get_neighbors(self, grid):
		self.neighbors = []
		neighbor_list = [[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
		for neighbor in neighbor_list:
			neighbor[0] += self.grid_x
			neighbor[1] += self.grid_y
		for neighbor in neighbor_list:
			if neighbor[0] < 0:
				neighbor[0] += COLS

			if neighbor[1] < 0:
				neighbor[1] += ROWS

			if neighbor[1] > ROWS-1:
				neighbor[1] -= ROWS

			if neighbor[0] > COLS-1:
				neighbor[0] -= COLS

		for neighbor in neighbor_list:
			try:
				self.neighbors.append(grid[neighbor[1]][neighbor[0]])
			except:
				print(neighbor)

class Start_Button:
 
	def __init__(self, text,  pos, font, bg="black", feedback="Stop"):
		self.x, self.y = pos
		self.font = pygame.font.SysFont("Arial", font)
		if feedback == "":
			self.feedback = "text"
		else:
			self.feedback = feedback
		self.text = text
		self.start_text = text
		self.change_text(text, bg)
 
	def change_text(self, text, bg="black"):
		self.text = self.font.render(text, 1, pygame.Color("White"))
		self.size = self.text.get_size()
		self.surface = pygame.Surface(self.size)
		self.osurface = pygame.Surface((self.size[0]+10, self.size[1]+10))
		self.osurface.fill('green')
		self.surface.fill(bg)
		self.surface.blit(self.text, (0, 0))
		#self.orect = pygame.Rect(self.x-5, self.y-5, self.size[0], self.size[1])
		self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

 
	def show(self, screen):
		screen.blit(self.osurface, (self.x-5, self.y-5))
		screen.blit(self.surface, (self.x, self.y))
 
	def click(self, event):
		global play
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if self.rect.collidepoint(x, y):
					if play == True:
						play = False
						self.change_text(self.start_text, bg= "black")
					else:
						play = True
						self.change_text(self.feedback, bg="red")

def click_cell(pos,mode):
	grid_pos = [pos[0]-(WIDTH//2 - GM_WIDTH//2), pos[1]-(HEIGHT-20)]
	grid_pos[0]=grid_pos[0]//CELL_SIZE
	grid_pos[1] = grid_pos[1] // CELL_SIZE
	if mode == 0:
		game_window.grid[grid_pos[1]][grid_pos[0]].alive = True
	else:
		game_window.grid[grid_pos[1]][grid_pos[0]].alive = False

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
game_window = Game_window(window)
b = Start_Button('Start', (WIDTH//2 - 20,10), 20)


running = True

while running:
	get_events()
	if play:
		update()
	draw()
	pygame.display.update()
	clock.tick(FPS)
pygame.quit()
sys.exit()