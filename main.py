# -*- coding: utf-8 -*-
import base64
import json
import os
from io import BytesIO

import pymorphy2  # creating tags based on words morphology
from PIL import Image  # to show pics of recipes
from flask import Flask, jsonify, send_file, request
from flask_httpauth import HTTPBasicAuth
from flask_restful import reqparse, abort, Api, Resource

from data import db_session  # db engine
from data.images import Picture
from data.nutrition_programs import NutritionProgram  # orm NutritionProgram class
from data.products import Product  # orm Product class
from data.recipes import Recipe  # orm Recipe class

# arg parser for adding new recipes
recipe_post_parser = reqparse.RequestParser()
recipe_post_parser.add_argument('name', required=True)
recipe_post_parser.add_argument('ingredients', required=True)
recipe_post_parser.add_argument('how_to_cook', required=True)
recipe_post_parser.add_argument('portions', required=True)
recipe_post_parser.add_argument('time', required=True)
recipe_post_parser.add_argument('types', required=True)
recipe_post_parser.add_argument('bonded_ingredients', required=True)
recipe_post_parser.add_argument('photo_address', required=False)

# arg parser for recipe searching
recipe_tags_search_parser = reqparse.RequestParser()
recipe_tags_search_parser.add_argument('search_request', required=False)

# arg parser for adding new nutrition programs
n_program_post_parser = reqparse.RequestParser()
n_program_post_parser.add_argument('name', required=True)
n_program_post_parser.add_argument('meals_data_json', required=True)
n_program_post_parser.add_argument('type', required=True)
n_program_post_parser.add_argument('photo_address', required=False)


# arg parser for n programs searching
n_program_tags_search_parser = reqparse.RequestParser()
n_program_tags_search_parser.add_argument('search_request', required=False)


app = Flask(__name__)
app.config['SECRET_KEY'] = '9CB2FA9ED59693626BC2'
api = Api(app, prefix='/api')
auth = HTTPBasicAuth()

USER_DATA = {'api_user': 'super_secret_password'}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA[username] == password


class ImageResource(Resource):
    """
    Resource class for Images sent from main service
    """

    @staticmethod
    def abort_if_not_found(call_id):
        """
        aborts 404 error if it can't fond recipe with given id
        same as in RecipeResource class
        :param call_id:
        """
        session = db_session.create_session()
        image = session.query(Picture).filter(Picture.call_id == call_id).first()
        if not image:
            abort(404, message=f"Image {call_id} not found")

    def get(self, call_id):
        """
        sends image of recipe with id given as param
        :param call_id:
        """
        self.abort_if_not_found(call_id)
        session = db_session.create_session()
        image = session.query(Picture).filter(Picture.call_id == call_id).first()
        return send_file(image.photo_address, mimetype='image/jpeg')


class ImagePostResource(Resource):
    @staticmethod
    @auth.login_required
    def post():
        """
        adds new image
        """
        print('post')
        json_data = request.get_json()  # Get the POSTed json
        dict_data = json.loads(json_data)  # Convert json to dictionary

        img = dict_data["img"]  # Take out base64# str
        img = base64.b64decode(img)  # Convert image data converted to base64 to original binary data# bytes
        img = BytesIO(img)  # _io.Converted to be handled by BytesIO pillow
        img = Image.open(img)

        img.save(f'static/img/{dict_data["file_name"]}')  # saving file in static/img folder

        # adding record to database
        db_sess = db_session.create_session()
        # if there are a image with the name like that
        if db_sess.query(Picture).filter(Picture.call_id == dict_data['call_id']).first():
            print(f'this recipe already exists({dict_data["call_id"]})')
            abort(500, message=f'this recipe already exists({dict_data["call_id"]})')

        else:
            # creating Image class object
            image = Picture(call_id=dict_data['call_id'],
                            photo_address=f'static/img/{dict_data["file_name"]}')

            db_sess.add(image)
            db_sess.commit()
            db_sess.commit()

        return jsonify({'success': 'OK'})


