from http import HTTPStatus

from flask import Flask, jsonify

import pandas as pd

from webargs import fields, validate
from webargs.flaskparser import abort, use_kwargs

from database_handler import execute_query

app = Flask(__name__)


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


@app.route('/price')
@use_kwargs(
    {
        'country': fields.Str(
            load_default=None,
            validate=[validate.Regexp("[a-zA-Z]")]
        ),
    },
    location="query"
)
def order_price(country):
    sales = execute_query("SELECT invoices.BillingCountry, SUM(invoice_items.UnitPrice * invoice_items.Quantity) "
                          "FROM invoices "
                          "JOIN invoice_items "
                          "ON invoice_items.InvoiceId = invoices.InvoiceId "
                          "GROUP BY invoices.BillingCountry")
    available_countries = [country[0] for country in sales]
    result = {}
    if country is None:
        for country in sales:
            result.update({country[0]: country[1]})
        result.update({'Total': execute_query("SELECT SUM(UnitPrice * Quantity) "
                                              "FROM invoice_items;")[0][0]})

    else:
        if country not in available_countries:
            abort(400, messages='There is no such country in invoices!')
        else:
            sales = execute_query(
                f"SELECT BillingCountry, SUM(Total) "
                f"FROM invoices "
                f"WHERE BillingCountry == '{country}';")
            result.update({sales[0][0]: sales[0][1]})

    df = pd.DataFrame(data=list(result.items()), columns=['Country', 'Sales']).to_html()
    return df


@app.route('/tracks')
@use_kwargs(
    {
        'track_id': fields.Int(
            required=False,
            load_default=None,
            validate=[validate.Range(min=1, max=3503)]
        ),
    },
    location="query"
)
def get_all_info_about_track(track_id):
    query = ('SELECT tracks.Name Track, '
             'artists.Name, '
             'genres.Name, '
             'tracks.Composer, '
             'albums.Title, '
             'round((tracks.Milliseconds / 60000.0), 2), '
             'round((tracks.Bytes * 0.000001), 2),'
             'media_types.Name,'
             'playlists.Name '
             'FROM tracks '
             'JOIN albums ON tracks.AlbumID=albums.AlbumID '
             'JOIN artists ON albums.ArtistID=artists.ArtistID '
             'JOIN genres on genres.GenreId = tracks.GenreId '
             'JOIN media_types on media_types.MediaTypeId = tracks.MediaTypeId '
             'JOIN playlist_track on tracks.TrackId = playlist_track.TrackId '
             'JOIN playlists on playlists.PlaylistId = playlist_track.PlaylistId ')
    if track_id:
        query += f'WHERE tracks.TrackId={str(track_id)}'
    else:
        query += 'GROUP BY tracks.TrackId'
    tracks_time = execute_query('SELECT SUM(Milliseconds) FROM tracks;')
    tracks_time_in_hours = f'<p>The total time of all tracks is {str(tracks_time[0][0] / 3600000)} hours!</p>'
    df = pd.DataFrame(data=list(execute_query(query)), columns=['Track',
                                                      'Artist',
                                                      'Genre',
                                                      'Composer',
                                                      'Album',
                                                      'Time (Seconds)',
                                                      'Weight (MB)',
                                                      'Media Type',
                                                      'Playlist']).to_html()
    return df + f'<center>{tracks_time_in_hours}</center>'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
