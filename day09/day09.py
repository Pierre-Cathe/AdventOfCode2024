from tqdm import tqdm, trange

FILENAME = './input'
# FILENAME = './example'


def parse_data(filename):
    data = ''
    with open(filename) as lines:
        for raw_line in lines:
            data = raw_line.rstrip()
    return data


def expand_memory(memory):
    expanded = []
    file_id = 0
    for i in range(len(memory)):
        block_count = int(memory[i])
        if i % 2 == 0:
            for j in range(block_count):
                expanded.append(file_id)
            file_id += 1
        else:
            for j in range(block_count):
                expanded.append(None)
    return expanded


def compact_without_fragmentation(memory, memory_repr):
    new_memory = memory.copy()
    block_index = len(new_memory) - 1
    file_index = len(memory_repr) - 1
    with tqdm(total=len(memory_repr)/2, desc="Files processed") as pbar:
        while file_index > 0:
            file_length = int(memory_repr[file_index])
            available_space_start = 0
            is_long_enough = False
            while not is_long_enough and available_space_start < block_index - file_length:
                available_space_start += 1
                if available_space_start < block_index - file_length and new_memory[available_space_start] is None:
                    reached_the_end = True
                    for i in range(file_length):
                        if new_memory[available_space_start + i] is not None:
                            reached_the_end = False
                            break
                    if reached_the_end:
                        is_long_enough = True
            if is_long_enough:
                for i in range(file_length):
                    new_memory[available_space_start + i] = new_memory[block_index - i]
                    new_memory[block_index - i] = None
            previous_blank_length = int(memory_repr[file_index - 1])
            block_index -= file_length
            block_index -= previous_blank_length
            file_index -= 2
            pbar.update(1)
    return new_memory


def compact_with_fragmentation(memory):
    new_memory = memory.copy()
    empty_space_index = 1
    for file_index in range(len(new_memory) - 1, -1, -1):
        if new_memory[file_index] is not None:
            while new_memory[empty_space_index] is not None and empty_space_index < file_index:
                empty_space_index += 1
            if new_memory[empty_space_index] is None:
                new_memory[empty_space_index] = new_memory[file_index]
                new_memory[file_index] = None
    return new_memory


def compute_checksum(memory):
    checksum = 0
    for i in range(len(memory)):
        if memory[i] is not None:
            checksum += i * memory[i]
    return checksum


def run():
    memory_repr = parse_data(FILENAME)
    memory = expand_memory(memory_repr)
    compacted_memory = compact_with_fragmentation(memory)
    checksum = compute_checksum(compacted_memory)
    print(f"Checksum fragmented : {checksum}")

    unfragmented_memory = compact_without_fragmentation(memory, memory_repr)
    checksum = compute_checksum(unfragmented_memory)
    print(f"Checksum non-fragmented : {checksum}")



if __name__ == '__main__':
    run()
