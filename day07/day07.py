from tqdm import tqdm, trange
import operator

FILENAME = './input'
# FILENAME = './example'


def parse_data(filename):
    data = []
    with open(filename) as lines:
        for raw_line in lines:
            line = raw_line.rstrip()
            result, values = line.split(':')
            operands = tuple([int(x) for x in values.split() if x != ''])
            data.append((int(result), operands))
    return data


def is_max_operator_vector(operators, possible_operators):
    for op in operators:
        if op != len(possible_operators) - 1:
            return False
    return True


def solve(equation, possible_operators):
    result, operands = equation
    operators = [0] * (len(operands) - 1)
    has_found_solution = False
    op_index = 0

    while not has_found_solution:
        current_result = evaluate_solution(operands, [possible_operators[x] for x in operators])
        if current_result == result:
            has_found_solution = True
        else:
            if is_max_operator_vector(operators, possible_operators):
                return False, operators
            for i in range(len(operators)-1, -1, -1):
                if operators[i] != len(possible_operators) - 1:
                    operators[i] += 1
                    break
                else:
                    operators[i] = 0
    return True, operators


def evaluate_solution(operands, operators):
    result = operands[0]
    for i in range(len(operators)):
        result = operators[i](result, operands[i+1])
    return result


def run():
    equations = parse_data(FILENAME)
    sum_of_solvable_equations_add_mul = 0
    sum_of_solvable_equations_add_mul_concat = 0
    for equation in tqdm(equations):
        is_solvable, solution = solve(equation, (operator.add, operator.mul))
        if is_solvable:
            equation_result, _ = equation
            sum_of_solvable_equations_add_mul += equation_result
        is_solvable, solution = solve(equation, (operator.add, operator.mul, lambda x, y : int(str(x)+str(y))))
        if is_solvable:
            equation_result, _ = equation
            sum_of_solvable_equations_add_mul_concat += equation_result

    print(f"Sum of solvable equations with add and mul : {sum_of_solvable_equations_add_mul}")
    print(f"Sum of solvable equations with add, mul and concat : {sum_of_solvable_equations_add_mul_concat}")


if __name__ == '__main__':
    run()
