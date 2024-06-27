from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, unique=True, nullable=False)

    # add relationship
    pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    # add serialization rules
    serialize_rules = ('-pizzas.restaurant', '-restaurant.pizza')

    @validates('name')
    def validate_name(self, key, value):
        if len(value) > 30:
            raise ValueError("Name must be less than 50 characters long.")
        return value  



    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurants = db.relationship('RestaurantPizza', backref='pizza')

    # add serialization rules
    serialize_rules = ('-restaurant', 'pizza')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # add relationships

    ###### The relationships are already defined in the Restaurant and Pizza models

    # add serialization rules
    serialize_rules = ('-restaurant', 'pizza')

    # add validation
    @validates('price')
    def validate_price(self, key, value):
        if not 1 <= value <= 30:
            raise ValueError("Price should be between 1 and 30")
        return value

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
