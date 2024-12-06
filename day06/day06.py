import copy

from tqdm import tqdm
import re

FILENAME = './input'
# FILENAME = './example'

LAB_SPACE = '.'
OBSTRUCTION = '#'
GUARD_START = "^"

# Directions go clockwise : up, right, down, left
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_data(filename):
    data = []
    with open(filename) as lines:
        for raw_line in lines:
            data.append(raw_line.rstrip())
    return data


def find_initial_guard_location(lab_map):
    for x in range(len(lab_map)):
        for y in range(len(lab_map[x])):
            if lab_map[x][y] == GUARD_START:
                return x, y
    return None


def is_in_bounds(location, lab_map):
    x, y = location
    return 0 <= x < len(lab_map) and 0 <= y < len(lab_map[x])


def do_guard_step(lab_map, location, direction):
    x, y = location
    dir_x, dir_y = DIRECTIONS[direction]
    new_x, new_y = x + dir_x, y + dir_y
    if is_in_bounds((new_x, new_y), lab_map):
        if lab_map[new_x][new_y] in (LAB_SPACE, GUARD_START):
            return (new_x, new_y), direction
        else:
            # guard met an obstruction
            while lab_map[new_x][new_y] == OBSTRUCTION:
                direction = (direction + 1) % len(DIRECTIONS)  # turn right
                dir_x, dir_y = DIRECTIONS[direction]
                new_x, new_y = x + dir_x, y + dir_y
            return (new_x, new_y), direction
    else:
        return None, direction


def do_guard_walk(lab_map):
    current_x, current_y = find_initial_guard_location(lab_map)
    direction = 0
    walked_squares = {((current_x, current_y), direction)}
    guard_has_exited = False
    guard_has_looped = False
    while not guard_has_exited and not guard_has_looped:
        new_location, direction = do_guard_step(lab_map, (current_x, current_y), direction)
        if (new_location, direction) in walked_squares:
            guard_has_looped = True
        elif new_location is None:
            guard_has_exited = True
        else:
            walked_squares.add((new_location, direction))
            current_x, current_y = new_location
    return walked_squares, guard_has_looped


def display_path(lab_map, walked_squares):
    updated_map = copy.deepcopy(lab_map)
    for location, _ in walked_squares:
        x, y = location
        updated_map[x] = updated_map[x][:y] + 'X' + updated_map[x][y + 1:]
    return updated_map


def run():
    lab_map = parse_data(FILENAME)

    walked_squares, _ = do_guard_walk(lab_map)
    print(f"Walked squares : {len(walked_squares)}")

    looping_obstructions_found = 0
    for x in tqdm(range(len(lab_map)), desc="X"):
        for y in tqdm(range(len(lab_map[x])), desc="Y", leave=False):
            if lab_map[x][y] == LAB_SPACE:
                lab_map[x] = lab_map[x][:y] + OBSTRUCTION + lab_map[x][y + 1:]
                _, has_looped = do_guard_walk(lab_map)
                if has_looped:
                    looping_obstructions_found += 1
                lab_map[x] = lab_map[x][:y] + LAB_SPACE + lab_map[x][y + 1:]
    print(f"Looping obstructions found : {looping_obstructions_found}")


if __name__ == '__main__':
    run()
