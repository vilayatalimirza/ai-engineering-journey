def main():
    text = input("Please enter the string to be checked: ").lower().split()
    frequency = count_words(text)
    print_frequency(frequency)

def count_words(text):
    frequency = {}
    for word in text:
        if word:
            word = word.strip(".,'!?\"")
            frequency[word] = frequency.get(word,0) + 1
    return frequency

def print_frequency(frequency):
    for word,count in frequency.items():
        print(f'Word \'{word}\' appears \'{count}\' number of times.')

if __name__ == "__main__":
    main()
