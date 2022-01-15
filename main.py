# -*- coding: utf-8 -*-
import os

import pymorphy2  # creating tags based on words morphology
from PIL import Image  # to show pics of recipes
from flask import Flask, jsonify, send_file
from flask_restful import reqparse, abort, Api, Resource

from data import db_session  # db engine
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

app = Flask(__name__)
app.config['SECRET_KEY'] = '9CB2FA9ED59693626BC2'


class RecipeResource(Resource):
    """
    Resource class for REST api
    """

    @staticmethod
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

    def get(self, recipe_id):
        """
        sends data in json of one recipe by its id given as param
        :param recipe_id:
        """
        self.abort_if_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        return jsonify({'recipe': recipe.to_dict()})

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
        return send_file(recipe.photo_address, mimetype='image/jpeg')


class RecipeListResource(Resource):
    """
    Resource class for REST api
    works with multiple recipes(lists)
    """

    @staticmethod
    def get():
        """
        sends list with all recipes in db
        """
        session = db_session.create_session()
        recipes = session.query(Recipe).all()
        return jsonify({'recipes': [item.to_dict() for item in recipes]})

    @staticmethod
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
                       photo_address=args['photo_address'])

        return jsonify({'success': 'OK'})


class SearchableRecipeListResource(Resource):
    """
    part of REST api, this one is for searching
    """

    @staticmethod
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
    def abort_if_not_found(recipe_id):
        """
        aborts 404 error if it can't fond recipe with given id
        :param recipe_id:
        """
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        if not recipe:
            abort(404, message=f"Recipe {recipe_id} not found")

    def get(self, recipe_id):
        """
        returns all products bonded to a recipe in json format
        :param recipe_id:
        """
        self.abort_if_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)

        return jsonify({'products': get_products_bonded_with_recipe(recipe)})


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


def add_new_recipe(name, ingredients, bonded_ingredients, how_to_cook, portions, time, types, photo_address=''):
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
                        bonded_ingredients=bonded_ingredients)

        db_sess.add(recipe)
        db_sess.commit()
        recipe.set_photo_address(photo_address)
        db_sess.commit()
        print(f'added recipe {name}')


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


def main():
    db_session.global_init("db/recipes_data.db")  # connecting to db
    db_sess = db_session.create_session()

    api = Api(app)

    api.add_resource(RecipeResource, '/api/recipes/<int:recipe_id>')
    api.add_resource(RecipeListResource, '/api/recipes')
    api.add_resource(SearchableRecipeListResource, '/api/recipes/search')
    api.add_resource(RecipeImageResource, '/api/recipes/photo/<int:recipe_id>')

    api.add_resource(ProductResource, '/api/products/<int:product_id>')
    api.add_resource(ProductListResource, '/api/products')
    api.add_resource(ProductsBondedListResource, '/api/products/for_recipe/<int:recipe_id>')

    app.run()

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
