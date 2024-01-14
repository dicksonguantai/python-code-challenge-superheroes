#!/usr/bin/env python3

from flask import Flask, make_response,jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource 
from models import db, Hero, Power, hero_power_association

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


@app.route('/')
def home():
    return 'This is the home page'

class Heroes(Resource):
    def get(self):
        heroes = []
        for hero in Hero.query.all():
            hero_data = {
                "id":hero.id,
                "name": hero.name,
                "super_name":hero.super_name,
                "created_at":hero.created_at
            }
            heroes.append(hero_data)
        return make_response(jsonify(heroes),200)

api.add_resource(Heroes, '/heroes')

class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero:
            hero_data = {
                "id":hero.id,
                "name":hero.name,
                "super_name":hero.super_name,
                "powers":[
                    {
                        "id": power.id,
                        "name":power.name,
                        "description":power.description
                         
                    }
                    for power in hero.powers
                ]
            }
            return make_response(jsonify(hero_data),200)
        else:
            response_dict = {"error":"Hero not found"}
            return make_response(jsonify(response_dict),404)
        
api.add_resource(HeroesById, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        powers = []
        for power in Power.query.all():
            power_data = {
                "id":power.id,
                "name":power.name,
                "description":power.description,
                "created_at":power.created_at,
                "hero_ps":[
                    {
                        "id":hero_p.id,
                        "strength":hero_p.strength,
                        "hero_id":hero_p.hero_id
                    }
                    for hero_p in power.hero_ps
                ]
            }
            powers.append(power_data)
        return make_response(jsonify(powers),200)
api.add_resource(Power, '/powers')

class PowerById(Resource):
    def get(self,id):
        power = Power.querry.get(id)
        if power:
            power_data = {
                "id":power.id,
                "name":power.name,
                "description":power.description,
                "created_at":power.created_at,
                "hero_ps":[
                    {
                        "id":hero_p.id,
                        "strength":hero_p.strength,
                        "hero_id":hero_p.hero_id
                    }
                    for hero_p in power.hero_ps
                ]

            }
            return make_response(jsonify([power_data]),200)
        else:
            response_dict = {"error":"Power not found"}
            return make_response(jsonify(response_dict),404)
    
    def patch(self,id):
        power = Power.query.get(id)
        if power:
            data = request.get_json()
            description = data.get('description')

            if not description or len(description)<20:
                response_dict ={"errors":["validation errors"]}
                return make_response(jsonify(response_dict),400)
            power.descrption = description
            db.session.commit()

            power_data = {
                "id":power.id,
                "name":power.name,
                "description":power.description,
                "created_at":power.created_at
            }
            return make_response(jsonify(power_data),200)
        else:
            response_dict = {"error":"Power not found"}
            return make_response(jsonify(response_dict),404)
api.add_resource(PowerById, '/powers/<int:id>')





if __name__ == '__main__':
    app.run(port=5555)
