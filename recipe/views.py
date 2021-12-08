from django.shortcuts import render

from database_work.main_recipes_api import recipe_tags_search



# Create your views here.
def main_page(request):
    q = 'Борщ c говядиной'
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    try:
        rec = recipe_tags_search(q)[0].get_json_data()
    except IndexError:
        rec = {'name': 'Ничего не найдено'}
    context = dict(
        recipe=rec,
        q=q
    )
    return render(request, 'main_page.html', context)


def recipe(request):
    q = 'Борщ'
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    rec = recipe_tags_search(q)[0].get_json_data()
    context = dict(
        recipe=rec,
        ing = rec.get('ingredients').split(';')
    )
    return render(request, 'recipe_template.html', context)
