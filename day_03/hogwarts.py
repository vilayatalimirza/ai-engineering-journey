"""
students = ["Harry","Hermionie","Ron","Draco"]

for student in students:
    print(student)

for i in range(len(students)):
    print(students[i])

"""
"""
students = {
    "Harry" : "Gryffindor",
    "Hermionie" : "Gryffindor",
    "Ron" : "Gryffindor",
    "Draco" : "Slytherin"
}

for student in students:
    print(student, students[student], sep=",")
"""

students = [
    {"Name":"Harry", "House":"Gryffindor", "Patronus": "Stag"},
    {"Name":"Hermionie", "House":"Gryffindor", "Patronus": "Otter"},
    {"Name":"Ron", "House":"Gryffindor", "Patronus": "Stag"},
    {"Name":"Draco", "House":"Slytherin", "Patronus": None}
]

for student in students:
    print(f'{student["Name"]}, {student["House"]}')
