from flask import Flask
import random
import string
import csv
import pandas as pd


app = Flask(__name__)


@app.route("/password")
def generate_password(min_limit=10, max_limit=25):
    password_length = random.randint(min_limit, max_limit)
    password = ''
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    punctuation = string.punctuation.replace('<', '')
    print(punctuation)
    char_choice = [upper, lower, digits, punctuation]
    while len(password) < password_length:
        password = password + (random.choice(char_choice[random.randint(0, 3)]))
    validation = {'upper': 0,
                  'lower': 0,
                  'digits': 0,
                  'punctuation': 0}
    for char in password:
        if upper.__contains__(char):
            validation['upper'] += 1
        if lower.__contains__(char):
            validation['lower'] += 1
        if digits.__contains__(char):
            validation['digits'] += 1
        if punctuation.__contains__(char):
            validation['punctuation'] += 1
    print(validation)
    if 0 not in validation.values():
        print(password)
        return f'<center><p><h1>Your password:</h1>{password}<p></center>'
    else:
        print(password)
        return generate_password(min_limit, max_limit)


@app.route('/average')
def calculate_average():
    students_heights = []
    students_weights = []
    with open('src/hw.csv', 'r') as readfile:
        reader = csv.reader(readfile, delimiter=',')
        for row in reader:
            if row[0].lower() == row[0].upper():
                students_heights.append(float(row[1].replace(' ', '')))
                students_weights.append(float(row[2].replace(' ', '')))

        return f'<center><h1>The average height of all students:</h1><p>{sum(students_heights) / len(students_heights)}</p>'\
               f'<h1>The average weight of all students:</h1><p>{sum(students_weights) / len(students_weights)}</p></center>'


@app.route('/average_with_pandas')
def calculate_average_with_pandas():
    data = pd.read_csv('src/hw.csv')
    return f'<center><h1>The average height of all students:</h1><p>{data["Height(Inches)"].mean()}</p>' \
           f'<h1>The average weight of all students:</h1><p>{data["Weight(Pounds)"].mean()}</p></center>'


app.run(port=5000, debug=True)