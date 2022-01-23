import base64
from json import dumps

from requests import get


sample_string = "api_user:super_secret_password"
sample_string_bytes = sample_string.encode("ascii")

base64_bytes = base64.b64encode(sample_string_bytes)
base64_password = base64_bytes.decode("ascii")

print(f"Encoded base 64 password: {base64_password}")

params_search = {f'Authorization': f'Basic {base64_password}',
                 'search_request': 'курин'}

only_auth_headers = {'Authorization': f'Basic {base64_password}'}


# для поиска:
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/search', params=params_search).json(), indent=4, ensure_ascii=False))

# рецепт по id
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/5', headers=only_auth_headers).json(), indent=4, ensure_ascii=False))

# все рецепты
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes', headers=only_auth_headers).json(), indent=4, ensure_ascii=False))

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
