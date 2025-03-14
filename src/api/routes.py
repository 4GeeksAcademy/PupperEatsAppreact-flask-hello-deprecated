"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Food, Pet, Accessories
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select, and_, or_
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt 

api = Blueprint('api', __name__)
bcrypt = Bcrypt()


# Allow CORS requests to this API
CORS(api)


# @api.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }

#     return jsonify(response_body), 200


@api.route('/')
def sitemap():
    return generate_sitemap(api)

# Obtener todos los alimentos
@api.route('/foods', methods=['GET'])
def get_foods():
    foods = Food.query.all()
    if not foods:
        return "food not found", 404
    else:
        return jsonify([food.serialize() for food in foods]), 200


# Obtener un alimento por ID
@api.route('/foods/<int:food_id>', methods=['GET'])
def get_food(food_id):
    food = Food.query.get(food_id)
    if not food:
        return jsonify({"error": "Food not found"}), 404
    return jsonify(food.serialize()), 200

#obtener todos los usuarios
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if not users:
        return "not users found", 404
    return jsonify([user.serialize() for user in users]), 200


# Obtener un usuario por ID
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user.serialize()), 200


@api.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    if not pets:
        return "no pets found", 404
    return jsonify([pet.serialize() for pet in pets]), 200


# Obtener una mascota por ID
@api.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"error": "pet not found"}), 404
    return jsonify(pet.serialize()), 200



#obtener sugerencias de comida según mascota
@api.route('/foods/suggestions/<int:pet_id>', methods=['GET'])
@jwt_required()
def get_pet_suggestions(pet_id):
    pet = Pet.query.get(pet_id).serialize()
    # Problema: Un animal puede tener varias patologias en su campo, habría que coger este campo y tratarlo,
    # separar las patologias en una lista y hacer la query para cada patologia.
    # Solucion simple: limitar a 1 patologia cada animal por ahora
    #if para pet# anymal_type == perro, animal size    #si no no hace falta size
    if pet["animal_type"] == "perro":
        food_suggestions = db.session.execute(select(Food).where(and_(Food.animal_type==pet["animal_type"]),
                                                             Food.size==pet["size"],
                                                             Food.age==pet["age"],
                                                             Food.pathologies==pet["pathologies"])).all()
    else:
        food_suggestions = db.session.execute(select(Food).where(Food.animal_type==pet["animal_type"]),
                                                             Food.age==pet["age"],
                                                             Food.pathologies==pet["pathologies"]).all()
    if not food_suggestions :
        return "no suggestions found", 404
    return [food[0].serialize() for food in food_suggestions], 200


# #obtener sugerencias de comida según mascota
# @api.route('/foods/suggestions/<int:pet_id>', methods=['GET'])
# def get_pet_suggestions(pet_id):
#     pet = Pet.query.get(pet_id)
#     if not pet:
#         return jsonify({"error": "pet not found"}), 404
    
#     pet_data = pet.serialize()
#     filters = [Food.animal_type == pet_data["animal_type"], Food.age == pet_data["age"]]
    
#     if pet_data["animal_type"] == "perro":
#         filters.append(Food.size == pet_data["size"])
    
#     # Si la mascota tiene patologías, agregarlas al filtro
#     if pet_data["pathologies"]:
#         pathologies_list = pet_data["pathologies"].split(",")  
#         filters.append(Food.pathologies.in_(pathologies_list))
#     else: 
#         filters.append(or_(Food.pathologies != None, Food.pathologies == None))
#     food_suggestions = db.session.execute(select(Food).where(and_(*filters))).all()
    
#     if not food_suggestions:
#         return jsonify({"error": "no suggestions found"}), 404
    
#     return jsonify([food[0].serialize() for food in food_suggestions]), 200


#obtener todos los alimentos según tipo de animal
@api.route('/foods/cat', methods=['GET'])
def get_all_cat_food():
    food_cat = db.session.query(Food).filter(Food.animal_type.ilike("%gato%")).all()

    print("Datos obtenidos:", food_cat)

    if not food_cat:
        return jsonify({"error": "No cat food found"}), 404

    print("Datos obtenidos:", food_cat)
    if not food_cat:
        return jsonify({"error": "No cat food found"}), 404

    return jsonify([food.serialize() for food in food_cat]), 200



@api.route('/foods/dog', methods=['GET'])
def get_all_dog_food():
    food_dog = db.session.query(Food).filter(Food.animal_type.ilike("%perro%")).all()


    print("Datos obtenidos:", food_dog)

    if not food_dog:
        return jsonify({"error": "No dog food found"}), 404


    print("Datos obtenidos:", food_dog)
    if not food_dog:
        return jsonify({"error": "No dog food found"}), 404

    return jsonify([food.serialize() for food in food_dog]), 200

