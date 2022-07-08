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
    with open('students.csv', 'w') as my_csv:
        for i in range(count):
            my_csv.write(
                fake.name() + ',' + fake.profile('mail')['mail'] + ',' + fake.password(length=8) + ',' + str(
                    fake.date_of_birth(minimum_age=18, maximum_age=45)) + '\n')
    with open('students.csv', 'r') as my_json:
        result = csv.reader(my_json)
        final = {'students': []}
        for row in result:
            final['students'].append(({'Name': row[0], 'Email': row[1], 'Password': row[2], 'Birthday': row[3]}))
    app.config.update(JSON_SORT_KEYS=False)
    return final


@app.route("/bitcoin")
@use_kwargs(
    {
        'currency': fields.Str(
            load_default='USD',
        ),
        'count': fields.Int(
            load_default=1,
            validate=[validate.Range(min=1)]
        )
    },
    location="query"
)
def get_bitcoin_value(currency, count):
    currency = currency.upper()
    url = 'https://bitpay.com/api/rates'
    url_for_symbols = 'https://bitpay.com/currencies'

    result = requests.get(url, {})
    result = result.json()
    available_currencies = [x['code'] for x in result]
    if currency not in available_currencies:
        abort(400, messages='Not a valid currency!')

    result_for_symbols = requests.get(url_for_symbols, {})
    result_for_symbols = result_for_symbols.json()

    for row in result:
        if currency == row['code']:
            currency_rate = int(row['rate'])
    for row in result_for_symbols['data']:
        if currency == row['code']:
            currency_symbol = row['symbol']
    if count != 1:
        return f'<center><p>You can buy {round((count / currency_rate), 5)} bitcoins for {count} {currency_symbol}</p></center>'
    else:
        return f'<center><p>The price of one bitcoin is {currency_rate} {currency_symbol}</p></center>'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
