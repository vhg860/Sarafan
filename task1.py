def generator_numbers(input_string):
    result = []
    numbers = [int(x) for x in input_string.split()]
    for num in numbers:
        result.extend([num] * num)
    return ', '.join(map(str, result))


input_numbers = input("Введите числа через пробел: ")

print(generator_numbers(input_numbers))
