import time

import pygame
import sys
import random


# =====================
# Classes
# =====================
class Piece:
    def __init__(self, tiles, rgbColor):
        self.tiles = tiles
        self.color = rgbColor


# =====================
# Functions
# =====================
def SpawnPiece(pieces, SpawnPos):
    global SelectedPiece, grid, currentPieceTiles, pos, gameOver, NextUp
    # Use the NextUp piece as the current piece
    current_idx = NextUp
    piece = pieces[current_idx]

    # Generate the next piece for preview
    NextUp = random.randint(0, len(pieces) - 1)

    SelectedPiece.clear()
    currentPieceTiles = [tile[:] for tile in piece.tiles]
    pos = SpawnPos  # SpawnPos should be [y, x]

    for tile in currentPieceTiles:
        if grid[tile[0] + pos[0]][tile[1] + pos[1]] != 0:
            print("Game Over")
            gameOver = True
            return current_idx

    for tile in currentPieceTiles:
        y = tile[0] + pos[0]
        x = tile[1] + pos[1]
        grid[y][x] = 1
        SelectedPiece.append([y, x])

    return current_idx


def Move(dx, dy, lock_on_fail=False):
    global SelectedPiece, grid, pos

    if not SelectedPiece:
        return False

    for y, x in SelectedPiece:
        ny = y + dy
        nx = x + dx

        if nx < 0 or nx >= grid_width or ny < 0 or ny >= grid_height:
            if lock_on_fail:
                lock_piece()
            return False

        if grid[ny][nx] == 2:
            if lock_on_fail:
                lock_piece()
            return False

    for y, x in SelectedPiece:
        grid[y][x] = 0

    for i in range(len(SelectedPiece)):
        SelectedPiece[i][0] += dy
        SelectedPiece[i][1] += dx

    pos[0] += dy
    pos[1] += dx

    for y, x in SelectedPiece:
        grid[y][x] = 1

    return True


def lock_piece():
    global SelectedPiece
    for y, x in SelectedPiece:
        grid[y][x] = 2
    SelectedPiece.clear()
    CheckLine()  # Check for completed lines after locking
    CheckLine(True)


def HardDrop():
    """Drop the piece instantly to the lowest possible position"""
    global SelectedPiece, needNewPiece

    if not SelectedPiece:
        return

    # Keep moving down until we can't anymore
    while Move(gravity_dir[0], gravity_dir[1], False):
        pass

    # Lock the piece in place
    lock_piece()
    needNewPiece = True


def Rotate(rot):
    global SelectedPiece, grid, currentPieceTiles, pos

    if not SelectedPiece:
        return rot

    # O-piece does not rotate
    if len(currentPieceTiles) == 4 and currentPieceTiles == [[0, 0], [0, 1], [1, 0], [1, 1]]:
        return rot

    # Remove current piece from grid
    for y, x in SelectedPiece:
        grid[y][x] = 0

    # Use SECOND tile as pivot (classic & safe)
    pivot = currentPieceTiles[1]

    rotated = []
    for y, x in currentPieceTiles:
        ry = y - pivot[0]
        rx = x - pivot[1]

        ny = -rx
        nx = ry

        rotated.append([ny + pivot[0], nx + pivot[1]])

    newSelected = []
    for y, x in rotated:
        gy = y + pos[0]
        gx = x + pos[1]

        if gx < 0 or gx >= grid_width or gy < 0 or gy >= grid_height or grid[gy][gx] == 2:
            for oy, ox in SelectedPiece:
                grid[oy][ox] = 1
            return rot

        newSelected.append([gy, gx])

    currentPieceTiles[:] = rotated
    SelectedPiece[:] = newSelected

    for y, x in SelectedPiece:
        grid[y][x] = 1

    return (rot + 1) % 4


def CheckLine(Vertical=False):
    global grid
    lines_cleared = 0

    if not Vertical:
        # Check horizontal lines
        for row in range(grid_height):
            if all(grid[row][x] == 2 for x in range(grid_width)):
                # Clear the line
                grid[row] = [0] * grid_width
                lines_cleared += 1
                # Move every block above the line one down
                for y in range(row, 0, -1):
                    grid[y] = grid[y - 1][:]
                # Clear the top row
                grid[0] = [0] * grid_width
    else:
        # Check vertical lines
        for col in range(grid_width):
            if all(grid[y][col] == 2 for y in range(grid_height)):
                # Clear the column
                for y in range(grid_height):
                    grid[y][col] = 0
                lines_cleared += 1
                # Shift all blocks to the left of this column one to the right
                for x in range(col, grid_width - 1):
                    for y in range(grid_height):
                        grid[y][x] = grid[y][x + 1]
                # Clear the rightmost column
                for y in range(grid_height):
                    grid[y][grid_width - 1] = 0

    return lines_cleared


def DrawNextPiece():
    """Draw the next piece preview on the right side of the screen"""
    global NextUp, Pieces, screen, box_size, grid_width

    # Preview box position
    preview_x = grid_width * box_size + 10
    preview_y = 100
    preview_box_size = 30

    # Draw "NEXT" label
    next_font = pygame.font.Font(None, 40)
    next_text = next_font.render("NEXT", True, (255, 255, 255))
    screen.blit(next_text, (preview_x, preview_y - 50))

    # Draw preview background
    pygame.draw.rect(screen, (50, 50, 50),
                     (preview_x, preview_y, preview_box_size * 4, preview_box_size * 4))

    # Get the next piece
    next_piece = Pieces[NextUp]

    # Draw the next piece centered in the preview box
    for tile in next_piece.tiles:
        draw_y = tile[0] + 2  # Center vertically
        draw_x = tile[1] + 2  # Center horizontally

        pygame.draw.rect(
            screen,
            next_piece.color,
            (preview_x + draw_x * preview_box_size,
             preview_y + draw_y * preview_box_size,
             preview_box_size,
             preview_box_size)
        )