class RecipeResource(Resource):
    """
    Resource class for REST api
    """

    @staticmethod
    @auth.login_required
    def abort_if_not_found(recipe_id):
        """
        aborts 404 error if it can't fond recipe with given id
        func used in get and delete
        :param recipe_id:
        """
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        if not recipe:
            abort(404, message=f"Recipe {recipe_id} not found")

    @auth.login_required
    def get(self, recipe_id):
        """
        sends data in json of one recipe by its id given as param
        :param recipe_id:
        """
        self.abort_if_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        return jsonify({'recipe': recipe.to_dict()})

    @auth.login_required
    def delete(self, recipe_id):
        """
        deletes recipe with id given as param
        :param recipe_id:
        """
        self.abort_if_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        session.delete(recipe)
        session.commit()
        return jsonify({'success': 'OK'})


class RecipeImageResource(Resource):
    """
    REST resource class needed to work with images of recipes
    """

    @staticmethod
    def abort_if_not_found(recipe_id):
        """
        aborts 404 error if it can't fond recipe with given id
        same as in RecipeResource class
        :param recipe_id:
        """
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        if not recipe:
            abort(404, message=f"Recipe {recipe_id} not found")

    def get(self, recipe_id):
        """
        sends image of recipe with id given as param
        :param recipe_id:
        """
        self.abort_if_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)

        if recipe.photo_address[:8] == 'call_id:':
            session = db_session.create_session()
            image = session.query(Picture).filter(Picture.call_id == int(recipe.photo_address.split(":")[1])).first()
            return send_file(image.photo_address, mimetype='image/jpeg')
        else:
            return send_file(recipe.photo_address, mimetype='image/jpeg')


class RecipeListResource(Resource):
    """
    Resource class for REST api
    works with multiple recipes(lists)
    """

    @staticmethod
    @auth.login_required
    def get():
        """
        sends list with all recipes in db
        """
        session = db_session.create_session()
        recipes = session.query(Recipe).all()
        return jsonify({'recipes': [item.to_dict() for item in recipes]})

    @staticmethod
    @auth.login_required
    def post():
        """
        adds new recipe with args given as parameters of web post request
        """
        args = recipe_post_parser.parse_args()
        add_new_recipe(name=args['name'],
                       ingredients=args['ingredients'],
                       how_to_cook=args['how_to_cook'],
                       portions=args['portions'],
                       time=args['time'],
                       types=args['types'],
                       bonded_ingredients=args['bonded_ingredients'],
                       photo_address=args['photo_address'],
                       creator_id=args['creator_id'])

        return jsonify({'success': 'OK'})


class SearchableRecipeListResource(Resource):
    """
    part of REST api, this one is for searching
    """

    @staticmethod
    @auth.login_required
    def get():
        """
        gets search request as param of get post request
        it's basically recipe_tags_search() function wrapped in REST api format
        sends back all found recipes as jsons
        """
        args = recipe_tags_search_parser.parse_args()

        # session = db_session.create_session()
        print(args['search_request'])
        recipes = recipe_tags_search(args['search_request'])

        return jsonify({'recipes': [item.to_dict() for item in recipes]})


class ProductResource(Resource):
    """
    Resource class for REST api
    """

    @staticmethod
    @auth.login_required
    def abort_if_not_found(product_id):
        """
        aborts 404 error if it can't fond recipe with given id
        same as in RecipeResource
        :param product_id:
        """
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        if not product:
            abort(404, message=f"Recipe {product_id} not found")

    @auth.login_required
    def get(self, product_id):
        """
        sends data in json of one product by its id given as param
        :param product_id:
        """
        self.abort_if_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        return jsonify({'product': product.to_dict()})


class ProductListResource(Resource):
    """
    Resource class for REST api
    works with multiple products(lists)
    """

    @staticmethod
    @auth.login_required
    def get():
        """
        sends list with all recipes in db
        """
        session = db_session.create_session()
        products = session.query(Product).all()
        return jsonify({'products': [item.to_dict() for item in products]})


class ProductsBondedListResource(Resource):
    """
    class to wrap up get_products_bonded_with_recipe() func in REST api format
    """

    @staticmethod
    @auth.login_required
    def abort_if_not_found(recipe_id):
        """
        aborts 404 error if it can't fond recipe with given id
        :param recipe_id:
        """
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        if not recipe:
            abort(404, message=f"Recipe {recipe_id} not found")

    @auth.login_required
    def get(self, recipe_id):
        """
        returns all products bonded to a recipe in json format
        :param recipe_id:
        """
        self.abort_if_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)

        return jsonify({'products': get_products_bonded_with_recipe(recipe)})




