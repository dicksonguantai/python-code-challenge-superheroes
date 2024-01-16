#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPowers 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'This is the home page'

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        heroes_dict = [
            {
                'id':hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            }
            for hero in heroes
        ]

        return jsonify(heroes_dict)
    
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
                            "id": hero_power.power.id,
                            "name": hero_power.power.name,
                            "description": hero_power.power.description
                        }
                
                    for hero_power in hero.powers
                ]
            }
            return jsonify(hero_data)
        else:
            response_dict = {"error": "Hero not found"}
            return jsonify(response_dict),404

api.add_resource(HeroesById, '/heroes/<int:id>')

class PowerResource(Resource):
    def get(self):
        powers = Power.query.all()
        power_dict = [
            {
                "id":power.id,
                "name":power.name,
                "description": power.description,
            }
            for power in powers
        ]
        return jsonify(power_dict)
   
api.add_resource(PowerResource, '/powers')

class PowerById(Resource):
     def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
            }
            return jsonify(power_data)
        else:
            response_dict = {
                "error": "Power not found"
            }
            response = jsonify(response_dict), 404
            return response

     def patch(self, id):
        power = Power.query.filter_by(id=id).first()
        if power:
            data = request.get_json()
            description = data.get('description')
            power.description = description
            db.session.commit()

            response = {
                "id":power.id,
                "name": power.name,
                "description": power.description,
            }
            return jsonify(response)
        else:
            response_dict = {
                "error": "Power not found"
            }
            response = jsonify(response_dict)
            return response

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
                    "id": powers.power.id,
                    "name": powers.power.name,
                    "description": powers.power.description

                }
                for powers in hero.powers
            ]
        }
        return jsonify(hero_data)

api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555)