def DrawUI(col):
    """Draw UI background rectangle on the right side"""
    global screen, box_size, grid_width, grid_height
    # Correct syntax: pygame.draw.rect(surface, color, (x, y, width, height))
    pygame.draw.rect(
        screen,
        col,  # Color should be a tuple like (255, 255, 255)
        (box_size * grid_width, 0, box_size * 4, grid_height * box_size)  # Rectangle position and size
    )


# =====================
# Main Code
# =====================

# Init Pygame
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)  # None uses default font

box_size = 35
grid_width = 20
grid_height = 26
gravity = 0.3
gravity_dir = [0, 1]
moveSpeed = 0.15
GravityChangeSpeed = 10
rotation = 0

screen = pygame.display.set_mode((grid_width * box_size + box_size * 4, grid_height * box_size))
pygame.display.set_caption("Tetris")

grid = [[0] * grid_width for _ in range(grid_height)]

SelectedPiece = []
currentPieceTiles = []
pos = [1, grid_width // 2]  # Changed initial position to center

Pieces = [
    Piece([[-1, 0], [0, 0], [1, 0], [2, 0]], (0, 255, 255)),  # I
    Piece([[0, 0], [1, 0], [0, 1], [1, 1]], (255, 255, 0)),  # O
    Piece([[-1, 0], [0, 0], [1, 0], [0, 1]], (128, 0, 128)),  # T
    Piece([[0, 0], [1, 0], [-1, 1], [0, 1]], (0, 255, 0)),  # S
    Piece([[-1, 0], [0, 0], [0, 1], [1, 1]], (255, 0, 0)),  # Z
    Piece([[-1, 0], [0, 0], [1, 0], [1, 1]], (0, 0, 255)),  # J
    Piece([[-1, 0], [0, 0], [1, 0], [-1, 1]], (255, 165, 0)),  # L
    Piece([[0, 0], [0, -1], [1, -1], [0, 1], [1, 1]], (137, 168, 50))  # C
]

SelectedPieceID = None
NextUp = random.randint(0, len(Pieces) - 1)  # Initialize with random piece

gravityTimer = 0
moveTimer = 0
GravityChangeTimer = 0
GCTFont = font.render(f"{GravityChangeTimer}", True, (255, 255, 255))
hold = False
lastKey = None
needNewPiece = True
gameOver = False
running = True

# Game Loop
while running:
    dt = clock.get_time() / 1000
    gravityTimer += dt
    moveTimer += dt
    GravityChangeTimer += dt / 1.5
    GCTFont = font.render(f"{round(GravityChangeTimer)}/{round(GravityChangeSpeed * 100) / 100}", True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            lastKey = event.key
            hold = True
            moveTimer = moveSpeed
            if event.key == pygame.K_UP:
                rotation = Rotate(rotation)
            elif event.key == pygame.K_RETURN:  # Hard drop on Enter
                HardDrop()

        if event.type == pygame.KEYUP:
            hold = False
            lastKey = None

    if gravityTimer >= gravity:
        gravityTimer = 0
        if not Move(gravity_dir[0], gravity_dir[1], True):
            needNewPiece = True

    if hold:
        if moveTimer >= moveSpeed:
            moveTimer = 0
            if lastKey == pygame.K_LEFT:
                Move(gravity_dir[1] * -1, gravity_dir[0])
            elif lastKey == pygame.K_RIGHT:
                Move(gravity_dir[1], gravity_dir[0] * -1)
        elif moveTimer >= moveSpeed / 2:
            if lastKey == pygame.K_DOWN:
                Move(gravity_dir[0], gravity_dir[1], True)

    if needNewPiece:
        spos = [0, 0]
        if gravity_dir[0] == 0:
            if gravity_dir[1] != -1:
                spos = [1, grid_width // 2]
            else:
                spos = [grid_width - 1, grid_height // 2]
        elif gravity_dir[0] == 1:
            spos = [grid_height // 2, 1]
        elif gravity_dir[0] == -1:
            spos = [grid_height // 2, grid_width - 1]
        SelectedPieceID = SpawnPiece(Pieces, spos)
        needNewPiece = False

    if GravityChangeTimer >= GravityChangeSpeed:
        GravityChangeTimer = 0.0
        gravity_dir = [gravity_dir[1], gravity_dir[0]]
        GravityChangeSpeed -= 0.1  # Make it more chatoting evry second

    screen.fill((30, 30, 30))

    # Draw UI background
    DrawUI((60, 60, 60))  # Dark gray background for UI area

    screen.blit(GCTFont, (0, 0))

    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] == 1:
                pygame.draw.rect(
                    screen,
                    Pieces[SelectedPieceID].color,
                    (x * box_size, y * box_size, box_size, box_size),
                )
            elif grid[y][x] == 2:
                pygame.draw.rect(
                    screen,
                    (148, 148, 148),
                    (x * box_size, y * box_size, box_size, box_size),
                )

    # Draw the next piece preview
    DrawNextPiece()

    if gameOver:
        bigFont = pygame.font.Font(None, 100)  # None uses default font
        Lose = bigFont.render("Game Over!", True, (255, 0, 0))
        screen.blit(Lose, (float(screen.get_width()) // 3.0, float(screen.get_height()) // 3.0))
        pygame.display.flip()
        time.sleep(5)
        running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()