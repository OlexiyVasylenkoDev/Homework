import math

from flask import Flask, jsonify

from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import abort, use_kwargs


from database_handler import execute_query


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point):
        self.point = point
        return math.sqrt(math.pow((self.x-self.point.x), 2) + math.pow((self.y-self.point.y), 2)) <= self.radius


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


circle = Circle(10, 10, 6.8)
point1 = Point(4, 7)
point2 = Point(10, 10)
point3 = Point(140, 72)
print(circle.contains(point1))
print(circle.contains(point2))
print(circle.contains(point3))

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
    try:
        genre = genre.capitalize()
        query = execute_query(f"""SELECT COUNT(*) AS result, invoices.BillingCity, genres.Name \
            FROM tracks \
            JOIN genres on genres.GenreId = tracks.GenreId \
            JOIN invoice_items on tracks.TrackId = invoice_items.TrackId \
            JOIN invoices on invoices.InvoiceId = invoice_items.InvoiceId \
            GROUP BY invoices.BillingCity, genres.Name \
            HAVING genres.Name == '{genre}' \
            ORDER BY result DESC \
            LIMIT 1;""")
        return f'<center>{genre} is most often listened in {query[0][1]} with the count of {query[0][0]} times!</center>'
    except (IndexError, AttributeError) as e:
        abort(400, messages='Write down a valid genre please!')


if __name__ == '__main__':
    app.run(port=5001, debug=True)
