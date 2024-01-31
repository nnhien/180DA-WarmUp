import random
import pygame
from pygame.locals import (
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    MOUSEBUTTONUP,
    QUIT,
)

valid_moves = ['r', 'p', 's']

RECT_HEIGHT = 150
RECT_WIDTH = 150
RECT_PADDING = 100

SCREEN_PADDING = 25
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# returns whether user wins: 
#   1 for win
#   0 for tie
#   -1 for lose
def check_win(bot_move, user_move):
    # Maps to a tuple for results of particular user move (win, lose, tie)
    bot_move_results = {
        'r': ('p', 's', 'r'),
        'p': ('s', 'r', 'p'),
        's': ('r', 'p', 's'),
    }

    result = bot_move_results[bot_move]
    if user_move == result[0]:
        return 1
    if user_move == result[1]:
        return -1
    return 0

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))

rock_surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
rock_surface.fill((0, 0, 0))

paper_surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
paper_surface.fill((0, 0, 0))

scissors_surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
scissors_surface.fill((0, 0, 0))

font = pygame.font.SysFont('Helvetica', 20)

rock_text = font.render("Rock", True, (0, 0, 0))
paper_text = font.render("Paper", True, (0, 0, 0))
scissors_text = font.render("Scissors", True, (0, 0, 0))

screen.blit(rock_text, (SCREEN_PADDING, SCREEN_HEIGHT / 2 - 32))
screen.blit(paper_text, (SCREEN_PADDING + RECT_WIDTH + RECT_PADDING, SCREEN_HEIGHT / 2 - 32))
screen.blit(scissors_text, (SCREEN_PADDING + RECT_WIDTH + RECT_PADDING + RECT_WIDTH + RECT_PADDING, SCREEN_HEIGHT / 2 - 32))

r_rect = screen.blit(rock_surface, (SCREEN_PADDING, SCREEN_HEIGHT / 2))
p_rect = screen.blit(paper_surface, (SCREEN_PADDING + RECT_WIDTH + RECT_PADDING, SCREEN_HEIGHT / 2))
s_rect = screen.blit(scissors_surface, (SCREEN_PADDING + RECT_WIDTH + RECT_PADDING + RECT_WIDTH + RECT_PADDING, SCREEN_HEIGHT / 2))

buttons = [(rock_surface, r_rect), (paper_surface, p_rect), (paper_surface, s_rect)]

pygame.display.flip()

result_text = None

def handle_selection(mouse_pos):
    user_move = None

    for i, (_, rect) in enumerate(buttons):
        if rect.collidepoint(mouse_pos):
            match i:
                case 0:
                    user_move = 'r'
                    break
                case 1:
                    user_move = 'p'
                    break
                case 2:
                    user_move = 's'
                    break
    
    if user_move == None:
        return

    bot_move = random.choice(valid_moves)
    user_won = check_win(bot_move, user_move)

    match user_won:
        case 1:
            text = "You win! Press Enter to reset"
        case 0:
            text = "You tied. Press Enter to reset"
        case -1:
            text = "You lost... Press Enter to reset"

    result_text = font.render(text, True, (0, 0, 0))
    screen.blit(result_text, (SCREEN_PADDING, SCREEN_PADDING))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_RETURN:
                if result_text != None:
                    result_text = None
                screen.fill((255, 255, 255))
                screen.blit(rock_text, (SCREEN_PADDING, SCREEN_HEIGHT / 2 - 32))
                screen.blit(paper_text, (SCREEN_PADDING + RECT_WIDTH + RECT_PADDING, SCREEN_HEIGHT / 2 - 32))
                screen.blit(scissors_text, (SCREEN_PADDING + RECT_WIDTH + RECT_PADDING + RECT_WIDTH + RECT_PADDING, SCREEN_HEIGHT / 2 - 32))
        elif event.type == MOUSEBUTTONUP:
            if result_text == None:
                handle_selection(pygame.mouse.get_pos())
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
    
    mouse_pos = pygame.mouse.get_pos()
    for (surface, rect) in buttons:
        if rect.collidepoint(mouse_pos):
            surface.fill((0, 255, 0))
        else:
            surface.fill((0, 0, 0))
        screen.blit(surface, (rect.x, rect.y))
    pygame.display.flip()
    