import pygame
import random
pygame.init()

# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

background = white

# screen
WIDTH = 400
HEIGHT = 500
fps = 60

# setting up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
kitty = pygame.transform.scale(pygame.image.load("assets/460943764_1920929601748572_5990187909699847586_n-removebg-preview.png"), (40, 150))

# game variables
kitty_x = 170
kitty_y = 180
kitty_width = 40  # set width and height according to sprite size
kitty_height = 150
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [265, 150, 70, 10]]  # platform coordinates
jump = False
y_change = 0  # controls player movement direction
x_change = 0
player_speed = 3

# Initialize game over variable
game_over = False  # Track whether the game is over

# check collisions with platforms
def check_collisions(rect_list):
    global kitty_x, kitty_y, y_change, jump
    kitty_rect = pygame.Rect(kitty_x, kitty_y, kitty_width, kitty_height)
    
    for platform in rect_list:
        # Platform collision: only detect from above
        if kitty_rect.colliderect(platform) and y_change > 0:  # kitty is falling
            # Check if kitty's feet are above the platform
            if kitty_y + kitty_height - y_change <= platform.top:
                kitty_y = platform.top - kitty_height  # place kitty on the platform
                y_change = 0  # reset vertical speed
                return True  # jump is now available
    
    return False

# updates the player's y position
def update_player(y_pos):
    global jump, y_change
    jump_height = 9
    gravity = 0.3
    if jump:
        y_change = -jump_height  # initiate upward jump
        jump = False
    y_pos += y_change
    y_change += gravity  # apply gravity after updating position
    return y_pos

# infinite jumper
def update_platforms(my_list, y_pos, change):
    if y_pos < 250 and change < 0:  # only when you are going higher
        for i in range(len(my_list)):
            my_list[i][1] -= change  # move platforms downwards when high enough

    for i in range(len(my_list)):
        if my_list[i][1] > HEIGHT:  # if a platform goes below the screen, reset it to the top
            my_list[i] = [random.randint(10, WIDTH - 70), random.randint(-75, -35), 70, 10]  # randomize platform # -70 , -30 represets how often they appear
    
    return my_list  # return the modified list

# create a clock object to control the frame rate
timer = pygame.time.Clock()

# main game loop
running = True
while running:

    screen.fill(background)
    
    # Check if kitty falls out of the screen
    if kitty_y > HEIGHT:
        game_over = True
    
    if game_over:
        # Display Game Over message
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render('Game Over', True, black)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))

        restart_text = font.render('Press Space to Restart', True, black)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))

        # Wait for space to restart the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # reset variables to initial values
                kitty_x, kitty_y = 170, 180
                y_change = 0
                x_change = 0
                game_over = False

        pygame.display.flip()
        timer.tick(fps)
        continue  # skip the rest of the loop when game over

    # blit (draw) the kitty image
    screen.blit(kitty, (kitty_x, kitty_y))  # ensure it's drawn on the screen
    
    blocks_2 = []  # to hold platform blocks
    for platform in platforms:  # drawing the platforms
        block = pygame.draw.rect(screen, black, platform, 0, 3)  # platform shape
        blocks_2.append(block)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_change = -player_speed
            if event.key == pygame.K_d:
                x_change = player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                x_change = 0

    # update the player's position
    kitty_y = update_player(kitty_y)  # update vertical position based on gravity and jump
    jump = check_collisions(blocks_2)  # check for platform collisions
    
    # apply horizontal movement
    kitty_x += x_change
    
    # update platforms
    platforms = update_platforms(platforms, kitty_y, y_change)
    
    # player face
    kitty_image = pygame.transform.scale(pygame.image.load("assets/460943764_1920929601748572_5990187909699847586_n-removebg-preview.png"), (40, 150))
    if x_change > 0:
        kitty = kitty_image
    elif x_change < 0: 
        kitty = pygame.transform.flip(kitty_image, True, False)  # flips, makes left look left vice versa
    
    # update the display
    pygame.display.flip()

    # control the frame rate
    timer.tick(fps)
    
pygame.quit()
