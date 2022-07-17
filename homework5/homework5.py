import math
from http import HTTPStatus

from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import abort, use_kwargs

from database_handler import execute_query


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point):
        return math.sqrt(math.pow((self.x-point.x), 2) + math.pow((self.y-point.y), 2)) <= self.radius


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y




app = Flask(__name__)


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
@app.errorhandler(HTTPStatus.NOT_FOUND)
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


@app.route('/stats_by_city')
@use_kwargs(
    {
        'genre': fields.Str(
            required=False,
            load_default=None
        ),
    },
    location="query"
)
def stats_by_city(genre):
    # Tried to make ecranators,
    # so that R&B/Soul or Alternative & Punk were also displayed correctly
    # and there was no need to write escapers in the url,
    # but couldn't find how to change the url while sending a request
    # my_escapers = {
    #     ' ': '%20',
    #     '/': '%2F',
    #     '&': '%26'
    # }
    # for i in genre:
    #     if i in string.punctuation:
    #         escape_genre = re.sub(i, my_escapers[i], genre)
    # print(genre)
    # print(escape_genre)
    try:
        genre = genre.title()
        my_query = f"""SELECT COUNT(*) AS result, invoices.BillingCity, genres.Name \
                    FROM tracks \
                    JOIN genres on genres.GenreId = tracks.GenreId \
                    JOIN invoice_items on tracks.TrackId = invoice_items.TrackId \
                    JOIN invoices on invoices.InvoiceId = invoice_items.InvoiceId \
                    GROUP BY invoices.BillingCity, genres.Name \
                    HAVING genres.Name == '{genre}' \
                    ORDER BY result DESC \
                    LIMIT 1;"""
        send_query = execute_query(my_query)
        return f'<center>{genre} is most often listened in {send_query[0][1]} with the count of {send_query[0][0]} times!</center>'
    except (IndexError, AttributeError):
        abort(400, messages='Write down a valid genre please!')


if __name__ == '__main__':
    circle = Circle(10, 10, 6.8)
    point1 = Point(4, 7)
    point2 = Point(10, 10)
    point3 = Point(140, 72)
    print(circle.contains(point1))
    print(circle.contains(point2))
    print(circle.contains(point3))
    app.run(port=5001, debug=True)
