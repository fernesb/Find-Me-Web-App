import sys

from flask import Flask, jsonify, render_template, request
import wikipedia as wiki
import geocoder


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=str)
    b = request.args.get('b', 0, type=str)

    loc = geocoder.osm([a, b], method='reverse')

    if str(loc.town) != 'None':
        loc_name = loc.town + ' ' + loc.county + ' ' + loc.state
    elif str(loc.neighborhood) == 'None' and str(loc.suburb) == 'None':
        loc_name = loc.city + ' ' + loc.county + ' ' + loc.state
    elif str(loc.neighborhood) == 'None':
        if 'city_district' in loc.json['raw']['address']:
            loc_name = loc.suburb + ' ' + loc.json['raw']['address']['city_district']
        else:
            loc_name = loc.suburb, loc.city
    elif str(loc.suburb) == 'None':
        if 'city_district' in loc.json['raw']['address']:
            loc_name = loc.neighborhood + ' ' + loc.json['raw']['address']['city_district']
        else:
            loc_name = loc.neighborhood + ' ' + loc.city
    else:
        if 'city_district' in loc.json['raw']['address']:
            loc_name = loc.neighborhood + ' ' + loc.suburb, loc.json['raw']['address']['city_district']
        else:
            loc_name = loc.neighborhood + ' ' + loc.suburb + ' ' + loc.city

    summary = wiki.page(loc_name).summary

    return jsonify(result=loc_name + ': \n\n' + summary)


# @app.route('/receiver', methods=['POST'])
# def worker():
#     # read json + reply
#     data = request.get_json()
#     result = ''

#     for item in data:
#         # loop over every row
#         result += str(item['make']) + '\n'

#     return result


if __name__ == '__main__':
    app.run(debug=True)