@api.route('/foods/exotic', methods=['GET'])
def get_all_exotic_food():
    food_exotic = db.session.query(Food).filter(Food.animal_type.ilike("%exótico%")).all()


    print("Datos obtenidos:", food_exotic)

    if not food_exotic:
        return jsonify({"error": "No exotic food found"}), 404


    print("Datos obtenidos:", food_exotic)
    if not food_exotic:
        return jsonify({"error": "No exotic food found"}), 404

    return jsonify([food.serialize() for food in food_exotic]), 200

# Obtener todos los accesorios
@api.route('/accessories', methods=['GET'])
def get_accessories():
    accessories = Accessories.query.all()
    if not accessories:
        return "no accessories found", 404
    return jsonify([accessory.serialize() for accessory in accessories]), 200


# Obtener una accesorio por ID
@api.route('/accessories/<int:accessories_id>', methods=['GET'])
def get_accessory(accessories_id):
    accessories = Accessories.query.get(accessories_id)
    if not accessories:
        return jsonify({"error": "accessories not found"}), 404
    return jsonify(accessories.serialize())

# Crear un nuevo alimento
@api.route('/foods', methods=['POST'])
def create_food():
    data = request.get_json()
    new_food = Food(
        name=data["name"],
        brand=data["brand"],
        description=data.get("description"),
        ingredients=data["ingredients"],
        animal_type=data["animal_type"],
        pathologies=data["pathologies"],  # Recibe lista JSON
        size=data["size"],
        weight=data["weight"],
        price=data["price"],
        url=data.get("url")
    )
    db.session.add(new_food)
    db.session.commit()
    return jsonify(new_food.serialize()), 201


#registrar nuevo usuario(signup)

@api.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8') 

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password
)
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "El usuario ya existe"}), 400

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

# iniciar sesion(login)
# @api.route('/login', methods=['POST'])
# def logging_user():
#     data = request.get_json()
#     user = User.query.filter_by(email=data["email"]).first()


#     if User.query.filter_by(email=data["email"]).first() and User.query.filter_by(password=data["password"]).first():
#         access_token=create_access_token(identity=user.email)
#         return jsonify(access_token=access_token), 200
    
#     return jsonify ({"nsg":"credenciales invalidas"}), 400

@api.route('/login', methods=['POST'])
def login_user():

    body = request.get_json()

    if not body or "email" not in body or "password" not in body:
        return jsonify({"msg": "credenciales no validas"}), 400 

    email = body["email"]
    password = body["password"]
    user = User.query.filter_by(email=email).first()
    print(user)
    #if bcrypt.check_password_hash(user.password, body["password"]):
    if user != None and bcrypt.check_password_hash(user.password, body["password"]):
        token=create_access_token(identity=user.email)
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
        
        return jsonify({"msg": "inicio de sesion exitoso", "token": token, "user": user_data}), 200
    return jsonify({"msg": "credenciales no validas"}), 400 

#Vista privada del usuario CON el token
@api.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():

    current_user_email = get_jwt_identity()

    user = User().query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"msg": "usuario no encontrado"}), 400

    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name
    }

    return jsonify(user_data), 200


#Vista privada del usuario a sus mascotas
@api.route('/user_pets', methods=['GET'])
@jwt_required()
def get_user_pets_info():

    current_user_email = get_jwt_identity()

    user = User().query.filter_by(email=current_user_email).first()

    pets = Pet().query.filter_by(user_id=user.id).all()
    
    if not pets:
        return jsonify({"msg": "mascota no econtrada"}), 400

    return jsonify([pet.serialize() for pet in pets]), 200



#crear un nuevo accesorio
@api.route('/accessories', methods=['POST'])
def create_accessory():
    data = request.get_json()
    
    new_accessory = Accessories(
        name=data["name"],
        brand=data["brand"],
        description=data["description"],
        animal_type=data["animal_type"],
        pathologies=data["pathologies"],
        price=data["price"],
        url=data["url"]
)
    db.session.add(new_accessory)
    db.session.commit()
    return jsonify(new_accessory.serialize()), 201

#crear una nueva mascota
@api.route('/pets', methods=['POST'])
@jwt_required()
def create_pet():
    data = request.get_json()
    current_user_email = get_jwt_identity()
    user = User().query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"msg": "usuario no encontrado"}), 400

    new_pet = Pet(
        name=data["name"],
        size= None,
        breed= None,
        age=data["age"],
        animal_type=data["animal_type"],
        pathologies= None,
        url=data.get("url"),  # Asegúrate de que se está obteniendo correctamente
        user_id=user.id
        )
    db.session.add(new_pet)
    db.session.commit()
    return jsonify(new_pet.serialize()), 201

