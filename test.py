from requests import get, post
from json import dumps

params = {'name': '123',
          'ingredients': '123',
          'how_to_cook': '123',
          'portions': '123',
          'time': '123',
          'types': '123',
          'bonded_ingredients': {'Картофель': [1242, 1244]}
          }

params_2 = {'search_request': 'курин'}

print(dumps(get('http://localhost:5000/api/products/1').json(), indent=4, ensure_ascii=False))
