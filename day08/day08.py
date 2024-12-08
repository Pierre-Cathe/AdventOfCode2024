from tqdm import tqdm, trange
import operator

FILENAME = './input'
# FILENAME = './example'

EMPTY_LOCATION = '.'


def parse_data(filename):
    antenna_locations_by_frequency = {}
    antenna_map = []
    with open(filename) as lines:
        x = 0
        for raw_line in lines:
            line = raw_line.rstrip()
            antenna_map.append(line)
            y = 0
            for char in line:
                if char != EMPTY_LOCATION:
                    if char not in antenna_locations_by_frequency:
                        antenna_locations_by_frequency[char] = []
                    antenna_locations_by_frequency[char].append((x, y))
                y += 1
            x += 1
    return antenna_map, antenna_locations_by_frequency


def is_in_bounds(location, antenna_map):
    x, y = location
    return 0 <= x < len(antenna_map) and 0 <= y < len(antenna_map[x])


def generate_antenna_antinodes(location, direction, operation_to_perform, antenna_map):
    antinodes = []
    x, y = location
    x_dir, y_dir = direction
    i = 0
    while True:
        x = operation_to_perform(x, x_dir)
        y = operation_to_perform(y, y_dir)
        if is_in_bounds((x, y), antenna_map):
            antinodes.append((x, y))
        else:
            break
    return antinodes


def compute_antinodes(locations, antenna_map):
    antinodes = set()
    resonant_antinodes = set()
    for i in range(len(locations)):
        for j in range(i+1, len(locations)):
            resonant_antinodes.update((locations[i], locations[j]))
            x1, y1 = locations[i]
            x2, y2 = locations[j]
            x_diff = x2 - x1
            y_diff = y2 - y1

            antinodes_before = generate_antenna_antinodes((x1, y1), (x_diff, y_diff), operator.sub, antenna_map)
            antinodes_after = generate_antenna_antinodes((x2, y2), (x_diff, y_diff), operator.add, antenna_map)
            if len(antinodes_before) > 0:
                antinodes.add(antinodes_before[0])
            if len(antinodes_after) > 0:
                antinodes.add(antinodes_after[0])
            resonant_antinodes.update(antinodes_before)
            resonant_antinodes.update(antinodes_after)
    return antinodes, resonant_antinodes


def run():
    antenna_map, locations_by_frequency = parse_data(FILENAME)
    antinodes = set()
    resonant_antinodes = set()

    for frequency in tqdm(locations_by_frequency):
        frequency_antinodes, frequency_resonant_antinodes = compute_antinodes(locations_by_frequency[frequency], antenna_map)
        antinodes.update(frequency_antinodes)
        resonant_antinodes.update(frequency_resonant_antinodes)

    print(f"Number of antinodes : {len(antinodes)}")
    print(f"Number of resonant antinodes : {len(resonant_antinodes)}")


if __name__ == '__main__':
    run()
