from tqdm import tqdm, trange

FILENAME = './input'
# FILENAME = 'example2'

NEIGHBOR_DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


class HikingSpot:
    def __init__(self, x, y, elevation):
        self.x = x
        self.y = y
        self.location = (x, y)
        self.elevation = elevation
        self.reachable_nines = 0
        self.rating = 0


def parse_data(filename):
    data = []
    with open(filename) as lines:
        i = 0
        for raw_line in lines:
            data.append([])
            line = raw_line.rstrip()
            for j in range(len(line)):
                data[i].append(HikingSpot(i, j, int(line[j])))
            i += 1
    return data


def is_in_bounds(location, trail_map):
    x, y = location
    return 0 <= x < len(trail_map) and 0 <= y < len(trail_map[x])


def generate_neighbors(spot, trail_map):
    neighbors = []
    x, y = spot.location
    for direction in NEIGHBOR_DIRECTIONS:
        x_dir, y_dir = direction
        potential_neighbor_location = (x + x_dir, y + y_dir)
        if is_in_bounds(potential_neighbor_location, trail_map):
            neighbors.append(potential_neighbor_location)
    return neighbors


def update_trail_map(trail_map, starting_spot):
    current_elevation = starting_spot.elevation
    spots_to_evaluate = [starting_spot]
    seen_locations = set()
    while current_elevation > 0:
        next_level_spots = []
        for spot in spots_to_evaluate:
            for neighbor_location in generate_neighbors(spot, trail_map):
                x, y = neighbor_location
                neighbor = trail_map[x][y]
                if neighbor.elevation == current_elevation - 1 :
                    if neighbor_location not in seen_locations:
                        neighbor.reachable_nines += 1
                    neighbor.rating += 1
                    seen_locations.add(neighbor.location)
                    next_level_spots.append(neighbor)
        spots_to_evaluate = next_level_spots.copy()
        current_elevation -= 1


def run():
    trail_map = parse_data(FILENAME)
    for x in range(len(trail_map)):
        for y in range(len(trail_map[x])):
            if trail_map[x][y].elevation == 9:
                update_trail_map(trail_map, trail_map[x][y])
    score_sum = 0
    rating_sum = 0
    for x in range(len(trail_map)):
        for y in range(len(trail_map[x])):
            if trail_map[x][y].elevation == 0:
                score_sum += trail_map[x][y].reachable_nines
                rating_sum += trail_map[x][y].rating



    print(f"Score sum : {score_sum}")
    print(f"Rating sum : {rating_sum}")




if __name__ == '__main__':
    run()
