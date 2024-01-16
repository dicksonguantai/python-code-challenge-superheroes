from models import Hero, Power, HeroPowers
from random import choice as rc
from app import app,db

powers = [
    {"name": "teleportation", "description": "allows the wielder to instantly travel from one location to another"},
    {"name": "mind control", "description": "gives the wielder the ability to control the thoughts and actions of others"},
    {"name": "invisibility", "description": "renders the wielder invisible to the naked eye"},
    {"name": "telekinesis", "description": "enables the wielder to move and manipulate objects with the mind"}
]

heroes = [
    {"name": "Bruce Banner", "super_name": "The Hulk"},
    {"name": "Tony Stark", "super_name": "Iron Man"},
    {"name": "Natasha Romanoff", "super_name": "Black Widow"},
    {"name": "Thor Odinson", "super_name": "Thor"},
    {"name": "Peter Parker", "super_name": "Spider-Man"},
    {"name": "Scott Lang", "super_name": "Ant-Man"},
    {"name": "T'Challa", "super_name": "Black Panther"},
    {"name": "Doctor Stephen Strange", "super_name": "Doctor Strange"},
    {"name": "Matt Murdock", "super_name": "Daredevil"},
    {"name": "Jessica Jones", "super_name": "Jessica Jones"}
]

strengths = ["Strong","Weak","Average"]
with app.app_context():
        HeroPowers.query.delete()
        Hero.query.delete()
        Power.query.delete()


        for power in powers:
            power_to = Power(name=power["name"],description = power["description"])
            db.session.add(power_to)

        db.session.commit()

        for hero in heroes:
            hero_to = Hero(name=hero["name"],super_name=hero["super_name"])
            db.session.add(hero_to)
        db.session.commit()

        heroesrc = Hero.query.all()
        powersrc = Power.query.all()

        for a_hero in heroesrc:
            for _ in range(rc([1,2,3])):
                power = rc(powersrc)
                strength = rc(strengths)
                heropowers = HeroPowers(hero_id=a_hero.id, power_id=power.id,strength=strength)
                db.session.add(heropowers)
        db.session.commit()



        
        
