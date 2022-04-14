import base64
from json import dumps

from requests import get
from requests.auth import HTTPBasicAuth

# генерация строки user:pass в base 64 кодировке
sample_string = "api_user:super_secret_password"
sample_string_bytes = sample_string.encode("ascii")

base64_bytes = base64.b64encode(sample_string_bytes)
base64_password = base64_bytes.decode("ascii")

print(f"Encoded base 64 password: {base64_password}")
# для поиска
params_search = {'search_request': 'курин'}

# для авторизации по заголовкам
only_auth_headers = {'Authorization': f'Basic {base64_password}'}

# для авторизации через механизмы request
basic = HTTPBasicAuth('api_user', 'super_secret_password')
'''
# авторизация по заголовкам
# для поиска:
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/search', headers=only_auth_headers,
                params=params_search).json(), indent=4, ensure_ascii=False))

# рецепт по id
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/5', headers=only_auth_headers).json(), indent=4,
            ensure_ascii=False))

# все рецепты
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes', headers=only_auth_headers).json(), indent=4,
            ensure_ascii=False))

# авторизация через requests
# для поиска:
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/search', auth=basic, params=params_search).json(),
            indent=4, ensure_ascii=False))

# рецепт по id
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes/5', auth=basic).json(), indent=4, ensure_ascii=False))

# все рецепты
print(dumps(get('https://recipes-db-api.herokuapp.com/api/recipes', auth=basic).json(), indent=4, ensure_ascii=False))
'''
import requests
from PIL import Image
import json
import base64
from io import BytesIO

img = Image.open("C:/Users/admin/Desktop/colors_3.jpg")

# Convert Pillow Image to bytes and then to base64
buffered = BytesIO()
img.save(buffered, format="JPEG")
img_byte = buffered.getvalue()  # bytes
img_base64 = base64.b64encode(img_byte)  # Base64-encoded bytes * not str

# It's still bytes so json.Convert to str to dumps(Because the json element does not support bytes type)
img_str = img_base64.decode('utf-8')  # str

files = {
    "file_name": "color_3.jpg",
    "call_id": '2',
    "img": img_str
}

r = requests.post("http://127.0.0.1:5000/api/images/add", json=json.dumps(files), headers=only_auth_headers)  # POST to server as json

print(r.json())

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
