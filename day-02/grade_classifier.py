def main():
    score =float(input("Please enter your score: "))
    grade = grade_classifier(score)
    feedback = get_feedback(grade)
    print(f"Grade: {grade}")
    print(f"Your Feedback is: {feedback}")

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
    
def get_feedback(grade):
    feedback = {
        "A": "Excellent work!",
        "B": "Good job, keep it up!",
        "C": "Decent, but room to improve.",
        "D": "You need to put in more effort.",
        "F": "Needs serious improvement.",
        "Invalid score": "Please enter a score between 0 and 100."
    }
    return feedback.get(grade)


if __name__=="__main__":
    main()