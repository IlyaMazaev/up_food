from requests import get, post
from json import dumps


params_2 = {'search_request': 'курин'}

print(dumps(get('http://localhost:5000/api/recipes/search', params=params_2).json(), indent=4, ensure_ascii=False))

print(dumps(get('http://localhost:5000/api/recipes/5').json(), indent=4, ensure_ascii=False))