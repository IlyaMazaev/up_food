from django.core import serializers
from django.shortcuts import render, redirect
from requests import get, post
from requests.auth import HTTPBasicAuth

from recipe.forms import AddNewRecipe
from recipe.models import Profile, Comments, RecipeModel
from recipe.serializers import RecipeSerializers

basic = HTTPBasicAuth('api_user', 'super_secret_password')


def recipe(request):
    q = ''
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    rec = get('https://recipes-db-api.herokuapp.com/api/recipes/' + q, auth=basic).json()
    logged = request.user.is_authenticated
    dis_button_fav = False
    if logged:
        current_user = request.user
        fav = Profile.objects.get(user_id=current_user.id)
        allfav = fav.fav.split(';')
        if q in allfav:
            dis_button_fav = True
    recipe_id = rec.get('recipe').get('id')
    comments = Comments.objects.filter(recipe_id=recipe_id)
    context = dict(
        recipe=rec,
        ing=rec.get('recipe').get('ingredients').split(';'),
        q=q,
        disable=dis_button_fav,
        comments=comments,
    )
    return render(request, 'recipes/recipe_template.html', context)


def add_new_recipe(request):
    if request.method == 'POST':
        form = AddNewRecipe(request.POST)
        if form.is_valid():
            form.save()
            data = RecipeSerializers(RecipeModel.objects.first())
            RecipeModel.objects.all().delete()
            r = post('https://recipes-db-api.herokuapp.com/api/recipes', auth=basic, params=data.data)
            print(r.status_code)
            return redirect('/')
    else:
        form = AddNewRecipe()
    context = {
        'form': form
    }
    return render(request, 'recipes/recipe_create.html', context)
