# Ashna Jain
# H370 Final Project: Sorting Game w/ Hand Detection
# May 6th, 2023
import pygame
import random


# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34,139,34)
RED = (205,92,92)


HOME_SCREEN = 1
INTR_SCREEN = 2
GAME_SCREEN = 3
SCORE_SCREEN = 4
EXIT_SCREEN = 5
ALL_DONE_SCREEN = 6

currentScreen = HOME_SCREEN
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 600
score = 0

class Paper(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("paper.png").convert()
        self.rect = self.image.get_rect()
        self.recycleable = True

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("apple.png").convert()
        self.rect = self.image.get_rect()
        self.recycleable = False

class Trashcan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("trashcan.jpg").convert()
        self.rect = self.image.get_rect()
        self.canRecycle = False

class RecycleBin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("recyclebin.jpeg").convert()
        self.rect = self.image.get_rect()
        self.canRecycle = True

class RedBlock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 15])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

class Player(RedBlock):
    #each player has a list of item that it is carrying
    carry_item_list = []

    #update function 
    def update(self):
        pos = pygame.mouse.get_pos()
        diff_x = self.rect.x - pos[0]
        diff_y = self.rect.y - pos[1]

        for item in self.carry_item_list:
            item.rect.x -= diff_x
            item.rect.y -= diff_y

        self.rect.x = pos[0]
        self.rect.y = pos[1]

def score_print():
        font = pygame.font.SysFont('Comic Sans MS', 50)
        text = font.render("Score = " + str(score), False, BLACK)
        screen.blit(text, (370, 470))

def HomeScreen():
    global currentScreen
    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))
    screen.blit(background, [0, 0])

    go_button = pygame.Rect(330, 400, 150, 100)  # creates a rect object
    exit_button = pygame.Rect(530, 400, 150, 100)

    pygame.draw.rect(screen, GREEN, go_button)  # draw button on screen
    pygame.draw.rect(screen, RED, exit_button)  # draw button on screen

    go_exit_font = pygame.font.SysFont('Comic Sans MS', 45)
    go_banner = go_exit_font.render("PLAY!", False, WHITE)
    exit_banner = go_exit_font.render('EXIT', False, WHITE)

    screen.blit(go_banner, (344, 420))
    screen.blit(exit_banner, (544, 420))


    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                currentScreen = ALL_DONE_SCREEN

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the PLAY button
                if go_button.collidepoint(mouse_pos):
                    done = True
                    currentScreen = GAME_SCREEN
                #is mouse over the EXIT button
                if exit_button.collidepoint(mouse_pos):
                    done = True
                    currentScreen = ALL_DONE_SCREEN

        pygame.display.update()
        clock.tick(60)

def scoreScreen():
    global score
    global currentScreen

    background = pygame.image.load("background_game.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))
    screen.blit(background, [0, 0])

    pygame.mouse.set_visible(True)
    font = pygame.font.SysFont('Comic Sans MS', 70)
    text = font.render("Score = " + str(score), False, BLACK)
    screen.blit(text, (330, 100))

    replay_button = pygame.Rect(300, 300, 170, 100)  # creates a rect object
    exit_button = pygame.Rect(550, 300, 170, 100)

    pygame.draw.rect(screen, GREEN, replay_button)  # draw button on screen
    pygame.draw.rect(screen, RED, exit_button)  # draw button on screen

    go_exit_font = pygame.font.SysFont('Comic Sans MS', 40)
    replay_banner = go_exit_font.render("REPLAY!", False, WHITE)
    exit_banner = go_exit_font.render('EXIT', False, WHITE)

    screen.blit(replay_banner, (310, 320))
    screen.blit(exit_banner, (585, 320))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                currentScreen = ALL_DONE_SCREEN

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button
                if replay_button.collidepoint(mouse_pos):
                    done = True
                    currentScreen = GAME_SCREEN

                if exit_button.collidepoint(mouse_pos):
                    done = True
                    currentScreen = ALL_DONE_SCREEN

        pygame.display.update()
        clock.tick(60)

def GameScreen():
    #set up locations of all game objects
    item_list = pygame.sprite.Group()
    bin_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()

    trashcan = Trashcan()
    trashcan.rect.x = 150
    trashcan.rect.y = 340
    all_sprites_list.add(trashcan)
    bin_list.add(trashcan)
    
    recycleBin = RecycleBin()
    recycleBin.rect.x = 650
    recycleBin.rect.y = 300
    all_sprites_list.add(recycleBin)
    bin_list.add(recycleBin)

    for i in range(10):
        pictures = [Paper(), Apple()]
        item = random.choice(pictures)

        placed = False
        while not placed:
            item.rect.x = random.randrange(10, screen_width-10)
            item.rect.y = random.randrange(screen_height - 300)
            item_collide_list = pygame.sprite.spritecollide(item, item_list, False) #items that collided with other items
            bin_collide_list = pygame.sprite.spritecollide(item, bin_list, False) #items that collided with any bins
            if len(item_collide_list) == 0 and len(bin_collide_list) == 0:
                item_list.add(item)
                all_sprites_list.add(item)
                placed = True

    player = Player()
    all_sprites_list.add(player)

    return [item_list, bin_list, player, all_sprites_list]

def Game():
    global currentScreen
    global score

    score = 0
    start_time = 2
    frame_rate = 60
    my_frame_count = 0

    item_list, bin_list, player, all_sprites_list = GameScreen()


    # -------- Main Game Loop -----------
    done = False
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.carry_item_list = pygame.sprite.spritecollide(player, item_list, False)

            elif event.type == pygame.MOUSEBUTTONUP:
                bin_hit_list = pygame.sprite.spritecollide(player, bin_list, False)
                if len(bin_hit_list) != 0:
                    for item in player.carry_item_list:
                        if item.recycleable == bin_hit_list[0].canRecycle:
                            score += 1
                        else:
                            score -= 1
                        item_list.remove(item)
                        all_sprites_list.remove(item)
                    print(score)
                player.carry_item_list = []

        all_sprites_list.update()
        screen.fill(WHITE)
        all_sprites_list.draw(screen)
        score_print()
        my_font = pygame.font.Font(None, 25)
        # --- Timer going down ---
        # Calculate total seconds
        total_seconds = start_time - (my_frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0
            done = True
            currentScreen = SCORE_SCREEN

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        time = "Time left: {0:02}:{1:02}".format(minutes, seconds)
        text_text = my_font.render(time, True, BLACK)
        screen.blit(text_text, (420, 550))

        my_frame_count += 1
        clock.tick(frame_rate)
        pygame.display.flip()

# ------------------------------------------------------------Main Loop--------------------------------------------------

pygame.init()
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

while currentScreen != ALL_DONE_SCREEN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            currentScreen = ALL_DONE_SCREEN
    if currentScreen == HOME_SCREEN:
        HomeScreen()
    if currentScreen == GAME_SCREEN:
        Game()
    if currentScreen == SCORE_SCREEN:
        scoreScreen()
    if currentScreen == EXIT_SCREEN:
        print("ALL DONE")
    pygame.display.flip()
    clock.tick(60)
pygame.quit()


