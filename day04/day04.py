from tqdm import tqdm
import re

FILENAME = './input'
# FILENAME = './example'


DIRECTIONS = [(-1, 1), (0, 1), (1, 1),
              (-1, 0),         (1, 0),
              (-1, -1), (0, -1), (1, -1)]

XMAS_STR = "XMAS"

def parse_data(filename):
    data = []
    with open(filename) as lines:
        for raw_line in lines:
            data.append(raw_line.rstrip())
    return data


def is_in_bounds(location, word_grid, offset=0):
    x, y = location
    return 0+offset <= x < len(word_grid)-offset and 0+offset <= y < len(word_grid[0])-offset


def search_for_string(start_location, search_string, word_grid):
    x, y = start_location
    number_of_matches = 0
    if word_grid[x][y] != search_string[0]:
        return 0
    else:
        for direction in DIRECTIONS:
            x, y = start_location
            is_matching = True
            for letter in search_string[1:]:
                x += direction[0]
                y += direction[1]
                if is_in_bounds((x, y), word_grid):
                    if letter != word_grid[x][y]:
                        is_matching = False
                        break
                else:
                    is_matching = False
                    break
            if is_matching:
                number_of_matches += 1
    return number_of_matches

# Searches for an X-shaped MAS all over the grid. The start location corresponds to the center of the X
def is_x_mas(start_location, word_grid):
    if is_in_bounds(start_location, word_grid, 1):
        x, y = start_location
        if word_grid[x][y] == 'A':
            diagonals = ['MS', 'SM']
            diag1 = word_grid[x-1][y-1] + word_grid[x+1][y+1]
            diag2 = word_grid[x-1][y+1] + word_grid[x+1][y-1]
            if diag1 in diagonals and diag2 in diagonals:
                return True
    return False


def run():
    data = parse_data(FILENAME)
    xmas_matches = 0
    x_mas_matches = 0
    for x in tqdm(range(len(data))):
        for y in range(len(data[0])):
            xmas_matches += search_for_string((x, y), XMAS_STR, data)
            x_mas_matches += 1 if is_x_mas((x, y), data) else 0
    print(f"Number of matches for {XMAS_STR} : {xmas_matches}")
    print(f"Number of matches for X-MAS : {x_mas_matches}")



if __name__ == '__main__':
    run()
