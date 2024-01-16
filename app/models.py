from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk":"fk_%(table_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)



# Hero Table
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules = ('-heropowers.hero')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique= True)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('HeroPowers', back_populates = 'hero')

# Power Table
class Power(db.Model):
    __tablename__ = 'powers'
    serialize_rules = ('-heropowers.power')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('HeroPower', back_populates = 'power')

# HeroPowers Association Table
class HeroPowers(db.Model):
    __tablename__ = 'hero_powers'
    serialize_rules = ('-hero.powers', '-power.heroes')
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    hero = db.relationship('Hero', back_populates = 'powers')

    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    power = db.relationship('Power', back_populates ='heroes')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())