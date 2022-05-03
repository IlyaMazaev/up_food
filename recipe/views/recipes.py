import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from requests import get, post
from requests.auth import HTTPBasicAuth

from recipe.forms import AddNewRecipe
from recipe.models import Profile, Comments, RecipeModel
from recipe.serializers import RecipeSerializers
from random import randint

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


@login_required
def add_new_recipe(request):
    if request.method == 'POST':
        form = AddNewRecipe(request.POST, request.FILES)
        if form.is_valid():
            ins = form.save(commit=False)
            call_id = str(randint(30, 5000))
            while get('https://recipes-db-api.herokuapp.com/api/images/' + call_id).status_code != '404':
                call_id = str(randint(30, 5000))
            ins.photo_address = call_id
            ins.creator_id = request.user.id
            files = ins.save()
            RecipeModel.objects.first().delete()
            data = RecipeSerializers(ins)
            recipe_image_post = post('https://recipes-db-api.herokuapp.com/api/images/add', auth=basic,
                                     json=json.dumps(files))
            recipe_post = post('https://recipes-db-api.herokuapp.com/api/recipes', auth=basic, params=data.data)
            if recipe_post.status_code or recipe_image_post.status_code != '200':
                print(recipe_post.json())
                print(recipe_image_post.json())
                return HttpResponseServerError('<h1>Упс, что-то пошло не так.Попробуйте ещё раз</h1>')
            return redirect('/')
    else:
        form = AddNewRecipe()
    context = {
        'form': form
    }
    return render(request, 'recipes/recipe_create.html', context)
