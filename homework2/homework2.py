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
    while len(password) < password_length:
        result = [random.choice(upper), random.choice(lower), random.choice(digits), random.choice(punctuation)]
        random.shuffle(result)
        for i in result:
            if len(password) < password_length:
                password = password + i
            else:
                break
    return f'<center><p><h1>Your password:</h1>{password}<p></center>'


@app.route('/average')
def calculate_average():
    students_heights = []
    students_weights = []
    with open('homework2/hw.csv', 'r') as readfile:
        reader = csv.reader(readfile, delimiter=',')
        for row in reader:
            if row[0].isdigit():
                students_heights.append(float(row[1].replace(' ', '')))
                students_weights.append(float(row[2].replace(' ', '')))

        return f'<center><h1>The average height of all students:</h1><p>{sum(students_heights) / len(students_heights)}</p>'\
               f'<h1>The average weight of all students:</h1><p>{sum(students_weights) / len(students_weights)}</p></center>'


@app.route('/average_with_pandas')
def calculate_average_with_pandas():
    data = pd.read_csv('hw.csv')
    return f'<center><h1>The average height of all students:</h1><p>{data["Height(Inches)"].mean()}</p>' \
           f'<h1>The average weight of all students:</h1><p>{data["Weight(Pounds)"].mean()}</p></center>'


app.run(port=5000, debug=True)