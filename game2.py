import sys

import pygame

pygame.init()

display_width = 1548 // 2
display_height = 516
TILE_SIZE = 43

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Game")

bg1 = pygame.image.load("./sprites/bg3.png")

clock = pygame.time.Clock()

butt1 = [pygame.image.load('./sprites/buttons/play1.png'),
         pygame.image.load('./sprites/buttons/play2.png')]
butt2 = [pygame.image.load('./sprites/buttons/options1.png'),
         pygame.image.load('./sprites/buttons/options2.png')]
plat = [pygame.image.load('./sprites/plat/road1.png'), pygame.image.load('./sprites/plat/plat1.png'),
        pygame.image.load('./sprites/plat/plat2.png'), pygame.image.load('./sprites/plat/plat3.png')]
plat[1].set_colorkey((255, 255, 255))
plat[2].set_colorkey((255, 255, 255))

animCount = 0
bgCount = 0
player_y_momentum = 0
air_time = 0
CHUNK_SIZE = 8
font = pygame.font.SysFont("", 50)
tile_rect = []
bullets = []

scroll = [0, 0]


class Player:
    isJump = False
    jumpCount = 15

    left = False
    right = False
    lastMove = "right"

    walkRight = [pygame.image.load("./sprites/biker/run right/run1.png"),
                 pygame.image.load("./sprites/biker/run right/run2.png"),
                 pygame.image.load("./sprites/biker/run right/run3.png"),
                 pygame.image.load("./sprites/biker/run right/run4.png"),
                 pygame.image.load("./sprites/biker/run right/run5.png"),
                 pygame.image.load("./sprites/biker/run right/run6.png")]

    walkLeft = [pygame.image.load("./sprites/biker/run left/run1.png"),
                pygame.image.load("./sprites/biker/run left/run2.png"),
                pygame.image.load("./sprites/biker/run left/run3.png"),
                pygame.image.load("./sprites/biker/run left/run4.png"),
                pygame.image.load("./sprites/biker/run left/run5.png"),
                pygame.image.load("./sprites/biker/run left/run6.png")]

    playerStand = [pygame.image.load("./sprites/biker/idle/idle1.png"),
                   pygame.image.load("./sprites/biker/idle/idle2.png"),
                   pygame.image.load("./sprites/biker/idle/idle3.png"),
                   pygame.image.load("./sprites/biker/idle/idle4.png")]

    playerJumpR = [pygame.image.load("./sprites/biker/jumpRight/jump1.png"),
                   pygame.image.load("./sprites/biker/jumpRight/jump2.png"),
                   pygame.image.load("./sprites/biker/jumpRight/jump3.png"),
                   pygame.image.load("./sprites/biker/jumpRight/jump4.png")]

    playerJumpL = [pygame.image.load("./sprites/biker/jumpLeft/jump1.png"),
                   pygame.image.load("./sprites/biker/jumpLeft/jump2.png"),
                   pygame.image.load("./sprites/biker/jumpLeft/jump3.png"),
                   pygame.image.load("./sprites/biker/jumpLeft/jump4.png")]

    def __init__(self, x, y, width, height, speed):
        self.speed = speed
        self.player_rect = pygame.Rect(x, y, width, height)

    def get_x(self):
        return self.player_rect.x - self.player_rect.width / 1.5 - scroll[0]

    def get_y(self):
        return self.player_rect.y - self.player_rect.height / 3 - scroll[1]


class bullet:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


man = Player(display_width / 2, 100, 45, 60, 15)


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    map_game = []
    for row in data:
        map_game.append(list(row))
    return map_game


# def generate_chunk(x, y):
#     chunk_data = []
#     for y_pos in range(CHUNK_SIZE):
#         for x_pos in range(CHUNK_SIZE):
#             target_x = x * CHUNK_SIZE + x_pos
#             target_y = y * CHUNK_SIZE + y_pos
#             tile_type = 0
#             if target_y > 11:
#                 tile_type = 2
#             elif target_y == 10:
#                 tile_type = 1
#             if tile_type != 0:
#                 chunk_data.append([[target_x, target_y], tile_type])
#     return chunk_data


