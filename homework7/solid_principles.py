import gc
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
    def __init__(self, first_name, last_name, date_of_birth, subject):
        super().__init__(first_name, last_name, date_of_birth)
        self.subject = subject

    def represent(self):
        self.person_info.update({'course': self.subject})
        return self.person_info


class StudentManager:
    students_list = {}

    @classmethod
    def append_student(cls):
        for obj in gc.get_objects():
            if isinstance(obj, Student):
                for course in obj.course:
                    if course in cls.students_list.keys():
                        cls.students_list[course].append(f'{obj.first_name[0]} {obj.last_name[0]}')
                    else:
                        new_course = {course: [f'{obj.first_name[0]} {obj.last_name[0]}']}
                        cls.students_list.update(new_course)
        return cls.students_list

    def __repr__(self):
        return str(self.students_list)


class TeacherManager:
    teachers_list = {}

    @classmethod
    def append_student(cls):
        for obj in gc.get_objects():
            if isinstance(obj, Teacher):
                for course in obj.subject:
                    if course in cls.teachers_list.keys():
                        cls.teachers_list[course].append(f'{obj.first_name[0]} {obj.last_name[0]}')
                    else:
                        new_course = {course: [f'{obj.first_name[0]} {obj.last_name[0]}']}
                        cls.teachers_list.update(new_course)
        return cls.teachers_list


class Group:
    def __init__(self, course, teachers, students):
        self.course = f'{course}: \nTeacher: {teachers[course]}, \nStudents: {students[course]}'

    def __repr__(self):
        return self.course


if __name__ == '__main__':
    student1 = Student('Michael', 'Phillips', date(1999, 6, 14), ['Python', 'CSS'], 1)
    student2 = Student('Adam', 'Smith', date(2001, 7, 22), ['Python', 'Java', 'C#'], 5)
    student3 = Student('Mark', 'Jacobs', date(2000, 5, 7), ['Python', 'Java', 'C#'], 3)
    teacher1 = Teacher('Jennifer', 'Marks', date(1965, 4, 14), ['C#'])
    teacher2 = Teacher('Riley', 'James', date(1965, 4, 14), ['Python'])
    a = StudentManager().append_student()
    b = TeacherManager.append_student()
    pprint.pprint(a)
    print('\n')
    print(Group('Python', TeacherManager.teachers_list, StudentManager.students_list))

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
# INTERFACE SEGREGATION PRINCIPLE: Creating separate classes 'StudentManager' and 'TeacherManager' for creating groups
#                                  instead of creating one large Group class.
#
# DEPENDENCY INVERSION PRINCIPLE: 'person_info' argument of Person class doesn`t depend on whether a Person is a Student
#                                 or a Teacher. It could be a violation of this principle if, for example, I created an
#                                 if-else statement, which would pass different arguments according to whom a person is.
#                                 Classes 'StudentManager' and 'TeacherManager' also realized within this principle as
#                                 'Group' class doesn`t depend on changes inside those managers.
