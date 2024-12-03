from tqdm import tqdm
import re

FILENAME = './input'
# FILENAME = './example'

MUL_REGEX = "mul\(([0-9]*),([0-9]*)\)"
DO_REGEX = "do\(\)"
DONT_REGEX = "don't\(\)"


def parse_data(filename):
    data = ""
    with open(filename) as lines:
        for raw_line in lines:
            data += (raw_line.rstrip())
    return data


def extract_mul_instructions(source_code):
    instructions = []
    matches = re.findall(MUL_REGEX, source_code)
    instructions.extend([(int(x[0]), int(x[1])) for x in matches])
    return instructions


def extract_mul_instructions_enabled_only(source_code):
    instructions = []
    matches = re.finditer(MUL_REGEX, source_code)
    dos = sorted(re.finditer(DO_REGEX, source_code), key= lambda match: match.start())
    donts = sorted(re.finditer(DONT_REGEX, source_code), key= lambda match: match.start())
    for match in matches:
        latest_prior_do = 0
        latest_prior_dont = None
        for dont in donts:
            if dont.start() < match.start():
                latest_prior_dont = dont.start()
            else:
                break
        for do in dos:
            if do.start() < match.start():
                latest_prior_do = do.start()
            else:
                break
        if latest_prior_dont is None or latest_prior_do > latest_prior_dont:
            # either there hasn't been a "don't" yet, or there's been a "do" since then
            instructions.append((int(match.group(1)), int(match.group(2))))
    return instructions


def run():
    source_code = parse_data(FILENAME)
    instructions = extract_mul_instructions(source_code)
    result_mul = 0
    for instruction in instructions:
        result_mul += instruction[0] * instruction[1]
    print(f"Result of multiplications : {result_mul}")

    enabled_instructions = extract_mul_instructions_enabled_only(source_code)
    result_mul = 0
    for instruction in enabled_instructions:
        result_mul += instruction[0] * instruction[1]
    print(f"Result of enabled multiplications : {result_mul}")





if __name__ == '__main__':
    run()
