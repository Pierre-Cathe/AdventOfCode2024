from tqdm import tqdm
import re

FILENAME = './input'
# FILENAME = './example'


def parse_data(filename):
    rules, befores, afters, updates = {}, {}, {}, []
    with open(filename) as lines:
        for raw_line in lines:
            line = raw_line.rstrip()
            if line == '':
                continue
            if '|' in line:
                numbers = [int(number) for number in line.split('|')]
                for i in range(len(numbers)):
                    number = numbers[i]
                    if number not in rules:
                        rules[number] = []
                    rules[number].append((numbers[0], numbers[1]))
                    if i == 0:
                        if number not in afters:
                            afters[number] = []
                        afters[number].append(numbers[1])
                    else:
                        if number not in befores:
                            befores[number] = []
                        befores[number].append(numbers[0])
            else:
                update = [int(number) for number in line.split(',')]
                updates.append(update)
    return rules, befores, afters, updates


def is_printable(update, rules):
    for i in range(len(update)):
        number = update[i]
        relevant_rules = rules[number]
        for rule in relevant_rules:
            n_before, n_after = rule
            if number == n_after and n_before in update[i:]:
                return False
    return True


def reorder(update, rules, befores, afters):
    reordered_update = []
    numbers_to_add = update.copy()
    while len(numbers_to_add) != 0:
        i = 0
        while i < len(numbers_to_add):
            number = numbers_to_add[i]
            remaining_befores = []
            if number in befores:
                remaining_befores = [x for x in befores[number] if x in numbers_to_add]
            if len(remaining_befores) == 0:
                reordered_update.append(number)
                del(numbers_to_add[i])
                i -= 1
            i += 1
    return reordered_update




def run():
    rules, befores, afters, updates = parse_data(FILENAME)
    valid_updates_middle_pages = 0
    corrected_updates_middle_pages = 0
    for update in updates:
        if is_printable(update, rules):
            middle = update[len(update) // 2]
            valid_updates_middle_pages += middle
        else:
            corrected_update = reorder(update, rules, befores, afters)
            middle = corrected_update[len(corrected_update) // 2]
            corrected_updates_middle_pages += middle
    print(f"Printable updates middle pages sum : {valid_updates_middle_pages}")
    print(f"Corrected updates middle pages sum : {corrected_updates_middle_pages}")




if __name__ == '__main__':
    run()