class NutritionProgramResource(Resource):
    """
    Resource class for REST api
    """

    @staticmethod
    @auth.login_required
    def abort_if_not_found(nutrition_program_id):
        """
        aborts 404 error if it can't fond recipe with given id
        func used in get and delete
        :param nutrition_program_id:
        """
        session = db_session.create_session()
        recipe = session.query(NutritionProgram).get(nutrition_program_id)
        if not recipe:
            abort(404, message=f"NutritionProgram {nutrition_program_id} not found")

    @auth.login_required
    def get(self, nutrition_program_id):
        """
        sends data in json of one recipe by its id given as param
        :param nutrition_program_id:
        """
        self.abort_if_not_found(nutrition_program_id)
        session = db_session.create_session()
        n_program = session.query(NutritionProgram).get(nutrition_program_id)
        return jsonify({'nutrition_program': n_program.to_dict()})

    @auth.login_required
    def delete(self, nutrition_program_id):
        """
        deletes recipe with id given as param
        :param nutrition_program_id:
        """
        self.abort_if_not_found(nutrition_program_id)
        session = db_session.create_session()
        n_program = session.query(NutritionProgram).get(nutrition_program_id)
        session.delete(n_program)
        session.commit()
        return jsonify({'success': 'OK'})


class NutritionProgramImageResource(Resource):
    """
    REST resource class needed to work with images of nutrition programs
    """

    @staticmethod
    @auth.login_required
    def abort_if_not_found(nutrition_program_id):
        """
        aborts 404 error if it can't fond recipe with given id
        func used in get and delete
        :param nutrition_program_id:
        """
        session = db_session.create_session()
        recipe = session.query(NutritionProgram).get(nutrition_program_id)
        if not recipe:
            abort(404, message=f"NutritionProgram {nutrition_program_id} not found")

    @auth.login_required
    def get(self, nutrition_program_id):
        """
        sends image of recipe with id given as param
        :param nutrition_program_id:
        """
        self.abort_if_not_found(nutrition_program_id)
        session = db_session.create_session()
        n_program = session.query(NutritionProgram).get(nutrition_program_id)
        return send_file(n_program.photo_address, mimetype='image/jpeg')


class NutritionProgramListResource(Resource):
    """
    Resource class for REST api
    works with multiple nutrition programs (lists)
    """

    @staticmethod
    @auth.login_required
    def get():
        """
        sends list with all nutrition programs in db
        """
        session = db_session.create_session()
        n_programs = session.query(Recipe).all()
        return jsonify({'nutrition_programs': [item.to_dict() for item in n_programs]})

    @staticmethod
    @auth.login_required
    def post():
        """
        adds new nutrition program with args given as parameters of web post request
        """
        args = n_program_post_parser.parse_args()
        add_new_recipe(name=args['name'],
                       ingredients=args['meals_data_json'],
                       how_to_cook=args['type'],
                       photo_address=args['photo_address'])

        return jsonify({'success': 'OK'})


class SearchableNutritionProgramListResource(Resource):
    """
    part of REST api, this one is for searching
    """

    @staticmethod
    @auth.login_required
    def get():
        """
        gets search request as param of get post request
        it's basically recipe_tags_search() function wrapped in REST api format
        sends back all found recipes as jsons
        """
        args = n_program_tags_search_parser.parse_args()

        # session = db_session.create_session()
        print(args['search_request'])
        n_programs = nutrition_program_tags_search(args['search_request'])

        return jsonify({'nutrition_programs': [item.to_dict() for item in n_programs]})








@app.route('/')
@app.route('/index')
def index():
    return "index page (just a place holder)"


def get_all_word_forms(word):
    """input: a word ex:'makaroni'
        returns list of word's forms ex: ['makaronov', 'makarons']"""

    morph = pymorphy2.MorphAnalyzer()
    # getting an infinitive(normal) form of the word
    word_parse = morph.parse(word)[0]  # taking the first parse of the word
    normal_form_word = word_parse.normal_form

    # and creating a set containing only this normal form
    all_forms_set = {str(normal_form_word)}

    # source: https://github.com/kmike/pymorphy2/issues/74
    parse_list = morph.parse(word)  # list of all possible parses
    for parse in parse_list:
        lexeme = parse.lexeme
        for form in lexeme:
            all_forms_set.add(str(form.word))

    # print(all_forms_set)
    return list(all_forms_set)


