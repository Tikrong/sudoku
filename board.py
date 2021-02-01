import pygame

from sudoku import *

pygame.init()

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

#fonts
numbers_font = pygame.font.SysFont('verdana', 24)

#screen size
screen_height = 600
screen_width = 450

# sizes
tile_size = 50

screen = pygame.display.set_mode((screen_width, screen_height))

#load sudoku assignment
sudoku = Sudoku("structure0.txt")
solver = SudokuSolver(sudoku)
initial_state = solver.grid(solver.sudoku.initial_assignment)

solution = solver.grid(solver.sudoku.initial_assignment)
status = ""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw cells
    for i in range(9):
        for j in range(9):
            rect = pygame.Rect(j*tile_size, i*tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, WHITE, rect, 1)

            #print initial assignment
            if initial_state[i][j]:
                number = numbers_font.render(str(initial_state[i][j]), False, WHITE)
                numberRect = number.get_rect()
                numberRect.center = rect.center
                screen.blit(number, numberRect)

            elif solution[i][j]:
                number = numbers_font.render(str(solution[i][j]), False, GREEN)
                numberRect = number.get_rect()
                numberRect.center = rect.center
                screen.blit(number, numberRect)

            

    # draw 3x3 red squares
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(j*tile_size*3, i*tile_size*3, 3*tile_size, 3*tile_size)
            pygame.draw.rect(screen, RED, rect, 1)

    # draw main boundary
    rect = pygame.Rect(0, 0, 9*tile_size, 9*tile_size)
    pygame.draw.rect(screen, WHITE, rect, 1)

    # UI
    # Draw button
    Solve_Button = pygame.Rect(3*tile_size, 10*tile_size, 3*tile_size, tile_size)
    Solve_Text = numbers_font.render("SOLVE", False, GREEN)
    Solve_Text_Rect = Solve_Text.get_rect()
    Solve_Text_Rect.center = Solve_Button.center
    pygame.draw.rect(screen, WHITE, Solve_Button, 1)
    screen.blit(Solve_Text, Solve_Text_Rect)

    # Draw status bar
    Status_Text = numbers_font.render(status, False, WHITE)
    Status_Text_Rect = Status_Text.get_rect()
    #Status_Text_Rect.top = Solve_Button.bottom + tile_size * 0.5
    #Status_Text_Rect.left = Solve_Button.left
    Status_Text_Rect.center = Solve_Button.center
    Status_Text_Rect.top = Status_Text_Rect.top + tile_size * 1
    
    screen.blit(Status_Text, Status_Text_Rect)

    # Check if button is clicked
    click, _, _ = pygame.mouse.get_pressed()
    if click == True:
        mouse = pygame.mouse.get_pos()
        if Solve_Button.collidepoint(mouse):
            #send event that we need to solve the puzzle
            assignment = solver.solve()
            if assignment is None:
                status = "NO SOLUTION"
            else:
                status = "SOLVED"
                solution = solver.grid(assignment)
                print(solver.counter)


    # update everything on the screen
    pygame.display.flip()

pygame.quit()

