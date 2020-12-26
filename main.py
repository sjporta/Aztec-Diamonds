import pygame
from random import random

pygame.init()
pygame.mixer.init()
board_width, board_height = 24, 24
square_width = 32
width, height = square_width * board_width, square_width * board_height
block = pygame.image.load('block.png')
l, r, u, d = tuple(pygame.image.load(f'{i}.png') for i in ['l', 'r', 'u', 'd'])

def board_coords_to_blip_coords(x, y):
    return (square_width * (board_width // 2 - 1) + square_width * x,
            square_width * board_height // 2 - square_width * y)

def generate_blocks_in_board(size):
    """
    Generates the coordinates for the blocks in an Aztec board of size size.
    In a board of size 1, (0, 0) is the bottom left block.
    """
    for i in range(-size + 1, size + 1):
        for j in range(-size + 1, size + 1):
            taxi = abs(i) + abs(j)
            if taxi <= size - 1:
                yield (i, j)

            # Prevents extra from being generated in the bottom left
            elif taxi == size and (i > 0 or j > 0):
                yield (i, j)

            # Prevents extra from being generated elsewhere
            # other than the top right
            elif taxi == size + 1 and i > 0 and j > 0:
                yield(i, j)

def update_board(blocks, size, win):
    """
    Updates the board, re-painting the tiles and dominoes.
    """
    win.fill('black')

    for i, j in generate_blocks_in_board(size):
        c = board_coords_to_blip_coords(i, j)
        win.blit(block, c)

    for b, x, y in blocks:
        coords = board_coords_to_blip_coords(x, y)
        win.blit(b, coords)

    pygame.display.update()

def check_collisions(blocks):
    """
    Loops through all the items in blocks, checking
    :param blocks:
    :return:
    """
    s = set(b for b in blocks)
    collided = set()

    for b, x, y in blocks:
        if b is l and (r, x - 1, y) in s:
            collided.add((b, x, y))
        elif b is r and (l, x + 1, y) in s:
            collided.add((b, x, y))
        elif b is u and (d, x, y + 1) in s:
            collided.add((b, x, y))
        elif b is d and (u, x, y - 1) in s:
            collided.add((b, x, y))

    for b, x, y in collided:
        blocks.remove((b, x, y))

    return collided

def remove_collided(collided, win):
    """
    Read the name.
    """
    for b, x, y in collided:
        if b is l or b is r:
            win.blit(block, board_coords_to_blip_coords(x, y))
            win.blit(block, board_coords_to_blip_coords(x, y - 1))
        else:
            win.blit(block, board_coords_to_blip_coords(x, y))
            win.blit(block, board_coords_to_blip_coords(x + 1, y))

    pygame.display.update()

def slide(blocks):
    """
    Calculates the new positions for the blocks, after sliding
    """
    temp = []

    for b, x, y in blocks:
        if b is l:
            temp.append((b, x - 1, y))
        elif b is r:
            temp.append((b, x + 1, y))
        elif b is u:
            temp.append((b, x, y + 1))
        else:
            temp.append((b, x, y - 1))

    return temp


def get_coords_of_empty_2x2s(blocks, size):
    """
    Read the name.
    """
    seen = set()
    for b, x, y in blocks:
        if b is l or b is r:
            seen.add((x, y))
            seen.add((x, y - 1))
        else:
            seen.add((x, y))
            seen.add((x + 1, y))

    ret = []

    for x, y in generate_blocks_in_board(size):
        if (x, y) not in seen:
            ret.append((x, y))
            seen.add((x, y + 1))
            seen.add((x + 1, y + 1))
            seen.add((x + 1, y))

    return ret

def randomize_empty_blocks(empty):
    """
    Taking a list of the coordinates of the bottom-left tile of an empty 2x2
    block, fills in the tiles with random opposite facing pairs.
    """
    ret = []
    for x, y in empty:
        if random() < 0.5:
            ret.append((l, x, y + 1))
            ret.append((r, x + 1, y + 1))
        else:
            ret.append((d, x, y))
            ret.append((u, x, y + 1))

    return ret

def play():
    win = pygame.display.set_mode((width, height))

    blocks = randomize_empty_blocks([(0, 0)])
    size = 1
    update_board(blocks, 1, win)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return

                elif event.key == pygame.K_r:
                    blocks = randomize_empty_blocks([(0, 0)])
                    size = 1
                    update_board(blocks, 1, win)

                elif event.key == pygame.K_RETURN:
                    size += 1
                    update_board(blocks, size, win)
                    pygame.time.delay(1000)

                    collided = check_collisions(blocks)
                    remove_collided(collided, win)
                    pygame.time.delay(1000)

                    blocks = slide(blocks)
                    update_board(blocks, size, win)
                    pygame.time.delay(1000)

                    empty = get_coords_of_empty_2x2s(blocks, size)
                    new = randomize_empty_blocks(empty)
                    for b in new:
                        blocks.append(b)
                    update_board(blocks, size, win)
                    pygame.time.delay(500)



if __name__ == '__main__':
    # pygame.quit()
    play()