import pygame
import sys
import Setings
import save
import time

pygame.init()

ScreenX = Setings.ScreenX
ScreenY = Setings.ScreenY
Screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("CityLine")

grass_image = pygame.image.load(save.grass).convert_alpha()
sand_image = pygame.image.load(save.sand).convert_alpha()
factory_image = pygame.image.load(save.factory).convert_alpha()
cursor_image = pygame.image.load(save.cursor).convert_alpha()
flat_image = pygame.image.load(save.Flat).convert_alpha()
tree_image = pygame.image.load(save.forest).convert_alpha()
font = pygame.font.SysFont(None, 48)

money = 100
peoples = 0
factories = 0




def draw_map():
    cell_size = save.CellSize
    map_data = save.Map

    if not isinstance(map_data, list):
        return

    for y in range(len(map_data)):
        if not isinstance(map_data[y], list):
            continue

        for x in range(len(map_data[y])):
            pos_x = x * cell_size
            pos_y = y * cell_size

            if map_data[y][x] == 1:
                Screen.blit(grass_image, (pos_x, pos_y))
            elif map_data[y][x] == 2:
                Screen.blit(sand_image, (pos_x, pos_y))
            else:
                pygame.draw.rect(Screen, (0, 0, 0), (pos_x, pos_y, cell_size, cell_size))

def draw_buildings():
    cell_size = save.CellSize
    map_data = save.MapBuilds
    factory_payments = 100
    flat_payments = 50

    if not isinstance(map_data, list):
        return

    for y in range(len(map_data)):
        if not isinstance(map_data[y], list):
            continue

        for x in range(len(map_data[y])):
            pos_x = x * cell_size
            pos_y = y * cell_size

            if map_data[y][x] == 1:
                Screen.blit(factory_image, (pos_x, pos_y))
                factory_payments += save.payments
            elif map_data[y][x] == 2:
                Screen.blit(flat_image, (pos_x, pos_y))
                flat_payments += save.payments
            elif map_data[y][x] == 3:
                Screen.blit(tree_image, (pos_x, pos_y))
                flat_payments += save.payments


cursor_x, cursor_y = 0, 0
columns = 15
rows = 9

last_update_time = pygame.time.get_ticks()
update_interval = 5000

def update_economy():
    payments = save.payments
    global factories, money
    money += factories * 100
    money += peoples * 10
    payments -= money

    print(f"Updated payments: {payments}")



clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if cursor_x > 0:
                    save.MapCursor[cursor_y][cursor_x] = 0
                    cursor_x -= 1
                    save.MapCursor[cursor_y][cursor_x] = 1
            elif event.key == pygame.K_d:
                if cursor_x < columns - 1:
                    save.MapCursor[cursor_y][cursor_x] = 0
                    cursor_x += 1
                    save.MapCursor[cursor_y][cursor_x] = 1
            elif event.key == pygame.K_w:
                if cursor_y > 0:
                    save.MapCursor[cursor_y][cursor_x] = 0
                    cursor_y -= 1
                    save.MapCursor[cursor_y][cursor_x] = 1
            elif event.key == pygame.K_s:
                if cursor_y < rows - 1:
                    save.MapCursor[cursor_y][cursor_x] = 0
                    cursor_y += 1
                    save.MapCursor[cursor_y][cursor_x] = 1
            elif event.key == pygame.K_1:
                if money >= 100:
                    save.MapBuilds[cursor_y][cursor_x] = 1
                    money -= 100
                    factories += 1
            elif event.key == pygame.K_2:
                if money >= 10:
                    save.MapBuilds[cursor_y][cursor_x] = 2
                    money -= 10
                    peoples += 100
            elif event.key == pygame.K_5:
                save.MapBuilds[cursor_y][cursor_x] = 0

    if current_time - last_update_time >= update_interval:
        update_economy()
        last_update_time = current_time

    Screen.fill((0, 0, 0))
    draw_map()
    draw_buildings()

    for y in range(rows):
        for x in range(columns):
            if save.MapCursor[y][x] == 1:
                Screen.blit(cursor_image, (x * save.CellSize, y * save.CellSize))

    money_text = "$ : " + str(money)
    peoples_text = " peoples :  " + str(peoples)
    money_surface = font.render(money_text + peoples_text , True, (255, 255, 255))
    text_rect = money_surface.get_rect(topleft=(10, 10))
    Screen.blit(money_surface, (10, 10))

    if peoples == 10000 :
        with open('end.txt', 'w') as file:
            file.write("thanks for playing this is the end! You have become a worthy honey and made a career for yourself, thank you for playing!")
        pygame.quit()
        sys.exit()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