def create_tags_for_line(line):
    """creating tags for line of words
    can be used with any type of sentences, names, and such things
    returns line of tags looking like this: 'line;tag1;tag2;tag3'
     tags in this case are the words used in line and their grammatical forms"""
    # replaces some symbols
    line = line.replace("'", '')
    line = line.replace('"', '')
    line = line.replace('_', ' ')
    line = line.replace('_', ' ')
    line = line.replace('«', '')
    line = line.replace('»', '')
    tags = ''

    for word in line.split():  # creating tags for each word
        all_word_forms = get_all_word_forms(word.lower())
        tags += ';'.join(all_word_forms)  # adding word's tags to a single tags line

    return line.lower() + ';' + ';'.join(line.split()).lower() + tags.lower()


def add_new_recipe(name, ingredients, bonded_ingredients, how_to_cook, portions, time, types, creator_id,
                   photo_address=''):
    """adds new recipe to the db
    needs recipe name, ingredients in format: 'ingr1;ingr2;ingr3'
    tags are being created using create_tags_for_line(name)

    format of bonded_ingredients dict:
    {ingredient name: [matching product ids in db]}
    """
    db_sess = db_session.create_session()
    # if there are a recipe with the name like that
    if db_sess.query(Recipe).filter(Recipe.name == name).first():
        print(f'this recipe already exists({name})')

    else:
        # creating Recipe class object
        recipe = Recipe(name=name,
                        ingredients=ingredients,
                        how_to_cook=how_to_cook,
                        tags=create_tags_for_line(name),
                        portions=portions,
                        time=time,
                        types=types,
                        bonded_ingredients=bonded_ingredients,
                        creator_id=creator_id)

        db_sess.add(recipe)
        db_sess.commit()
        recipe.set_photo_address(photo_address)
        db_sess.commit()
        print(f'added recipe {name}')


def add_new_nutrition_program(name, meals_data_json, type, photo_address=''):
    """adds new nutrition program to the db
    needs program name, and its data in format:
    {
    'days':
        [
            {'meals': [
                {'name': 'program_name', 'time': 'time_of_this_meal', 'recipes': ['id_1', 'id_2']},
                {'name': 'program_name2', 'time': 'time_of_this_meal2', 'recipes': ['id_3', 'id_4']}
            ]}
        ]
}

    tags are being created using create_tags_for_line(name + type)
    """
    db_sess = db_session.create_session()
    # if there are a recipe with the name like that
    if db_sess.query(Recipe).filter(Recipe.name == name).first():
        print(f'this recipe already exists({name})')

    else:
        # creating NutritionProgram class object
        n_program = NutritionProgram(name=name,
                                     meals_data_json=meals_data_json,
                                     tags=create_tags_for_line(name + type),
                                     type=type)

        db_sess.add(n_program)
        db_sess.commit()
        n_program.set_photo_address(photo_address)
        db_sess.commit()
        print(f'added nutrition program {name}')


def add_new_product(name, store, price, type, photo_address=''):
    """adds new product to the db
        needs product name, store and price
        tags are being created using create_tags_for_line(name)
        """
    db_sess = db_session.create_session()
    # if there are a product with the name like that
    if db_sess.query(Product).filter(Product.name == name).first():
        print(f'this product already exists({name})')

    else:
        # creating Recipe class object
        product = Product(name=name,
                          store=store,
                          price=price,
                          type=type,
                          tags=create_tags_for_line(name))
        product.set_photo_address(photo_address)
        db_sess.add(product)
        db_sess.commit()


def recipe_tags_search(search_input):
    """input: searching request
    output: prints found recipes and opens photos
    returns a list of found Recipe objects """

    recipes_found = list()  # list which contains all found recipes
    for word in search_input.split():  # each word is an separated key
        db_sess = db_session.create_session()
        # searches for recipes where tags contain word
        search_query = db_sess.query(Recipe).filter(Recipe.tags.like('%' + word.lower() + '%')).all()
        print(search_query)

        for found_recipe in search_query:  # found recipes for word
            recipes_found.append(found_recipe)
            # printing data
            print('-' * 1000)
            print(found_recipe)
            print(found_recipe.how_to_cook)
            if os.path.isfile(found_recipe.photo_address):  # showing pic if exists
                with Image.open(found_recipe.photo_address) as img:
                    img.show()
            print('-' * 1000)
    # returns a list of found Recipe objects
    return recipes_found


