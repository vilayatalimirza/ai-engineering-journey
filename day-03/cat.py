def main():
    n=get_number()
    meow1(n)
    meow2(n)
    meow3(n)
    meow4(n)
    meow5(n)

def get_number():
    while True:
        n=int(input("Number of Meows"))
        if n>0:
            break
    return n

def meow1(n):
    i=0
    while i<n:
        print("meow")
        i +=1
    print("---------------- ")

def meow2(n):
    for _ in range(n):
        print("meow")
    print("---------------- ")

def meow3(n):    
    for _ in range (-1,n-1):
        print("meow")
    print("---------------- ")

def meow4(n):
    for _ in range (0,n):
        print("meow")
    print("---------------- ")

def meow5(n):
    print("meow\n" * n,end="")

main()