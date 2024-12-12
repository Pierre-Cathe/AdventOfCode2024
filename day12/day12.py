from tqdm import tqdm, trange

# FILENAME = './input'
FILENAME = './example'

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def parse_data(filename):
    data = []
    with open(filename) as lines:
        for raw_line in lines:
            line = raw_line.rstrip()
            data.append(line)
    return data


def is_in_bounds(location, plot_map):
    x, y = location
    return 0 <= x < len(plot_map) and 0 <= y < len(plot_map[x])


def explore_plot(start_location, plot_map, seen_plots):
    perimeter, area = 0, 0
    plots_to_explore = [start_location]
    x_start, y_start = start_location
    plot_letter = plot_map[x_start][y_start]
    seen_plots[x_start][y_start] = True
    all_edges = []

    # Compute area and perimeter
    while len(plots_to_explore) > 0:
        x, y = plots_to_explore.pop()
        area += 1
        for edge_index in range(len(DIRECTIONS)):
            x_dir, y_dir = DIRECTIONS[edge_index]
            x_neighbor = x + x_dir
            y_neighbor = y + y_dir
            if is_in_bounds((x_neighbor, y_neighbor), plot_map) and plot_map[x_neighbor][y_neighbor] == plot_letter:
                if not seen_plots[x_neighbor][y_neighbor]:
                    seen_plots[x_neighbor][y_neighbor] = True
                    plots_to_explore.append((x_neighbor, y_neighbor))
            else:
                perimeter += 1
                all_edges.append(((x_neighbor, y_neighbor), edge_index))

    # Follow edges to compute sides
    sides = 0
    seen_edges = []
    while not len(all_edges) == 0:
        # start on a new loop, going clockwise
        location, edge = all_edges.pop()
        while (location, edge) not in seen_edges:
            seen_edges.append((location, edge))
            tracing_direction = (edge + 1) % len(DIRECTIONS)
            neighbor_dir = DIRECTIONS[tracing_direction]
            x_next, y_next = location[0] + neighbor_dir[0], location[1] + neighbor_dir[1]

            is_right_turn = False
            is_left_turn = False
            if is_in_bounds((x_next, y_next), plot_map):
                if plot_map[x_next][y_next] == plot_letter:
                    # check if left turn
                    x_left, y_left = x_next + DIRECTIONS[edge][0], y_next + DIRECTIONS[edge][1]
                    if is_in_bounds((x_left, y_left), plot_map) and plot_map[x_left][y_left] == plot_letter:
                        is_left_turn = True
                        edge = (edge - 1) % len(DIRECTIONS)
                        location = x_left, y_left
                        sides += 1
                else:
                    is_right_turn = True
            else:
                is_right_turn = True

            if is_right_turn:
                edge = (edge + 1) % len(DIRECTIONS)
                sides += 1
            elif not is_left_turn:
                # is neither a right or left turn
                location = x_next, y_next

    return perimeter, area, sides


def analyze_plots(plot_map):
    seen_plots = []
    for x in range(len(plot_map)):
        seen_plots.append([])
        for y in range(len(plot_map[x])):
            seen_plots[x].append(False)

    perimeters, areas, sides = [], [], []
    for x in range(len(plot_map)):
        for y in range(len(plot_map[x])):
            if not seen_plots[x][y]:
                perimeter, area, plot_sides = explore_plot((x, y), plot_map, seen_plots)
                perimeters.append(perimeter)
                areas.append(area)
                sides.append(plot_sides)
    return perimeters, areas, sides


def run():
    plots = parse_data(FILENAME)
    perimeters, areas, sides = analyze_plots(plots)

    cost = 0
    bulk_cost = 0
    for i in range(len(perimeters)):
        cost += perimeters[i] * areas[i]
        bulk_cost += sides[i] * areas[i]

    print(f"Total fencing cost : {cost}")
    print(f"Bulk fencing cost : {bulk_cost}")




if __name__ == '__main__':
    run()
