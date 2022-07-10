import csv

import requests

from faker import Faker
from flask import Flask, jsonify
from http import HTTPStatus
from webargs import fields, validate
from webargs.flaskparser import abort, use_kwargs

app = Flask(__name__)

fake = Faker()


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ["Invalid request."])

    if headers:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
            headers
        )
    else:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
        )


@app.route("/students")
@use_kwargs(
    {
        'count': fields.Int(
            load_default=10,
            validate=[validate.Range(min=1, max=1000)]
        ),
    },
    location="query"
)
def generate_students(count):
    fieldnames = ['Name', 'Email', 'Password', 'Birthday']
    students = [
        {
            'Name': fake.name(),
            'Email': fake.profile('mail')['mail'],
            'Password': fake.password(length=8),
            'Birthday': str(fake.date_of_birth(minimum_age=18, maximum_age=45))
        } for _ in range(count)
    ]
    with open('students.csv', 'w', newline='',) as my_csv:
        writer = csv.DictWriter(my_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(student for student in students)
    app.config.update(JSON_SORT_KEYS=False)
    return jsonify(students)


@app.route("/bitcoin")
@use_kwargs(
    {
        'currency': fields.Str(
            load_default='USD',
        ),
        'count': fields.Int(
            load_default=None,
            validate=[validate.Range(min=1, max=1000000)]
        )
    },
    location="query"
)
def get_bitcoin_value(currency, count):
    currency = currency.upper()
    url = requests.get(f'https://bitpay.com/api/rates/{currency}').json()
    url_for_symbols = requests.get('https://bitpay.com/currencies').json()

    available_currencies = [x['code'] for x in url_for_symbols['data']]
    if currency not in available_currencies:
        abort(400, messages='Not a valid currency!')

    if currency == url['code']:
        currency_rate = int(url['rate'])
    for row in url_for_symbols['data']:
        if currency == row['code']:
            currency_symbol = row['symbol']
    if count is None:
        return f'<center><p>The price of one bitcoin is {currency_rate} {currency_symbol}</p></center>'
    else:
        return f'<center><p>You can buy {round((count / currency_rate), 5)} bitcoins for {count} {currency_symbol}</p></center>'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
