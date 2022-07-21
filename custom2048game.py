from custom2048 import *
import pygame
pygame.init()

all_sprite_sheets = ["normal-2048.png", "pretty-2048.png", "smash-2048.png", "rock-2048.png"]

gb = GameBoard(4, 4)
gb.set_parameter("starting_tiles", 2)
gb.set_parameter("chance_to_spawn_lowest", 0.9)
gb.set_parameter("sprite_sheet_file", "normal-2048.png")
gb.set_parameter("win_condition", 11)

screen = pygame.display.set_mode([gb.width*100, gb.height*100+100])
pygame.display.set_caption("Custom 2048")

running = True
game_updated = False
settings_menu_open = False
current_theme = 0

main_buttons = []
settings_buttons = []

sprite_sheet = pygame.image.load(gb.parameters["sprite_sheet_file"])
button_sheet = pygame.image.load("button2048.png").convert_alpha()
winscreen = pygame.image.load("winscreen.png").convert_alpha()
gb.set_parameter("sprite_sheet_rows", 4)
gb.set_parameter("sprite_sheet_cols", 4)
gb.set_parameter("sprite_sheet_height", sprite_sheet.get_height())
gb.set_parameter("sprite_sheet_width", sprite_sheet.get_width())

class Button:
    def __init__(self, src, pos, area, callback):
        self.src = src
        self.pos = pos
        self.area = area
        self.callback = callback

    def render(self):
        m_pos = pygame.mouse.get_pos()
        if m_pos[0] >= self.pos[0] and m_pos[0] <= self.pos[0]+self.pos[2] and m_pos[1] >= self.pos[1] and m_pos[1] <= self.pos[1]+self.pos[3]:
            draw_sprite(self.src, self.pos, (self.area[0], self.area[1]+self.area[3], self.area[2], self.area[3]))
        else:
            draw_sprite(self.src, self.pos, self.area)

    def check_click(self):
        m_pos = pygame.mouse.get_pos()
        if m_pos[0] >= self.pos[0] and m_pos[0] <= self.pos[0]+self.pos[2] and m_pos[1] >= self.pos[1] and m_pos[1] <= self.pos[1]+self.pos[3]:
            self.callback()

def draw_sprite(src, pos, area):
    c = pygame.Surface((pos[2], pos[3]), pygame.SRCALPHA, 32).convert_alpha()
    x_scalar = pos[2]/area[2]
    y_scalar = pos[3]/area[3]
    src = pygame.transform.scale(src, (src.get_width()*x_scalar, src.get_height()*y_scalar))
    c.blit(src, (0, 0), (area[0]*x_scalar, area[1]*y_scalar, area[2]*x_scalar, area[3]*y_scalar))
    screen.blit(c, (pos[0], pos[1]))

def draw_text(text, x, y, size, color):
    font = pygame.font.Font(None, size) 
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)

def open_settings_menu():
    global settings_menu_open
    settings_menu_open = True

def close_settings_menu():
    global settings_menu_open
    settings_menu_open = False
    gb.reset()

def change_theme():
    global current_theme
    global sprite_sheet
    current_theme = (current_theme + 1) % len(all_sprite_sheets)
    gb.set_parameter("sprite_sheet_file", all_sprite_sheets[current_theme])
    sprite_sheet = pygame.image.load(gb.parameters["sprite_sheet_file"])

def increase_rows():
    gb.set_parameter("height", gb.height+1)
    resize_screen()

def decrease_rows():
    gb.set_parameter("height", gb.height-1)
    resize_screen()

def increase_cols():
    gb.set_parameter("width", gb.width+1)
    resize_screen()

def decrease_cols():
    gb.set_parameter("width", gb.width-1)
    resize_screen()

def resize_screen():
    global screen
    screen = pygame.display.set_mode([gb.width*100, gb.height*100+100])
    generate_buttons()