@api.route('/foods/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    food = Food.query.get(food_id)
    if not food:
        return jsonify({"message": "Food not found"}), 404

    data = request.get_json()

    food.name = data.get("name", food.name)
    food.brand = data.get("brand", food.brand)
    food.description = data.get("description", food.description)
    food.ingredients = data.get("ingredients", food.ingredients)
    food.weight = data.get("weight", food.weight)
    food.price = data.get("price", food.price)
    food.animal_type = data.get("animal_type", food.animal_type)
    food.size = data.get("size", food.size)
    food.pathologies = data.get("pathologies", food.pathologies)
    food.url = data.get("url", food.url)

    db.session.commit()

    return jsonify({
        "id": food.id,
        "name": food.name,
        "brand": food.brand,
        "description": food.description,
        "ingredients": food.ingredients,
        "animal_type": food.animal_type,
        "price": food.price,
        "weight": food.weight,
        "size" : food.size,
        "pathologies": food.pathologies,
        "url": food.url
    })



@api.route('/users', methods=['PUT'])
@jwt_required()
def update_user():
    current_user_email = get_jwt_identity()
    user = User().query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"message": "user not found"}), 404

    data = request.get_json()

    user.name = data.get("name", user.name)
    user.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    # user.password = data.get("password" , user.password)

    db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "password":user.password
    })


@api.route('/pets/<int:pet_id>', methods=['PUT'])
@jwt_required()
def new_pet(pet_id):
    data = request.get_json()
    current_user_email = get_jwt_identity()
    user = User().query.filter_by(email=current_user_email).first()

    if not user:

        return jsonify({"msg": "usuario no encontrado"}), 400
    
    data = request.get_json()
    
    pet=Pet().query.filter_by(id=pet_id).first()

    pet.name = data.get("name", pet.name)
    pet.size = data.get("size", pet.size)
    pet.age = data.get("age", pet.age)
    pet.animal_type = data.get("animal_type", pet.animal_type)
    pet.pathologies = data.get("pathologies", pet.pathologies)
    pet.url = data.get("url", pet.url)

    db.session.commit()
    return jsonify(new_pet.serialize()), 201


@api.route('/accessories/<int:accessories_id>', methods=['PUT'])
def update_accessory(accessories_id):
    accessories = Accessories.query.get(accessories_id)
    if not accessories:
        return jsonify({"message": "Accessory not found"}), 404

    data = request.get_json()

    accessories.name = data.get("name", accessories.name)
    accessories.brand = data.get("brand", accessories.brand)
    accessories.description = data.get("description", accessories.description)
    accessories.price = data.get("price", accessories.price)
    accessories.animal_type = data.get("animal_type", accessories.animal_type)
    accessories.pathologies = data.get("pathologies", accessories.pathologies)
    accessories.url = data.get("url", accessories.url)

    db.session.commit()

    return jsonify({
        "id": accessories.id,
        "name": accessories.name,
        "brand": accessories.brand,
        "description": accessories.description,
        "animal_type": accessories.animal_type,
        "price": accessories.price,
        "pathologies": accessories.pathologies,
        "url": accessories.url
    })



@api.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    # Buscar el usuario por su ID
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email = current_user_email).first()

    # Eliminar el usuario de la base de datos
    db.session.delete(user)
    db.session.commit()

    # Devolver una respuesta JSON indicando que el usuario fue eliminado
    return jsonify({
        'message': f'User {user.name} with id {user.id} has been deleted successfully.'
    }), 200


@api.route('/pet/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    
    pet = Pet.query.get(pet_id).first()

    # Eliminar la mascota de la base de datos
    db.session.delete(pet)
    db.session.commit()

    # Devolver una respuesta JSON indicando que la mascota fue eliminada
    return jsonify({
        'message': f'Pet {pet.name} with id {pet.id} has been deleted successfully.'
    }), 200


@api.route('/search', methods=['GET'])
def search_product():
    data = request.get_json()
    # cada query (Food y Accessories) mira en cada uno de los campos de interes la busqueda introducida en el formulario 
    foods = Food.query.filter(or_(Food.name.like(f'%{data["search"]}%'),Food.animal_type.like(f'%{data["search"]}%'),
                                  Food.pathologies.like(f'%{data["search"]}%'),Food.brand.like(f'%{data["search"]}%'))).all()

    accessories = Accessories.query.filter(or_(Accessories.name.like(f'%{data["search"]}%'),
                                               Accessories.animal_type.like(f'%{data["search"]}%'),
                                               Accessories.pathologies.like(f'%{data["search"]}%'), 
                                               Accessories.brand.like(f'%{data["search"]}%'))).all()
    # Queries vacias devolvemos not found
    if not foods and not accessories:
        return jsonify({"message":"not results found"}), 404

    # Si la query no esta vacia preparamos una lista con un diccionario y la serializacion de cada item
    # para poderla jsonificar en el return
    if len(foods) > 0:
        dict_foods = [{ "foods":[food.serialize() for food in foods]}]
    else:
        dict_foods = []
    if len(accessories) > 0:
        dict_accessories = [{"accessories":[accessory.serialize() for accessory in accessories]}]
    else:
        dict_accessories = []
    # concatenamos ambas listas obtenidas en las queries
    return jsonify(dict_foods + dict_accessories), 200


