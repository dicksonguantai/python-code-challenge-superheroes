from flask import Flask
from models import db, Hero, Power, HeroPowers
from datetime import datetime

# Create a Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the SQLAlchemy instance to the application
db.init_app(app)

def seed_data():
    with app.app_context():
        # Seed Heroes
        hero1 = Hero(name='Superman', super_name='Clark Kent', created_at=datetime.utcnow())
        hero2 = Hero(name='Batman', super_name='Bruce Wayne', created_at=datetime.utcnow())
        hero3 = Hero(name='Wonder Woman', super_name='Diana Prince', created_at=datetime.utcnow())

        db.session.add_all([hero1, hero2, hero3])
        db.session.commit()

        # Seed Powers
        power1 = Power(name='Flight', description='Ability to fly')
        power2 = Power(name='Super Strength', description='Incredible strength')
        power3 = Power(name='Invisibility', description='Ability to become invisible')

        db.session.add_all([power1, power2, power3])
        db.session.commit()

        # Seed HeroPowers
        hero_power1 = HeroPowers(strength='Strong', hero=hero1, power=power1)
        hero_power2 = HeroPowers(strength='Average', hero=hero1, power=power2)
        hero_power3 = HeroPowers(strength='Weak', hero=hero2, power=power3)

        db.session.add_all([hero_power1, hero_power2, hero_power3])
        db.session.commit()

if __name__ == '__main__':
    # Run the seed_data function to populate the database
    seed_data()
