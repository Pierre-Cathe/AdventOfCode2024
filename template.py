from tqdm import tqdm, trange

# FILENAME = './input'
FILENAME = './example'


def parse_data(filename):
    data = []
    with open(filename) as lines:
        for raw_line in lines:
            line = raw_line.rstrip()
            data.append(line)
    return data



def run():
    data = parse_data(FILENAME)

    print(f"Solution : {}")




if __name__ == '__main__':
    run()
