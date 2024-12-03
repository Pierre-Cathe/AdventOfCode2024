from tqdm import tqdm
import re

FILENAME = './input'
# FILENAME = './example'

MUL_REGEX = "mul\(([0-9]*),([0-9]*)\)"


def parse_data(filename):
    lines = []
    with open(filename) as data:
        for raw_line in data:
            lines.append(raw_line.rstrip())
    return lines


def extract_mul_instructions(source_code):
    instructions = []
    for line in source_code:
        matches = re.findall(MUL_REGEX, line)
        instructions.extend([(int(x[0]), int(x[1])) for x in matches])
    return instructions


def run():
    source_code = parse_data(FILENAME)
    instructions = extract_mul_instructions(source_code)
    result_mul = 0
    for instruction in instructions:
        result_mul += instruction[0] * instruction[1]
    print(f"Result of multiplications : {result_mul}")





if __name__ == '__main__':
    run()
