
def main():
    numbers = get_numbers()
    minimum, maximum, average = calculate_stats(numbers)
    print(f"Min: {minimum}")
    print(f"Max: {maximum}")
    print(f"Average: {average:.2f}")


def get_numbers():
    numbers_input = input("Enter numbers separated by commas: ")
    if len(numbers_input)==0:
        raise ValueError("Please enter valid input")
    elif not numbers_input.isdigit():
        raise ValueError("Please enter comma separated numbers")
    numbers = [float(n.strip()) for n in numbers_input.split(",")]
    return numbers

def calculate_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    return minimum, maximum, average


if __name__ == "__main__":
    main()