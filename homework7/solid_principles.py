import pprint
from datetime import date


class Person:
    def __init__(self, first_name, last_name, date_of_birth):
        self.first_name = first_name,
        self.last_name = last_name,
        self.date_of_birth = date_of_birth
        self.person_info = dict({'first_name': self.first_name[0],
                                 'last_name': self.last_name[0],
                                 'age': self.calculate_age()})

    def calculate_age(self):
        today = date.today()
        current_age = today.year - self.date_of_birth.year - \
                      ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return current_age

    def represent(self):
        return self.person_info


class Student(Person):

    def __init__(self, first_name, last_name, date_of_birth, course, grade):
        super().__init__(first_name, last_name, date_of_birth)
        self.course = course
        self.grade = grade

    def represent(self):
        self.person_info.update({'course': self.course, 'grade': self.grade})
        return self.person_info


class Teacher(Person):
    def __init__(self, first_name, last_name, date_of_birth, course):
        super().__init__(first_name, last_name, date_of_birth)
        self.course = course

    def represent(self):
        self.person_info.update({'course': self.course})
        return self.person_info


class PersonManager:

    def __init__(self):
        self.persons_list = {}

    def append(self, persons):
        for person in persons:
            for course in person.course:
                if course in self.persons_list.keys():
                    self.persons_list[course].append(f'{person.first_name[0]} {person.last_name[0]}')
                else:
                    new_course = {course: [f'{person.first_name[0]} {person.last_name[0]}']}
                    self.persons_list.update(new_course)

        return self.persons_list

    def __repr__(self):
        return str(self.persons_list)


class Group:
    def __init__(self, course, teachers, students):
        self.course = f'{course}: \nTeacher: {teachers[course]}, \nStudents: {students[course]}'

    def __repr__(self):
        return self.course


if __name__ == '__main__':
    students = [
        Student('Michael', 'Phillips', date(1999, 6, 14), ['Python', 'CSS'], 1),
        Student('Adam', 'Smith', date(2001, 7, 22), ['Python', 'Java', 'C#'], 5),
        Student('Mark', 'Jacobs', date(2000, 5, 7), ['Python', 'Java', 'C#'], 3),
    ]

    teachers = [
        Teacher('Jennifer', 'Marks', date(1965, 4, 14), ['C#']),
        Teacher('Riley', 'James', date(1965, 4, 14), ['Python']),
    ]

    sm = PersonManager()
    tm = PersonManager()

    students1 = sm.append(students)
    teachers1 = tm.append(teachers)

    pprint.pprint(students1)
    print('\n')
    print(Group('Python', teachers1, students1))

# SINGLE-RESPONSIBILITY PRINCIPLE: Creating Person method 'calculate_age' instead of calculating it in __init__,
#                                  Creating separate classes 'StudentManager' and 'TeacherManager' for creating groups
#                                  according to programming language studied
#
# OPEN-CLOSED PRINCIPLE: 'represent' method is extended by each class, with no need to change anything in parent-class
#
# LISKOV SUBSTITUTION PRINCIPLE: Classes Student and Teacher inherits all arguments and methods of parent-class Person
#                                and, therefore, these arguments and methods could be written directly in child-classes
#                                without inheritance
#
# INTERFACE SEGREGATION PRINCIPLE: Creating separate 'PersonManager' class, which performs its own functions,
#                                                    so that it is not a 'Group'  method
#
# DEPENDENCY INVERSION PRINCIPLE: 'person_info' argument of Person class doesn`t depend on whether a Person is a Student
#                                 or a Teacher. It could be a violation of this principle if, for example, I created an
#                                 if-else statement, which would pass different arguments according to whom a person is.
#                                 Classes 'PersonManager' also realized within this principle as it doesn`t depend on
#                                 which Person is passed inside the manager.
