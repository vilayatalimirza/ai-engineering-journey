def main():
    score =float(input("Please enter your score: "))
    grade = grade_classifier(score)
    print(f"Grade:{grade}")

def grade_classifier(score):
    if score < 0 or score > 100:
        raise ValueError("Please enter valid score!")
    elif score < 35:
        return "F"
    elif score<50:
        return "E"
    elif score<60:
        return "D"
    elif score<70:
        return "C"
    elif score<80:
        return "B"
    elif score<90:
        return "A"
    elif score<95:
        return "A+"
    elif score<=100:
        return "A++"
    
if __name__=="__main__":
    main()