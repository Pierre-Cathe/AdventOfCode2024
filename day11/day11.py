from tqdm import tqdm, trange

FILENAME = './input'
# FILENAME = './example2'

NUMBER_OF_BLINKS_FIRST_STAR = 25
NUMBER_OF_BLINKS_SECOND_STAR = 75


def parse_data(filename):
    data = []
    with open(filename) as lines:
        for raw_line in lines:
            line = raw_line.rstrip()
            for number in line.split():
                data.append(int(number))
    return data


def do_blinks_depth_first(stone, blink, blink_limit, seen_stones):
    if (stone, blink) in seen_stones:
        return seen_stones[(stone, blink)]
    if blink == blink_limit:
        str_repr = str(stone)
        if len(str_repr) % 2 == 0:
            return 2
        else:
            return 1
    else:
        if stone == 0:
            value = do_blinks_depth_first(1, blink+1, blink_limit, seen_stones)
            seen_stones[(stone, blink)] = value
            return value
        else:
            str_repr = str(stone)
            if len(str_repr) % 2 == 0:
                midpoint = int(len(str_repr) / 2)
                stone1 = int(str_repr[:midpoint])
                stone2 = int(str_repr[midpoint:])
                return do_blinks_depth_first(stone1, blink+1, blink_limit, seen_stones) + do_blinks_depth_first(stone2, blink+1, blink_limit, seen_stones)
            else:
                value = do_blinks_depth_first(stone*2024, blink+1, blink_limit, seen_stones)
                seen_stones[(stone, blink)] = value
                return value


def do_blink_breadth_first(stones):
    i = 0
    with tqdm(total=len(stones), leave=False) as pbar:
        while i < len(stones):
            if stones[i] == 0:
                stones[i] = 1
            else:
                str_repr = str(stones[i])
                if len(str_repr) % 2 == 0:
                    midpoint = int(len(str_repr)/2)
                    stones[i] = int(str_repr[:midpoint])
                    stones.insert(i + 1, int(str_repr[midpoint:]))
                    i += 1
                else:
                    stones[i] *= 2024
            i += 1
            pbar.update(1)


def run():
    original_stones = parse_data(FILENAME)
    stones = original_stones.copy()
    for _ in trange(NUMBER_OF_BLINKS_FIRST_STAR):
        do_blink_breadth_first(stones)

    print(f"Stones after {NUMBER_OF_BLINKS_FIRST_STAR} : {len(stones)}")

    result = 0
    for stone in tqdm(original_stones):
        result += do_blinks_depth_first(stone, 1, NUMBER_OF_BLINKS_SECOND_STAR, {})
    print(f"Stones after {NUMBER_OF_BLINKS_SECOND_STAR} : {result}")


if __name__ == '__main__':
    run()
