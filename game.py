import pygame
import sys
import random

# -------------------- INITIALIZE --------------------
pygame.init()
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("COA Maze Escape")

FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 28)

# -------------------- COLORS --------------------
BACKGROUND = (20, 20, 30)
FLOOR_BASE = (92, 110, 88)
FLOOR_TILE = (110, 130, 105)
WALL_BASE = (60, 60, 65)
WALL_EDGE = (90, 90, 95)
WHITE = (255, 255, 255)
GRID_COLOR = (40, 40, 45)
KEY_COLOR = (255, 215, 0)

# -------------------- LOAD IMAGES --------------------
PLAYER_IMG = pygame.image.load("image.png.png").convert_alpha()
KEY_IMG = pygame.image.load("key.png").convert_alpha()
DOOR_IMG = pygame.image.load("door.png").convert_alpha()

# -------------------- ROOMS --------------------
rooms = [
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,2,0,0,0,0,0,3,0,1],
        [1,0,1,1,1,0,1,0,0,1],
        [1,0,0,0,1,0,1,0,1,1],
        [1,0,1,0,0,0,0,0,4,1],
        [1,1,1,1,1,1,1,1,1,1]
    ],
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,2,0,0,1,0,0,0,3,1],
        [1,0,1,0,1,0,1,0,0,1],
        [1,0,1,0,0,0,1,0,1,1],
        [1,0,0,0,1,0,0,0,4,1],
        [1,1,1,1,1,1,1,1,1,1]
    ],
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,2,0,0,0,0,3,0,0,1],
        [1,0,1,1,1,0,1,0,0,1],
        [1,0,0,0,1,0,1,0,1,1],
        [1,0,1,0,0,0,0,0,4,1],
        [1,1,1,1,1,1,1,1,1,1]
    ]
]

room_difficulty = ["Easy", "Medium", "Hard"]
current_room = 0
maze = rooms[current_room]
ROWS, COLS = len(maze), len(maze[0])
CELL = WIDTH // COLS

# Resize images to cell size
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (CELL-10, CELL-10))
KEY_IMG = pygame.transform.scale(KEY_IMG, (CELL-14, CELL-14))
DOOR_IMG = pygame.transform.scale(DOOR_IMG, (CELL-8, CELL-8))

# -------------------- GAME STATE --------------------
has_key = False
player_input = ""
coa_question = None
coa_answer = None
message = ""
message_timer = 0

# -------------------- HELPERS --------------------
def find_player():
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 2:
                return [r, c]

player_pos = find_player()

def show_message(text, time=120):
    global message, message_timer
    message = text
    message_timer = time

# -------------------- COA QUESTIONS --------------------
def generate_coa_question():
    global coa_question, coa_answer
    if current_room == 0:
        n = random.randint(10, 30)
        coa_question = f"Convert {n} to Binary"
        coa_answer = bin(n)[2:]
    elif current_room == 1:
        n = random.randint(5, 20)
        b = bin(n)[2:]
        coa_question = f"Convert {b} to Decimal"
        coa_answer = str(n)
    else:
        qa = {
            "Which unit performs arithmetic operations?": "alu",
            "Which memory is fastest?": "register",
            "Which unit controls instruction flow?": "control unit"
        }
        coa_question, coa_answer = random.choice(list(qa.items()))

# -------------------- DRAWING --------------------
def draw_hud():
    pygame.draw.rect(WIN, (0,0,0), (0,0,WIDTH,70))
    WIN.blit(FONT.render(f"Room: {current_room+1}", True, WHITE), (10,10))
    WIN.blit(FONT.render(f"Difficulty: {room_difficulty[current_room]}", True, WHITE), (10,35))
    WIN.blit(FONT.render(f"Key: {'Yes' if has_key else 'No'}", True, WHITE), (10,55))

def draw_message():
    global message_timer
    if message_timer > 0:
        msg = BIG_FONT.render(message, True, KEY_COLOR)
        WIN.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 30))
        message_timer -= 1

def draw_maze():
    WIN.fill(BACKGROUND)

    for r in range(ROWS):
        for c in range(COLS):
            x, y = c*CELL, r*CELL
            tile = maze[r][c]

            # FLOOR
            if tile in [0,2,3,4]:
                pygame.draw.rect(WIN, FLOOR_BASE, (x,y,CELL,CELL))
                pygame.draw.rect(WIN, FLOOR_TILE, (x+4,y+4,CELL-8,CELL-8), border_radius=4)

            # WALL
            if tile == 1:
                pygame.draw.rect(WIN, WALL_BASE, (x,y,CELL,CELL))
                pygame.draw.rect(WIN, WALL_EDGE, (x+3,y+3,CELL-6,CELL-6), border_radius=3)

            # KEY (IMAGE)
            if tile == 3:
                WIN.blit(KEY_IMG, (x+7, y+7))

            # DOOR (IMAGE)
            if tile == 4:
                WIN.blit(DOOR_IMG, (x+4, y+4))

            # PLAYER (IMAGE)
            if tile == 2:
                WIN.blit(PLAYER_IMG, (x+5, y+5))

    for i in range(COLS+1):
        pygame.draw.line(WIN, GRID_COLOR, (i*CELL,0),(i*CELL,HEIGHT))
    for i in range(ROWS+1):
        pygame.draw.line(WIN, GRID_COLOR, (0,i*CELL),(WIDTH,i*CELL))

    draw_hud()
    draw_message()

    if coa_question:
        WIN.blit(FONT.render(coa_question, True, WHITE), (20, HEIGHT-100))
        WIN.blit(FONT.render("Answer: "+player_input, True, KEY_COLOR), (20, HEIGHT-70))

    pygame.display.update()

# -------------------- GAME LOGIC --------------------
def load_next_room():
    global current_room, maze, ROWS, COLS, has_key, coa_question
    current_room += 1
    if current_room >= len(rooms):
        show_message("ALL ROOMS COMPLETED 🎉", 300)
        return
    maze = rooms[current_room]
    ROWS, COLS = len(maze), len(maze[0])
    player_pos[:] = find_player()
    has_key = False
    coa_question = None
    show_message(f"LEVEL {current_room+1}")

def move_player(dr, dc):
    global has_key, coa_question
    r,c = player_pos
    nr,nc = r+dr,c+dc

    if maze[nr][nc] == 1:
        return
    if maze[nr][nc] == 3:
        has_key = True
        show_message("KEY COLLECTED 🗝️")
        maze[nr][nc] = 0
    if maze[nr][nc] == 4:
        if not has_key:
            show_message("DOOR LOCKED 🚪")
            return
        if not coa_question:
            generate_coa_question()
            show_message("ANSWER TO UNLOCK")
        return

    maze[r][c] = 0
    maze[nr][nc] = 2
    player_pos[:] = [nr,nc]

# -------------------- MAIN LOOP --------------------
clock = pygame.time.Clock()
show_message("LEVEL 1 - EASY", 150)
running = True

while running:
    clock.tick(12)
    draw_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if coa_question and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if player_input.lower() == coa_answer.lower():
                    player_input = ""
                    coa_question = None
                    load_next_room()
                else:
                    show_message("WRONG ❌")
                    player_input = ""
                    coa_question = None
            elif event.key == pygame.K_BACKSPACE:
                player_input = player_input[:-1]
            else:
                player_input += event.unicode

        if not coa_question and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(-1,0)
            elif event.key == pygame.K_DOWN:
                move_player(1,0)
            elif event.key == pygame.K_LEFT:
                move_player(0,-1)
            elif event.key == pygame.K_RIGHT:
                move_player(0,1)

pygame.quit()
sys.exit()
