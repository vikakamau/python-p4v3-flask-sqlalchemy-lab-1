# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.filter(Earthquake.id==id).first()
    if earthquake:
        body = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year,}
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    return make_response(body, status)
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude == magnitude).all()
    count = len(earthquakes)
    
    if count > 0:
        earthquake_list = [{
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year,
        } for earthquake in earthquakes]

        return jsonify({
            'count': count,
            'quakes': earthquake_list
        })
    else:
        body = {'count': 0, 'quakes': []}
        return make_response(jsonify(body), 200)


# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
