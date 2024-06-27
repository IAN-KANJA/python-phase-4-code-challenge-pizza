from flask import Flask,request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import Restaurant, Pizza, RestaurantPizza
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Miriams_Pizza_Restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)


#create your home classs what you want to be seen when one has entered your URL
class Home(Resource):
     def get(self):
        
        response_dict = {
            "message": "Welcome to Miriam's Pizza Resataurant",
        }
        
        response = make_response(
            response_dict,
            200
        )

        return response
api.add_resource(Home, '/')

#Define your ResataurantList class
class RestaurantList(Resource):

    def get(self):
        #create an empty list
        restaurants=[]
        #loop through the class TO GET all that is in the class
        for restaurant in Restaurant.query.all():
            restaurant_dict={
                "id":restaurant.id,
                "name":restaurant.name,
                "address":restaurant.address
            }
            #The restaurant list will append the restaurant_dict
            restaurants.append(restaurant_dict)
        response=make_response(jsonify(restaurants),200)
        return response
        

        #we addd the class to the resource plus its url
api.add_resource(RestaurantList, '/restaurants')


#create my RestaurantById class
class RestaurantById(Resource):
    def get(self, id):
        #Get each restaurant by its id
        restaurant = Restaurant.query.get(id)  
        if restaurant:
            restaurant_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            response = make_response(jsonify(restaurant_dict), 200)
        else:
            response = make_response(jsonify({"error": "Restaurant not found"}), 404)
        #The return should be outside not inside
        return response
      # define my delete function
    def delete(self, id):
        #Get the restaurant by id
        restaurant = Restaurant.query.get(id)  

        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            response = make_response(jsonify({"message": "Restaurant successfully deleted"}), 204)
        else:
            response = make_response(jsonify({"error": "Restaurant not found"}), 404)

        return response

# Add the class plus its URL to the resources
api.add_resource(RestaurantById, '/restaurants/<int:id>')


#Define my class PizzaList
class PizzaList(Resource):

    def get(self):
        pizzas=[]
        for pizza in Pizza.query.all():
            pizza_dict={
                "id":pizza.id,
                "name":pizza.name,
                "ingredient":pizza.ingredient
            }
            pizzas.append(pizza_dict)
        return make_response(jsonify(pizzas),200)
api.add_resource(PizzaList, '/pizza')
#add the pizza class and its url to the resource

class RestaurantPizza(Resource):
    
    def post(self):
        #get data in json format
        data = request.get_json()

        # This are the requred keys
        if not all(key in data for key in ("price", "pizza_id", "restaurant_id")):
            return make_response(jsonify({"errors": ["validation errors.include all keys"]}), 400)
        pizza_id = data["pizza_id"]
        restaurant_id = data["restaurant_id"]

        # Check if the Pizza and Restaurant exist based on their ids
        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)
        if not pizza or not restaurant:
            return make_response(jsonify({"errors": ["validation errors pizza and restaurant dont exist"]}), 400)

        #  Then you create a new RestaurantPizza
        restaurant_pizza = RestaurantPizza(
            price = data["price"],
            pizza_id = data["pizza_id"],
            restaurant_id = data["restaurant_id"]
        )
        db.session.add(restaurant_pizza)
        db.session.commit()

        # Return data thai is related  to the Pizza
        pizza_data = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }

        return make_response(jsonify(pizza_data), 201)
api.add_resource(RestaurantPizza,'/restaurant_pizza')

    
    
   

if __name__ == '__main__':
    app.run(port=5555, debug=True)