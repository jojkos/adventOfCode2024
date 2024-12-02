def is_safe(report):
    isIncreasing = None
    for j in range(len(report) - 1):
        diff = report[j + 1] - report[j]
        if abs(diff) < 1 or abs(diff) > 3 or diff == 0:
            return False
        if isIncreasing is None:
            isIncreasing = diff > 0
        elif (isIncreasing and diff <= 0) or (not isIncreasing and diff >= 0):
            return False
    return True

with open("input.txt", "r") as file:
    data = [list(map(int, line.strip().split())) for line in file]

safeCount = 0

for report in data:
    if is_safe(report):
        safeCount += 1
    else:
        for i in range(len(report)):
            new_report = report[:i] + report[i+1:]
            if len(new_report) < 2:
                continue
            if is_safe(new_report):
                safeCount += 1
                break

print(safeCount)
