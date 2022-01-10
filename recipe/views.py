from recipe.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from database_work.main_recipes_api import recipe_tags_search, get_products_bonded_with_recipe



# Create your views here.

def main_page(request):
    q = ' '
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
    q = ''
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    rec = recipe_tags_search(q)[0].get_json_data()
    context = dict(
        recipe=rec,
        ing = rec.get('ingredients').split(';')
    )
    return render(request, 'recipe_template.html', context)

def register(request):
    context = dict()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Профиль создан для {username}')
            return redirect('/')
    else:
        form = UserRegisterForm()
    context['form'] = form
    return render(request, 'registration/register.html', context)

def order(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    rec = recipe_tags_search(q)[0].get_json_data()
    products_dict = get_products_bonded_with_recipe(recipe_tags_search(q)[0])
    products_list = list(products_dict.values())
    ingredients_list = list(products_dict.keys())
    context = dict(
        recipe=rec,
        ing=ingredients_list,
        products=products_list,
        prod_dict=products_dict

    )
    return render(request, "order_form.html", context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Изменения профиля сохранены для {username}')
            return redirect('/profile/')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)





