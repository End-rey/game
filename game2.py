import pygame

pygame.init()

display_width = 1549 / 2
display_height = 516

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Game")

bg1 = pygame.image.load("./sprites/bg3.png")

clock = pygame.time.Clock()

animCount = 0
bgCount = 0
game = True


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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed


def draw_window(man: Player):
    global animCount, bgCount

    screen.blit(bg1, (-man.x - man.width // 2, 0))

    if animCount >= 30:
        animCount = 0

    if man.isJump:
        if man.lastMove == "right":
            screen.blit(man.playerJumpR[animCount // 5], (man.x, man.y))
        else:
            screen.blit(man.playerJumpL[animCount // 5], (man.x, man.y))
        animCount += 1
    elif man.right:
        screen.blit(man.walkRight[animCount // 5], (man.x, man.y))
        animCount += 1
    elif man.left:
        screen.blit(man.walkLeft[animCount // 5], (man.x, man.y))
        animCount += 1
    else:
        screen.blit(man.playerStand[animCount // 8], (man.x, man.y))
        animCount += 1
    print(animCount)
    pygame.display.update()


def pressed_key(man: Player, keys):
    global animCount, game
    if keys[pygame.K_ESCAPE]:
        game = False

    if keys[pygame.K_d]:
        if man.x < display_width - man.width / 2:
            man.x += man.speed
            man.lastMove = "right"
            man.right = True
            man.left = False
    elif keys[pygame.K_a]:
        if man.x > - man.width / 2:
            man.x -= man.speed
            man.lastMove = "left"
            man.right = False
            man.left = True
    else:
        man.left = False
        man.right = False

    if not man.isJump:
        if keys[pygame.K_SPACE]:
            man.isJump = True
            animCount = 0
    else:
        if man.jumpCount >= -15:
            if man.jumpCount < 0:
                man.y += (man.jumpCount ** 2) / 3
            else:
                man.y -= (man.jumpCount ** 2) / 3
            man.jumpCount -= 2
        else:
            man.isJump = False
            man.jumpCount = 15


def main():
    global animCount, game
    man = Player(50, display_height - 100, 100, 100, 5)
    while game:
        clock.tick(30)
        pygame.time.delay(40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        keys = pygame.key.get_pressed()

        pressed_key(man, keys)

        draw_window(man)


if __name__ == "__main__":
    main()