def generate_buttons():
    global main_buttons
    global settings_buttons
    main_buttons = []
    main_buttons.append(Button(button_sheet, (10, 10, 75, 30), (0, 0, 250, 100), gb.reset))
    main_buttons.append(Button(button_sheet, (gb.width*100-80, 10, 30, 30), (250, 0, 100, 100), gb.undo))
    main_buttons.append(Button(button_sheet, (gb.width*100-40, 10, 30, 30), (350, 0, 100, 100), open_settings_menu))

    settings_buttons = []
    settings_buttons.append(Button(button_sheet, (120, 60, 30, 15), (700, 0, 100, 50), increase_rows))
    settings_buttons.append(Button(button_sheet, (120, 80, 30, 15), (700, 100, 100, 50), decrease_rows))
    settings_buttons.append(Button(button_sheet, (120, 120, 30, 15), (700, 0, 100, 50), increase_cols))
    settings_buttons.append(Button(button_sheet, (120, 140, 30, 15), (700, 100, 100, 50), decrease_cols))
    settings_buttons.append(Button(button_sheet, (gb.width*100/2-62.5, gb.height*100+25, 125, 50), (450, 0, 250, 100), close_settings_menu))
    settings_buttons.append(Button(button_sheet, (gb.width*100-40, 60, 30, 15), (700, 0, 100, 50), lambda: gb.set_parameter("win_condition", gb.parameters["win_condition"]+1 if gb.parameters["win_condition"] < 15 else gb.parameters["win_condition"])))
    settings_buttons.append(Button(button_sheet, (gb.width*100-40, 80, 30, 15), (700, 100, 100, 50), lambda: gb.set_parameter("win_condition", gb.parameters["win_condition"]-1 if gb.parameters["win_condition"] > 1 else gb.parameters["win_condition"])))
    settings_buttons.append(Button(button_sheet, (gb.width*100-120, 100, 75, 30), (800, 0, 250, 100), change_theme))
    settings_buttons.append(Button(button_sheet, (gb.width*100-40, 150, 30, 15), (700, 0, 100, 50), lambda: gb.set_parameter("starting_tiles", gb.parameters["starting_tiles"]+1 if gb.parameters["starting_tiles"] < gb.width*gb.height else gb.parameters["starting_tiles"])))
    settings_buttons.append(Button(button_sheet, (gb.width*100-40, 170, 30, 15), (700, 100, 100, 50), lambda: gb.set_parameter("starting_tiles", gb.parameters["starting_tiles"]-1 if gb.parameters["starting_tiles"] > 1 else gb.parameters["starting_tiles"])))
    settings_buttons.append(Button(button_sheet, (gb.width*100-40, 210, 30, 15), (700, 0, 100, 50), lambda: gb.set_parameter("chance_to_spawn_lowest", gb.parameters["chance_to_spawn_lowest"]+0.05 if gb.parameters["chance_to_spawn_lowest"] < 1 else gb.parameters["chance_to_spawn_lowest"])))
    settings_buttons.append(Button(button_sheet, (gb.width*100-40, 230, 30, 15), (700, 100, 100, 50), lambda: gb.set_parameter("chance_to_spawn_lowest", gb.parameters["chance_to_spawn_lowest"]-0.05 if gb.parameters["chance_to_spawn_lowest"] > 0 else gb.parameters["chance_to_spawn_lowest"])))

generate_buttons()

gb.set_initial_state()

while running:
    m_pos = pygame.mouse.get_pos()
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not gb.win_state == 1 and not settings_menu_open:
                if not game_updated and (event.key == pygame.K_UP or event.key == pygame.K_w):
                    game_updated = gb.shift("up")
                if not game_updated and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    game_updated = gb.shift("left")
                if not game_updated and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    game_updated = gb.shift("down")
                if not game_updated and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    game_updated = gb.shift("right")
        if event.type == pygame.MOUSEBUTTONUP:
            gb.continue_after_win()
            if gb.game_is_over():
                gb.reset()
            if not settings_menu_open:
                for b in main_buttons:
                    b.check_click()
            else:
                for b in settings_buttons:
                    b.check_click()
    if game_updated:
        gb.spawn_new()
    # Fill the background with white
    screen.fill((255, 255, 255))
    if not settings_menu_open:
        for y, row in enumerate(gb.board):
            for x, cell in enumerate(row):
                draw_sprite(sprite_sheet, (x*100, y*100+50, 100, 100), gb.get_sprite(cell.value))
        draw_text("Score: "+str(int(gb.score)), gb.width*100/2, 25, 25, (0, 0, 0))
        for b in main_buttons:
            b.render()
        draw_text("Combine same tiles to reach the       tile.", gb.width*100/2, gb.height*100+75, 30, (0, 0, 0))
        draw_sprite(sprite_sheet, (gb.width*100/2+120, gb.height*100+57, 36, 36), gb.get_sprite(gb.parameters["win_condition"]))
        if gb.game_is_won():
            draw_sprite(winscreen, (0, 0, gb.width*100, gb.height*100+50), (0, 0, 500, 200))
            draw_text("YOU WIN!", gb.width*100/2, (gb.height*100+50)/2, 40, (0, 0, 0))
            draw_text("Click to continue.", gb.width*100/2, (gb.height*100+50)/2+50, 20, (0, 0, 0))
        if gb.game_is_over():
            draw_sprite(winscreen, (0, 0, gb.width*100, gb.height*100+50), (0, 0, 500, 200))
            draw_text("GAME OVER", gb.width*100/2, (gb.height*100+50)/2, 40, (0, 0, 0))
            draw_text("Final Score: "+str(int(gb.score)), gb.width*100/2, (gb.height*100+50)/2+50, 40, (0, 0, 0))
            draw_text("Click to start a new game.", gb.width*100/2, (gb.height*100+50)/2+100, 20, (0, 0, 0))
    else:
        draw_text("SETTINGS", gb.width*100/2, 25, 40, (0, 0, 0))
        draw_text("Rows: "+str(gb.height), 50, 78, 25, (0, 0, 0))
        draw_text("Columns: "+str(gb.width), 60, 138, 25, (0, 0, 0))
        draw_text("Win tile:", gb.width*100-120, 78, 25, (0, 0, 0))
        draw_sprite(sprite_sheet, (gb.width*100-80, 60, 35, 35), gb.get_sprite(gb.parameters["win_condition"]))
        draw_text("Starting tiles: "+str(gb.parameters["starting_tiles"]), gb.width*100-110, 168, 25, (0, 0, 0))
        draw_text("Low-tile spawn rate: "+str(gb.parameters["chance_to_spawn_lowest"]), gb.width*100-145, 228, 25, (0, 0, 0))
        for b in settings_buttons:
            b.render()


    # Flip the display
    pygame.display.flip()
    if game_updated:
        gb.game_is_over() # just a check to see if it is over, does not actually end the game
        game_updated = False

# Done! Time to quit.
pygame.quit()