def products_for_recipe_search(search_input):
    """
    input: searching request
    output: prints found products
    returns a list of found Product with matching name"""

    products_found = list()  # list which contains all found recipes
    search_query = []
    for word in list(map(lambda x: x.lower(), search_input.split())):  # each word is an separated search key
        if word not in ['и', 'с', 'из', 'для']:  # filtering prepositions
            db_sess = db_session.create_session()

            # if search_query was empty creates it with search by first word from request
            search_query = db_sess.query(Product).filter(Product.tags.ilike('%' + word.lower() + '%')).all()

            '''
            # filters the list and leaves only products which names contain the word
            
            print(list(filter(lambda x: word.lower() in list(map(lambda x: x.lower(), x.name.split())), search_query)))
            search_query = list(filter(lambda x: word.lower() in list(map(lambda x: x.lower(), x.name.split())), search_query))
            '''

            for found_product in search_query:  # found products for word
                products_found.append(found_product)
    # returns a list of found Recipe objects
    print(products_found)
    return products_found


def get_products_bonded_with_recipe(recipe):
    """returns dict with Product objects bonded with recipe
    return format
    {ingredient name: [Product, Product]}"""
    db_sess = db_session.create_session()

    bonded_products = dict()
    for recipe_name, product_ids in recipe.bonded_ingredients.items():
        bonded_products[recipe_name] = []
        for product_id in product_ids:
            bonded_products[recipe_name].append(db_sess.query(Product).get(product_id).to_dict())

    print(bonded_products)
    return bonded_products


def nutrition_program_tags_search(search_input):
    """input: searching request
    output: prints found nutrition programs
    returns a list of found NutritionProgram objects """

    n_programs_found = list()  # list which contains all found recipes
    for word in search_input.split():  # each word is an separated key
        db_sess = db_session.create_session()
        # searches for recipes where tags contain word
        search_query = db_sess.query(NutritionProgram).filter(
            NutritionProgram.tags.like('%' + word.lower() + '%')).all()
        print(search_query)

        for found_n_program in search_query:  # found recipes for word
            n_programs_found.append(found_n_program)
            # printing data

    # returns a list of found NutritionProgram objects
    return n_programs_found


def main():
    db_session.global_init("db/recipes_data.db")  # connecting to db
    db_sess = db_session.create_session()

    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(SearchableRecipeListResource, '/recipes/search')
    api.add_resource(RecipeImageResource, '/recipes/photo/<int:recipe_id>')

    api.add_resource(ProductResource, '/products/<int:product_id>')
    api.add_resource(ProductListResource, '/products')
    api.add_resource(ProductsBondedListResource, '/products/for_recipe/<int:recipe_id>')

    api.add_resource(NutritionProgramResource, '/nutrition_programs/<int:nutrition_program_id>')
    api.add_resource(NutritionProgramListResource, '/nutrition_programs')
    api.add_resource(SearchableNutritionProgramListResource, '/nutrition_programs/search')
    api.add_resource(NutritionProgramImageResource, '/nutrition_programs/photo/<int:nutrition_program_id>')

    api.add_resource(ImagePostResource, '/images/add')
    api.add_resource(ImageResource, '/images/<int:call_id>')

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

    '''
    for el in products_for_recipe_search(input()):
        print(el)
    '''
    '''
    print(db_sess.query(Product).filter(Product.tags.like('%' + 'мука' + '%')).first())
    print(db_sess.query(Product).filter(Product.tags.like('%' + 'мука' + '%')).first().get_json_data())
    '''
    '''
    product_prices_sum = 0  # stores sum of ingredients prices
    for found_recipe in recipe_tags_search(input()):  # for all matching recipes
        print(found_recipe.ingredients)  # prints ingredients
        for ingredient in found_recipe.ingredients.split(';'):  # iterating product ingredients
            print(ingredient.split(' - ')[0])
            products_found = products_for_recipe_search(ingredient.split(' - ')[0])  # getting list of matching products
            try:
                product_prices_sum += int(
                    products_found[0].price)  # if found adds price of first element to sum variable
            except IndexError:
                pass  # of sequence is empty does nothing
    print(f'Итого: {product_prices_sum}')  # printing sum of found products
    '''


if __name__ == '__main__':
    main()
