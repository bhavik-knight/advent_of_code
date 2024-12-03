

def is_diff_in_range(numbers, dampener, memory = {}) -> bool:
    if memory.get(tuple(numbers)) is not None:
        return memory[tuple(numbers)]

    tolerance = 0
    i = 0
    for p,c,n in zip(numbers[:-2], numbers[1:-1], numbers[2:]):
        if p > c and c < n:
            if 1 <= abs(n - p) <= 3:
                tolerance += 1
        elif c > p and c > n:
            if 1 <= abs(n - p) <= 3:
                tolerance += 1
        elif not 1 <= abs(p - c) <= 3 or not 1 <= abs(c - n) <= 3:
            tolerance += 1

        print(f"Iteration({i + 1}) = ({p}, {c}, {n}): => {tolerance}")
        i += 1

        if dampener and tolerance > 1:
            return False

        if not dampener and tolerance > 0:
            return False

    memory[tuple(numbers)] = True
    return True


def is_diff(numbers, dampener, memory={}) -> dict:
    if len(numbers) < 3:
        if 1 <= abs(numbers[-1] - numbers[0]) <= 3:
            memory[tuple(numbers)] = 1

    tolerance = 0
    if len(numbers) == 3:
        p, c, n = numbers
        if not 1 <= abs(c - n) <= 3:
            tolerance += 1
        elif not 1 <= abs(p - n) <= 3:
            tolerance += 1
        elif not 1 <= abs (p - c) <= 3:
            tolerance += 1

        memory[tuple(numbers)] = tolerance
    return memory




numbers_list = [
[7, 6, 4, 2, 1],
[1, 2, 7, 8, 9],
[9, 7, 6, 2, 1],
[1, 3, 2, 4, 5],
[8, 6, 4, 4, 1],
[1, 3, 6, 7, 9],
[1, 2, 7, 3, 4],
[78, 81, 78, 80, 81, 83, 85, 83],
[8, 11, 9, 11, 14],
]

for l in numbers_list:
    print("-" * 50)
    result = is_diff_in_range(l, False)
    print(f"Report: {l} => {result}")

    print("=" * 30)

    result = is_diff(l, True)
    print(f"Report: {l} => {result}")
    print("-" * 50)