game_map = load_map('map')


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def draw_tile():
    global tile_rect
    tile_rect = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(plat[0], (x * TILE_SIZE - scroll[0],
                                      y * TILE_SIZE - TILE_SIZE - scroll[1]))
            elif tile == '2':
                screen.blit(plat[3], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            elif tile == '3':
                screen.blit(plat[1], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            elif tile == '4':
                screen.blit(plat[2], (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rect.append(pygame.Rect(
                    x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1


# def draw_tile():
#     for y in range(3):
#         for x in range(3):
#             target_x = x - 1 + int(scroll[0] / (CHUNK_SIZE * 43))
#             target_y = y - 1 + int(scroll[1] / (CHUNK_SIZE * 43))
#             target_chunk = str(x) + ';' + str(y)
#             if target_chunk not in game_map:
#                 game_map[target_chunk] = generate_chunk(target_x, target_y)
#             for tile in game_map[target_chunk]:
#                 if tile[1] == '1':
#                     screen.blit(plat[0], (tile[0][0] * TILE_SIZE - scroll[0],
#                                           tile[0][1] * TILE_SIZE - TILE_SIZE - scroll[1]))
#                 elif tile[1] == '2':
#                     screen.blit(plat[3], (tile[0][0] * TILE_SIZE - scroll[0], tile[0][1] * TILE_SIZE - scroll[1]))
#                 elif tile[1] == '3':
#                     screen.blit(plat[1], (tile[0][0] * TILE_SIZE - scroll[0], tile[0][1] * TILE_SIZE - scroll[1]))
#                 elif tile[1] == '4':
#                     screen.blit(plat[2], (tile[0][0] * TILE_SIZE - scroll[0], tile[0][1] * TILE_SIZE - scroll[1]))
#                 if tile[1] != '0':
#                     tile_rect.append(pygame.Rect(
#                         tile[0][0] * TILE_SIZE, tile[0][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_window():
    global animCount, bgCount

    screen.blit(bg1, (scroll[0] / 10, scroll[1] / 10))

    draw_tile()
    print(game_map)

    if animCount >= 30:
        animCount = 0

    if man.isJump:
        if man.lastMove == "right":
            screen.blit(man.playerJumpR[animCount // 5], (man.get_x(), man.get_y()))
        else:
            screen.blit(man.playerJumpL[animCount // 5], (man.get_x(), man.get_y()))
        animCount += 1
    elif man.right:
        screen.blit(man.walkRight[animCount // 5], (man.get_x(), man.get_y()))
        animCount += 1
    elif man.left:
        screen.blit(man.walkLeft[animCount // 5], (man.get_x(), man.get_y()))
        animCount += 1
    else:
        screen.blit(man.playerStand[animCount // 8], (man.get_x(), man.get_y()))
        animCount += 1
    print(animCount)

    for bul in bullets:
        bul.draw(screen)

    # pygame.draw.rect(screen, "red", man.player_rect)
    pygame.display.update()


def draw_text(text, font_rect, color, surface, x, y):
    text_obj = font_rect.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def pressed_key(keys):
    global animCount, player_y_momentum, air_time

    player_movement = [0, 0]
    if keys[pygame.K_d]:
        player_movement[0] += man.speed
        man.lastMove = "right"
        man.right = True
        man.left = False
    elif keys[pygame.K_a]:
        if man.player_rect.x > - man.player_rect.width / 2:
            player_movement[0] -= man.speed
            man.lastMove = "left"
            man.right = False
            man.left = True
    else:
        man.left = False
        man.right = False

    if keys[pygame.K_f]:
        if man.lastMove == 'right':
            face = 1
        else:
            face = -1

        if len(bullets) < 100:
            bullets.append(bullet(round(man.player_rect.x + man.player_rect.width // 2), round(man.player_rect.y +
                                                                                               man.player_rect.height // 2),
                                  5, (255, 0, 0), face))

    # if not man.isJump:
    #     if keys[pygame.K_SPACE]:
    #         man.isJump = True
    #         animCount = 0
    # else:
    # if man.jumpCount >= -15:
    #     if man.jumpCount < 0:
    #         man.player_rect.y += (man.jumpCount ** 2) / 3
    #     else:
    #         man.player_rect.y -= (man.jumpCount ** 2) / 3
    #     man.jumpCount -= 2
    # else:
    #     man.isJump = False
    #     man.jumpCount = 15
    if keys[pygame.K_SPACE]:
        if air_time < 1:
            animCount = 0
            man.isJump = True
            player_y_momentum = -60

    player_movement[1] += player_y_momentum
    player_y_momentum += 10
    if player_y_momentum > 50:
        player_y_momentum = 50

    man.player_rect, collision = move(man.player_rect, player_movement, tile_rect)
    if collision['top']:
        player_y_momentum = 10
    if collision['bottom']:
        player_y_momentum = 0
        air_time = 0
        man.isJump = False
    else:
        air_time += 1


def main_menu():
    running = True
    click = False
    while running:
        clock.tick(30)
        pygame.time.delay(40)

        screen.fill((0, 0, 0))
        draw_text('main menu', font, (255, 255, 255),
                  screen, display_width // 2 - 95, 30)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(display_width // 2 - 100, 100, 200, 50)
        button2 = pygame.Rect(display_width // 2 - 100, 200, 200, 50)

        screen.blit(butt1[0], (display_width // 2 - 100, 100))
        screen.blit(butt2[0], (display_width // 2 - 100, 200))
        if button1.collidepoint((mx, my)):
            screen.blit(butt1[1], (display_width // 2 - 100, 100))
            if click:
                game()
        if button2.collidepoint((mx, my)):
            screen.blit(butt2[1], (display_width // 2 - 100, 200))
            if click:
                option()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def option():
    running = True
    while running:
        clock.tick(30)
        pygame.time.delay(40)

        screen.fill((0, 0, 0))
        draw_text('options', font, (255, 255, 255),
                  screen, display_width // 2 - 100, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()


def game():
    global animCount

    running = True
    while running:
        clock.tick(60)
        pygame.time.delay(60)

        scroll[0] += int(man.player_rect.x - scroll[0] - display_width / 2 - man.player_rect.width / 2) / 5
        # scroll[1] += int(man.player_rect.y - scroll[1] - display_height / 2 - man.player_rect.height / 2) / 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        for bul in bullets:
            if 1024 > bul.x > 0:
                bul.x += bul.vel
            else:
                bullets.pop(bullets.index(bul))

        keys = pygame.key.get_pressed()

        pressed_key(keys)

        draw_window()


if __name__ == "__main__":
    main_menu()
