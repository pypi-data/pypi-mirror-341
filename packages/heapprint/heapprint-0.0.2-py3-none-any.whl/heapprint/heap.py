import math

def heap(numbers: list[int] = []):

    height = math.ceil(math.log2(len(numbers) + 1))

    current_index = 0
    for level in range(height):

        elements_in_level = min(2 ** level, len(numbers) - current_index)

        spaces_before = " " * (2 ** (height - level - 1) * 3)
        print(spaces_before, end="")

        for i in range(elements_in_level):
            if current_index < len(numbers):
                print(f"{numbers[current_index]:2}", end="")
                current_index += 1
                if i < elements_in_level - 1:
                    print(" " * (2 ** (height - level) * 3 - 1), end="")
        print()
