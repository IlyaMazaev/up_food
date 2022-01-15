from requests import get, post
from json import dumps


params_search = {'search_request': 'курин'}

# для поиска:
print(dumps(get('http://localhost:5000/api/recipes/search', params=params_search).json(), indent=4, ensure_ascii=False))

# рецепт по id
print(dumps(get('http://localhost:5000/api/recipes/5').json(), indent=4, ensure_ascii=False))

# все рецепты
print(dumps(get('http://localhost:5000/api/recipes').json(), indent=4, ensure_ascii=False))