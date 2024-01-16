#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPowers  # Update import statement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

# Include HeroPowers in the db.create_all() call
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'This is the home page'

class Heroes(Resource):
    def get(self):
        heroes = []
        for hero in Hero.query.all():
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "created_at": hero.created_at
            }
            heroes.append(hero_data)
        return make_response(jsonify(heroes), 200)

api.add_resource(Heroes, '/heroes')

class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero:
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {
                        "id": hero_power.id,
                        "strength": hero_power.strength,
                        "power": {
                            "id": power.id,
                            "name": power.name,
                            "description": power.description
                        }
                    }
                    for hero_power in hero.hero_powers
                ]
            }
            return make_response(jsonify(hero_data), 200)
        else:
            response_dict = {"error": "Hero not found"}
            return make_response(jsonify(response_dict), 404)

api.add_resource(HeroesById, '/heroes/<int:id>')

class PowerResource(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
                "created_at": power.created_at,
                "hero_ps": [
                    {
                        "strength": hero_power.strength,
                        "hero_id": hero_power.hero_id
                    }
                    for hero_power in power.hero_powers
                ]
            }
            return make_response(jsonify(power_data), 200)
        else:
            response_dict = {
                "error": "Power not found"
            }
            response = make_response(jsonify(response_dict), 404)
            return response

    def patch(self, id):
        power = Power.query.filter_by(id=id).first()

        if power:
            description = request.form.get('description')

            if not description or len(description) < 20:
                response_dict = {
                    "errors": ["validation errors"]
                }
                response = make_response(jsonify(response_dict), 400)
                return response

            for attr in request.form:
                setattr(power, attr, request.form.get(attr))
            db.session.add(power)
            db.session.commit()

            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
                "created_at": power.created_at
            }

            response = make_response(jsonify(power_data), 200)
            return response
        else:
            response_dict = {
                "error": "Power not found"
            }
            response = make_response(jsonify(response_dict), 404)
            return response

api.add_resource(PowerResource, '/powers')

class PowerById(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
                "created_at": power.created_at,
                "hero_ps": [
                    {
                        "id": hero_power.id,
                        "strength": hero_power.strength,
                        "hero_id": hero_power.hero_id
                    }
                    for hero_power in power.hero_powers
                ]
            }
            return make_response(jsonify([power_data]), 200)
        else:
            response_dict = {"error": "Power not found"}
            return make_response(jsonify(response_dict), 404)

    def patch(self, id):
        power = Power.query.get(id)
        if power:
            data = request.get_json()
            description = data.get('description')

            if not description or len(description) < 20:
                response_dict = {"errors": ["validation errors"]}
                return make_response(jsonify(response_dict), 400)
            power.description = description
            db.session.commit()

            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
                "created_at": power.created_at
            }
            return make_response(jsonify(power_data), 200)
        else:
            response_dict = {"error": "Power not found"}
            return make_response(jsonify(response_dict), 404)

api.add_resource(PowerById, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        if strength not in ["Strong", "Weak", "Average"]:
            response_dict = {"errors": ["validation errors"]}
            return make_response(jsonify(response_dict), 400)
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            response_dict = {"error": "Invalid hero_id or power_id"}
            return make_response(jsonify(response_dict), 404)
        hero_power_entry = HeroPowers(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id
        )
        db.session.add(hero_power_entry)
        db.session.commit()
        hero_data = {
            "id": hero_id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {
                    "id": power_id,
                    "name": power.name,
                    "description": power.description

                }
                for power in hero.powers
            ]
        }
        return make_response(jsonify(hero_data), 201)

api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555)
