from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from requests import get
from requests.auth import HTTPBasicAuth

from recipe.models import Profile

basic = HTTPBasicAuth('api_user', 'super_secret_password')


def order(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    rec = get('https://recipes-db-api.herokuapp.com/api/recipes/' + q, auth=basic).json()
    products_dict = get('https://recipes-db-api.herokuapp.com/api/products/for_recipe/' + q,
                        auth=basic).json()
    products_list = list(products_dict.get('products').values())
    ingredients_list = list(products_dict.get('products').keys())
    context = dict(
        recipe=rec,
        ing=ingredients_list,
        products=products_list,
        prod_dict=products_dict,
        q=q

    )
    return render(request, "order_form.html", context)


@login_required
def add_cart(request):
    ans = request.GET.getlist('dropdown')
    cart = Profile.objects.get(user_id=request.user.id)
    for i in ans:
        if i != 'Не требуется':
            if cart.cart.find(i + ';') == -1:
                cart.cart += i + ';'
    cart.save()
    return redirect('/')


def clear_cart(request):
    cart = Profile.objects.get(user_id=request.user.id)
    cart.cart = ''
    cart.save()
    return redirect('/')


def remove_from_cart(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    cart = Profile.objects.get(user_id=request.user.id)
    cart.cart = cart.cart.replace(q, '')
    cart.save()
    return redirect('/cart/')


def cart(request):
    price = 0.0
    c = 0
    cart = Profile.objects.get(user_id=request.user.id)
    all_cart = cart.cart.split(';')
    cart.save()
    for i in all_cart:
        price_list = i.split(' ')
        for j in price_list:
            if ',' in j:
                for k in j.split(','):
                    if k.isdigit() == True:
                        c += 1
                    if c == len(j.split(',')):
                        price += float(j.replace(',', '.'))
                        c = 0
    price = '{:.2f}'.format(price)
    context = dict(
        price=price,
        prod=all_cart,
    )
    return render(request, 'cart.html', context)
