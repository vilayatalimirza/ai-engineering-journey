def main():
    x=get_int()
    print(f'Number you entered is: {x}')
    word = input("Enter a word : ")
    print(f'Reverse of the word is: {word[-1::-1]}')
    print(f'Alternative letters in odd places of the word is: {word[::2]}')
    print(f'Alternative letters in even places of the word is: {word[1::2]}')
    
    
def get_int():
    while True:
        try:
            number = int(input("Please enter an number: "))
        except ValueError:
            print("Enter a valid number")
        else:
            return number    

main()
