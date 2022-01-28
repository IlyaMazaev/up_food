from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from database_work.main_recipes_api import recipe_tags_search, get_products_bonded_with_recipe
from recipe.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from recipe.models import Profile

alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


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
        ing=rec.get('ingredients').split(';'),
        q=q
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
        prod_dict=products_dict,
        q=q

    )
    return render(request, "order_form.html", context)


def add_cart(request):
    cart = list()
    ans = list()
    ans = request.GET.getlist('dropdown')
    cart = Profile.objects.get(id=request.user.id)
    for i in ans:
        cart.cart += i + ';'
    cart.save()
    return redirect('/')


def add_fav(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    current_user = request.user
    fav = Profile.objects.get(id=current_user.id)
    fav.fav += q + ';'
    fav.save()
    return redirect('/')


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


def favorite(request):
    rec = list()
    current_user = request.user
    fav = Profile.objects.get(id=current_user.id)
    allfav = fav.fav.split(';')
    fav.save()
    for i in allfav:
        if len(i) >= 1:
            rec.append(recipe_tags_search(i.strip(';'))[0].get_json_data())
    context = dict(
        fav=rec
    )
    return render(request, 'favorite.html', context)


def cart(request):
    price = 0.0
    c = 0
    cart = Profile.objects.get(id=request.user.id)
    all_cart = cart.cart.split(';')
    cart.save()
    for i in all_cart:
        price_list = i.split(' ')
        for j in price_list:
            for k in j.split(','):
                if k.isdigit() == True:
                    c += 1
                if c == len(j.split(',')):
                    price += float(j.replace(',','.'))
                    c = 0
    price = '{:.2f}'.format(price)

    context = dict(
        price=price,
        prod = all_cart,
    )
    return render(request, 'cart.html', context)
