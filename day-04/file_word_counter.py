def main():
    filepath = input("Enter the file path: ")
    text = read_file(filepath)
    frequency = count_words(text)
    top_words = find_top(frequency)
    if top_words is None:
        print("Please enter correct filepath.")
        return
    print("Top Words: ")
    for word,count in top_words:
        print(f'{word}: {count}')


def read_file(filepath):
    try:
        with open(filepath,"r") as f:
            return f.read()
    except FileNotFoundError:
         return None


def count_words(text):
    if text is None:
        return None
    words = text.lower().split()
    frequency = {}
    for word in words:
        word = word.strip(".,'!?\"")
        if word:    
                frequency[word] = frequency.get(word,0) + 1
    
    return frequency


def find_top(frequency, n=5):
    if frequency is None:
        return None
    sorted_words = sorted(frequency.items(),key=lambda item: item[1], reverse=True)
    return sorted_words[:n]

if __name__ == "__main__":
    main()