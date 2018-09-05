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

    location = geocoder.google([a, b], method='reverse')
    loc_name = location.city + ' ' + location.state
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
