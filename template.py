from tqdm import tqdm
import re

# FILENAME = './input'
FILENAME = './example'


def parse_data(filename):
    data = []
    with open(filename) as lines:
        for raw_line in lines:
            data.append(raw_line.rstrip())
    return data



def run():
    data = parse_data(FILENAME)

    print(f"Solution : {}")




if __name__ == '__main__':
    run()
