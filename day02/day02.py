from tqdm import tqdm

FILENAME = './input'
# FILENAME = './example'


def parse_data(filename):
    reports = []
    with open(filename) as data:
        for raw_line in data:
            report = [int(x) for x in raw_line.rstrip().split()]
            reports.append(report)

    return reports


# A safe report is either strictly increasing or strictly decreasing, and always only by 1, 2 or 3.
def is_safe_report(report):
    previous_number = report[0]
    could_be_ascending = True
    could_be_descending = True
    for i in range(1, len(report)):
        if report[i] < previous_number :
            could_be_ascending = False
        elif report[i] > previous_number :
            could_be_descending = False
        else : # Numbers are equal
            return False
        if not could_be_descending and not could_be_ascending:
            return False
        difference = abs(report[i] - previous_number)
        if difference not in [1, 2, 3]:
            return False
        previous_number = report[i]
    return True


def dampen_report(report, dampened_level):
    new_report = []
    for i in range(len(report)):
        if i != dampened_level:
            new_report.append(report[i])
    return new_report

def run():
    reports = parse_data(FILENAME)
    safe_reports = 0
    dampened_reports = 0
    for report in reports:
        if is_safe_report(report):
            safe_reports += 1
        else:
            for i in range(len(report)):
                if is_safe_report(dampen_report(report, i)):
                    dampened_reports += 1
                    break

    print(f"Safe reports : {safe_reports}")
    print(f"Safe and dampened reports : {safe_reports + dampened_reports}")





if __name__ == '__main__':
    run()
