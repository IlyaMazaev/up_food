from requests import get
from json import dumps


params_search = {'search_request': 'курин'}

# для поиска:
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/search', params=params_search).json(), indent=4, ensure_ascii=False))

# рецепт по id
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/5').json(), indent=4, ensure_ascii=False))

# все рецепты
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes').json(), indent=4, ensure_ascii=False))

'''
все адреса
api.add_resource(RecipeResource, '/api/recipes/<int:recipe_id>')
api.add_resource(RecipeListResource, '/api/recipes')
api.add_resource(SearchableRecipeListResource, '/api/recipes/search')
api.add_resource(RecipeImageResource, '/api/recipes/photo/<int:recipe_id>')

api.add_resource(ProductResource, '/api/products/<int:product_id>')
api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductsBondedListResource, '/api/products/for_recipe/<int:recipe_id>')
'''