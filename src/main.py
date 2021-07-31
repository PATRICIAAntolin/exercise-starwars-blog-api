"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

current_user_id = 0

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_users():
    users = User.query.all()
    users_all = []
    for user in users:
        users_all.append(users.serialize())
    return jsonify(users_all), 200

@app.route('/user/favorites', methods=['GET'])
def handle_user_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    favorites_all = []
    for favorite in favorites:
        favorites_all.append(favorite.serialize())
    return jsonify(favorites_all), 200

@app.route('/people', methods=['GET'])
def handle_people():
    characters = Character.query.all()
    characters_all = []
    for character in characters:
        characters_all.append(character.serialize())
    return jsonify(characters_all), 200

@app.route('/people/<int:id>', methods=['GET'])
def handle_people_by_id(id):
    character = Character.query.filter_by(id=id).first()
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planet.query.all()
    planets_all = []
    for planet in planets:
        planets_all.append(planet.serialize())
    return jsonify(planets_all), 200

@app.route('/planets/<int:id>', methods=['GET'])
def handle_planets_by_id(id):
    planet = Planet.query.filter_by(id=id).first()
    return jsonify(planet.serialize()), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_favorite_planet_add_remove(planet_id):
    if request.method == 'POST':
        favorite = Favorite(userid = current_user_id, planet_id = planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'result': 'OK'})
    else:
        favorite = Favorites.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'result': 'OK'})


@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def handle_favorite_people_add_remove(people_id):
    if request.method == 'POST':
        favorite = Favorite(userid = current_user_id, character_id = people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'result': 'OK'})
    else:
        favorite = Favorites.query.filter_by(user_id=current_user_id, character_id=people_id).first()
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'result': 'OK'})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
