import sys

import pygame

pygame.init()

display_width = 1548 // 2
display_height = 516
TILE_SIZE = 43

screen = pygame.display.set_mode((display_width, display_height), 0, 32)
pygame.display.set_caption("Game")

bg1 = pygame.image.load("./sprites/bg3.png").convert()

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
tile_rect = []
bullets = []
scroll = [0, 0]
main_font = pygame.font.SysFont("comicsansms", 40)
health_font = pygame.font.SysFont("comicsansms", 25)


class Player:
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

    playerStandRight = [pygame.image.load("./sprites/biker/idleRight/idle1.png"),
                        pygame.image.load("./sprites/biker/idleRight/idle2.png"),
                        pygame.image.load("./sprites/biker/idleRight/idle3.png"),
                        pygame.image.load("./sprites/biker/idleRight/idle4.png")]

    playerStandLeft = [pygame.image.load("./sprites/biker/idleLeft/idle1.png"),
                       pygame.image.load("./sprites/biker/idleLeft/idle2.png"),
                       pygame.image.load("./sprites/biker/idleLeft/idle3.png"),
                       pygame.image.load("./sprites/biker/idleLeft/idle4.png")]

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
        self.isJump = False
        self.jumpCount = 15
        self.left = False
        self.right = False
        self.lastMove = "right"
        self.hp = 300
        self.player_y_momentum = 0
        self.air_time = 0

    def get_x(self):
        return self.player_rect.x - self.player_rect.width / 1.5 - scroll[0]

    def get_y(self):
        return self.player_rect.y - self.player_rect.height / 3 - scroll[1]

    def draw_player(self, win):
        global animCount
        if animCount >= 30:
            animCount = 0
        if self.isJump:
            if self.lastMove == "right":
                win.blit(self.playerJumpR[animCount // 5], (self.get_x(), self.get_y()))
            else:
                win.blit(self.playerJumpL[animCount // 5], (self.get_x(), self.get_y()))
            animCount += 1
        elif self.right:
            win.blit(self.walkRight[animCount // 5], (self.get_x(), self.get_y()))
            animCount += 1
        elif self.left:
            win.blit(self.walkLeft[animCount // 5], (self.get_x(), self.get_y()))
            animCount += 1
        else:
            if self.lastMove == 'right':
                win.blit(self.playerStandRight[animCount // 8], (self.get_x(), self.get_y()))
            else:
                win.blit(self.playerStandLeft[animCount // 8], (self.get_x(), self.get_y()))
            animCount += 1
        print(animCount)
        man.health(win)

    def draw_collision_rect(self, win):
        pygame.draw.rect(win, "red",
                         pygame.Rect(self.get_x() + self.player_rect.width / 1.5,
                                     self.get_y() + self.player_rect.height / 3,
                                     self.player_rect.width, self.player_rect.height), 2)
        draw_text(str(int(self.hp / 3)) + "/100", health_font, "white", win, 80, 42)

    def health(self, win):
        pygame.draw.rect(win, "red", pygame.Rect(29, 29, 302, 32))
        pygame.draw.rect(win, "green", pygame.Rect(30, 30, self.hp, 30))


class bullet:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        self.bul_rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.get_x() + self.radius, self.get_y() + self.radius), self.radius)

    def get_x(self):
        return self.bul_rect.x - scroll[0]

    def get_y(self):
        return self.bul_rect.y - scroll[1]

    def draw_collision_rect(self, win):
        pygame.draw.rect(win, "blue", pygame.Rect(self.get_x(), self.get_y(), self.radius * 2, self.radius * 2), 2)


class Enemy:
    enemy_stand = pygame.image.load('./sprites/enemy/standing.png')
    enemy_walkR = []
    enemy_walkL = []
    for i in range(11):
        enemy_walkR.append(pygame.image.load(f'./sprites/enemy/walkRight/R{i + 1}E.png'))
        enemy_walkL.append(pygame.image.load(f'./sprites/enemy/walkLeft/L{i + 1}E.png'))

    def __init__(self, x, y, width, height):
        self.enemy_rect = pygame.Rect(x, y, width, height)
        self.move_count = 100
        self.gravity = 10
        self.right = False
        self.left = False

    def get_x(self):
        return self.enemy_rect.x - scroll[0]

    def get_y(self):
        return self.enemy_rect.y - scroll[1]

    def draw_enemy_rect(self, win):
        pygame.draw.rect(win, "blue",
                         pygame.Rect(self.get_x(), self.get_y(), self.enemy_rect.width, self.enemy_rect.height), 2)

    def move_enemy(self):
        self.enemy_rect, collision = move(self.enemy_rect, [0, self.gravity], tile_rect)
        if collision['bottom']:
            if self.move_count > 1:
                self.enemy_rect, collision = move(self.enemy_rect, [5, 10], tile_rect)
                self.right = True
                self.left = False
                self.move_count -= 1
            elif self.move_count == 1:
                self.move_count = -100
            elif self.move_count == -1:
                self.move_count = 100
            elif self.move_count < -1:
                self.enemy_rect, collision = move(self.enemy_rect, [-5, 10], tile_rect)
                self.right = False
                self.left = True
                self.move_count += 1

    def draw_enemy(self, win):
        global animCount

        if self.right:
            win.blit(self.enemy_walkR[animCount // 3],
                     (self.get_x() - self.enemy_rect.width / 2, self.get_y() + 5))
        elif self.left:
            win.blit(self.enemy_walkL[animCount // 3],
                     (self.get_x() - self.enemy_rect.width / 2, self.get_y() + 5))
        else:
            win.blit(self.enemy_stand,
                     (self.get_x() - self.enemy_rect.width / 2, self.get_y() + 5))


en1 = Enemy(500, 100, 32, 64)
enemy_rect1 = en1.enemy_rect
man = Player(display_width / 2 + 45, 100, 45, 60, 15)


def initialisation():
    global animCount, bgCount, tile_rect, bullets, scroll, man, en1, enemy_rect1
    animCount = 0
    bgCount = 0
    tile_rect = []
    bullets = []
    scroll = [0, 0]
    en1 = Enemy(500, 100, 32, 64)
    enemy_rect1 = en1.enemy_rect
    man = Player(display_width / 2 + 45, 100, 45, 60, 15)


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    map_game = []
    for row in data:
        map_game.append(list(row))
    return map_game


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


def draw_window():
    global bgCount

    screen.blit(bg1, (- scroll[0] / 10 - man.player_rect.width, -scroll[1] / 10))

    draw_tile()

    man.draw_player(screen)
    # en1.draw_enemy_rect(screen)
    en1.draw_enemy(screen)

    for bul in bullets:
        bul.draw(screen)
        # bul.draw_collision_rect(screen)

    # man.draw_collision_rect(screen)
    pygame.display.update()


def draw_text(text, font_rect, color, surface, x, y):
    text_obj = font_rect.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def pressed_key(keys):
    global animCount

    player_movement = [0, 0]
    if keys[pygame.K_d]:
        player_movement[0] += man.speed
        man.lastMove = "right"
        man.right = True
        man.left = False
    elif keys[pygame.K_a]:
        if man.player_rect.x > man.player_rect.width:
            player_movement[0] -= man.speed
            man.lastMove = "left"
            man.right = False
            man.left = True
    else:
        man.left = False
        man.right = False

    if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP]:
        face = 1 if keys[pygame.K_RIGHT] else -1 if keys[pygame.K_LEFT] else 0
        if len(bullets) < 100:
            bullets.append(bullet(round(man.player_rect.x + man.player_rect.width / 2),
                                  round(man.player_rect.y + man.player_rect.height / 2),
                                  5, (255, 0, 0), face))

    if keys[pygame.K_SPACE]:
        if man.air_time < 1:
            animCount = 0
            man.isJump = True
            man.player_y_momentum = -60

    player_movement[1] += man.player_y_momentum
    man.player_y_momentum += 10
    if man.player_y_momentum > 50:
        man.player_y_momentum = 50

    man.player_rect, collision = move(man.player_rect, player_movement, tile_rect)

    if collision['top']:
        man.player_y_momentum = 10
    if collision['bottom']:
        man.player_y_momentum = 0
        man.air_time = 0
        man.isJump = False
    else:
        man.air_time += 1

    if man.player_rect.colliderect(enemy_rect1):
        man.hp -= 10
    if man.hp == 0:
        draw_window()
        death()


def death():
    click = False
    display = pygame.Surface((display_width, display_height))
    display.fill("black")
    display.set_alpha(150)
    screen.blit(display, (0, 0))
    while True:
        clock.tick(30)
        pygame.time.delay(40)
        draw_text('YOU DIED', main_font, "red", screen, display_width / 2, display_height / 2)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(display_width // 2 - 100, 100, 200, 50)
        text = main_font.render("Main Menu", True, "red", "blue")
        screen.blit(text, button1)

        if button1.collidepoint((mx, my)):
            text = main_font.render("Main Menu", True, "blue", "red")
            screen.blit(text, button1)
            if click:
                main_menu()

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def pause():
    click = False
    display = pygame.Surface((display_width, display_height))
    display.fill("black")
    display.set_alpha(150)
    screen.blit(display, (0, 0))
    while True:
        clock.tick(30)
        pygame.time.delay(40)

        draw_text("PAUSE", main_font, "white", screen, display_width / 2, 30)

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(display_width // 2 - 100, 100, 200, 50)
        button2 = pygame.Rect(display_width / 2 - 100, 200, 200, 50)
        text_but1 = main_font.render("Main Menu", True, "red", "blue")
        text_but2 = main_font.render("Back", True, "red", "blue")
        screen.blit(text_but1, button1)
        screen.blit(text_but2, button2)

        if button1.collidepoint((mx, my)):
            text = main_font.render("Main Menu", True, "blue", "red")
            screen.blit(text, button1)
            if click:
                main_menu()
        if button2.collidepoint((mx, my)):
            text = main_font.render("Back", True, "blue", "red")
            screen.blit(text, button2)
            if click:
                game()

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game()
                if event.key == pygame.K_RETURN:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def main_menu():
    click = False
    while True:
        clock.tick(30)
        pygame.time.delay(40)

        screen.fill((0, 0, 0))

        initialisation()

        draw_text('main menu', main_font, (255, 255, 255),
                  screen, display_width // 2, 30)

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
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def option():
    while True:
        clock.tick(30)
        pygame.time.delay(40)

        screen.fill((0, 0, 0))
        draw_text('options', main_font, (255, 255, 255),
                  screen, display_width // 2, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        pygame.display.update()


def game():
    global animCount

    while True:
        clock.tick(60)
        pygame.time.delay(60)

        if man.player_rect.x >= (display_width / 2 + man.player_rect.width / 2):
            scroll[0] += int(man.player_rect.x - scroll[0] - display_width / 2 + man.player_rect.width / 2)

        if man.player_rect.y < (display_height / 2 + man.player_rect.height / 2):
            scroll[1] += int(man.player_rect.y - scroll[1] - display_height / 2 - man.player_rect.height / 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        for bul in bullets:
            if bul.vel != 0:
                if 1024 > bul.get_x() > 0:
                    bul.bul_rect, collision = move(bul.bul_rect, [bul.vel, 0], tile_rect)
                    if collision['top'] or collision['bottom'] or collision['right'] or collision['left']:
                        bullets.pop(bullets.index(bul))
                else:
                    bullets.pop(bullets.index(bul))
            else:
                if display_height > bul.bul_rect.y > 0:
                    bul.bul_rect, collision = move(bul.bul_rect, [0, -10], tile_rect)
                    if collision['top'] or collision['bottom'] or collision['right'] or collision['left']:
                        bullets.pop(bullets.index(bul))
                else:
                    bullets.pop(bullets.index(bul))

        keys = pygame.key.get_pressed()

        pressed_key(keys)

        en1.move_enemy()

        draw_window()


if __name__ == "__main__":
    main_menu()
