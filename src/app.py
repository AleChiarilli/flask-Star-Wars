"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import json
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, FavoritePlanets, Characters, FavoriteCharacters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


    # éstos son mis endpoints
    # 1. éste es el endpoint para recibir la info de todos los usuarios
@app.route('/user', methods=['GET'])
def handle_hello():

    results = User.query.all()
    users_list = list(map(lambda item: item.serialize(),results))


    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results": users_list
    }

    return jsonify(response_body), 200

         #2. éste es el endpoint para consultar UN dato o usuario en la tabla, éste método puede devolver varios elementos con el
         #   mismo ID, si no se usa la función first()
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    print(id)

    user = User.query.filter_by(id=id).first()
    data = user.serialize()
    

    return jsonify(data), 200


         #3. éste es el endpoint para crear un dato o usuario en la tabla
@app.route('/user', methods=['POST'])
def create_user():

    body = json.loads(request.data)

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    # esta linea busca el is active y lo pondra por defecto en True
    is_active = request.json.get("is_active", True)
    user = User(email=body["email"], password=body["password"], is_active=is_active)
    # session es una palabra reservada de SQL-Alchemy
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "The user has been created",
    }

    return jsonify(response_body), 200

    #4. éste es el endpoint para borrar un usuario en la tabla
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    print(id)

    # el filter_by te identifica el usuario
    user = User.query.filter_by(id=id).first()
    print(user.serialize())
    # session es una palabra reservada de SQL-Alchemy
    db.session.delete(user)
    db.session.commit()

    response_body = {
        "msg": "El usuario ha sido borrado",
    }
    return jsonify(response_body), 200


# estos son los endpoints para los planetas
# ############################################
@app.route('/planets', methods=['GET'])
def handle_planets():

    results = Planets.query.all()
    planets_list = list(map(lambda item: item.serialize(),results))

    return jsonify(planets_list), 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    print(id)
    # éste es el pedido de un solo planeta, pero con el método get
    planet = Planets.query.get(id)
    data = planet.serialize()

    return jsonify(data), 200

@app.route('/planets', methods=['POST'])
def create_planet():

    body = json.loads(request.data)
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'size' not in body:
        raise APIException('You need to specify the size', status_code=400)
    # esta linea busca el is active y lo pondra por defecto en True
    planet = Planets(name=body["name"], size=body["size"])
    # session es una palabra reservada de SQL-Alchemy
    db.session.add(planet)
    db.session.commit()

    response_body = {
        "msg": "El planeta ha sido creado",
    }

    return jsonify(response_body), 200


@app.route('/api/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    print(id)

    # el filter_by te identifica el usuario
    planet = Planets.query.filter_by(id=id).first()
    print(planet.serialize())
    # session es una palabra reservada de SQL-Alchemy
    db.session.delete(planet)
    db.session.commit()

    response_body = {
        "msg": "El planeta ha sido borrado",
    }
    return jsonify(response_body), 200

# AQUÍ VIENEN LOS ENDPOINTS PARA LOS CHARACTERS
# ############################################
@app.route('/characters', methods=['GET'])
def handle_characters():
    results = Characters.query.all()
    characters_list = list(map(lambda item: item.serialize(),results))
    return jsonify(characters_list), 200


@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    print(id)
    # éste es el pedido de un solo planeta, pero con el método get
    character = Characters.query.get(id)
    data = character.serialize()
    return jsonify(data), 200


@app.route('/characters', methods=['POST'])
def create_character():
    body = json.loads(request.data)
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body:
        raise APIException('You need to specify the name', status_code=400)
    if 'gender' not in body:
        raise APIException('You need to specify the gender', status_code=400)
    # esta linea busca el is active y lo pondra por defecto en True
    character = Characters(name=body["name"], gender=body["gender"])
    # session es una palabra reservada de SQL-Alchemy
    db.session.add(character)
    db.session.commit()
    response_body = {
        "msg": "the character has been created",
    }
    return jsonify(response_body), 200


@app.route('/api/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    print(id)
    # el filter_by te identifica el usuario
    character = Characters.query.filter_by(id=id).first()
    print(character.serialize())
    # session es una palabra reservada de SQL-Alchemy
    db.session.delete(character)
    db.session.commit()
    response_body = {
        "msg": "The character has been deleted",
    }
    return jsonify(response_body), 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
