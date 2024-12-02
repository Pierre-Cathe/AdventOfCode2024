from tqdm import tqdm
import bisect

FILENAME = './input'
# FILENAME = './example'


def parse_data(filename):
    with open(filename) as data:
        left_list, right_list = [], []
        for raw_line in data:
            line = raw_line.rstrip()
            numbers = raw_line.split()
            bisect.insort(left_list, int(numbers[0]))
            bisect.insort(right_list, int(numbers[1]))
    return left_list, right_list



def run():
    left_list, right_list = parse_data(FILENAME)
    total_distance = 0
    for i in range(len(left_list)):
        total_distance += abs(left_list[i] - right_list[i])

    print(f"Total distance : {total_distance}")
    previous_item = None
    previous_value = 0
    similarity_value = 0
    right_list_index = 0
    for i in range(len(left_list)):
        if previous_item == left_list[i]:
            similarity_value += previous_value
        else:
            previous_item = left_list[i]
            j = right_list_index
            number_of_matches = 0
            while left_list[i] >= right_list[j]:
                if left_list[i] == right_list[j]:
                    number_of_matches += 1
                j += 1
                right_list_index = j

                if j == len(right_list):
                    break
            previous_value = number_of_matches * left_list[i]
            similarity_value += previous_value
    print(f"Similarity value : {similarity_value}")





if __name__ == '__main__':
    run()
