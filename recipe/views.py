from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.timezone import now
from requests import get
from requests.auth import HTTPBasicAuth

from recipe.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm
from recipe.models import Profile, Comments

basic = HTTPBasicAuth('api_user', 'super_secret_password')


# Create your views here.

def main_page(request):
    q = ''
    day_time = ''
    d_t = now().hour + 3
    if d_t < 12 and d_t > 4:
        day_time = 'morning'
    elif d_t > 12 and d_t < 17:
        day_time = 'afternoon'
    elif d_t > 17 and d_t != 0:
        day_time = 'evening'
    else:
        day_time = 'night'
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    if q != '':
        params_search = {'search_request': q}
        rec = get('https://recipes-db-api.herokuapp.com/api/recipes/search', auth=basic, params=params_search).json()
    else:
        rec = get('https://recipes-db-api.herokuapp.com/api/recipes', auth=basic).json()
    context = dict(
        recipe=rec,
        q=q,
        day_time=day_time,
    )
    return render(request, 'main_page.html', context)


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
    return render(request, 'recipe_template.html', context)


def register(request):
    context = dict()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Профиль создан для {username}')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            request.session['form-submitted'] = True
            return redirect('/accounts/profile_register/')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)


def profile_register(request):
    if not request.session.get('form-submitted', False):
        raise Http404('Упс, что-то пошло не так')
    else:
        context = dict()
        if request.method == 'POST':
            form = ProfileRegisterForm(request.POST, instance=Profile.objects.get(user_id=request.user.id))
            if form.is_valid():
                form.save()
                request.session['form-submitted'] = False
                return redirect('/')
        else:
            form = ProfileRegisterForm(instance=Profile.objects.get(user_id=request.user.id))
        context = {
            'form': form,
        }
        return render(request, 'registration/profile_register.html', context)


def menu(request):
    user_photo = request.user.image
    context = dict(
        image=user_photo
    )
    return render(request, 'menu.html', context)


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


def add_fav(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    current_user = request.user
    fav = Profile.objects.get(user_id=current_user.id)
    fav.fav += q + ';'
    fav.save()
    return redirect('/recipe/?q=' + q)


def add_comment(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    current_profile = Profile.objects.get(user_id=request.user.id)
    text = request.GET.get('textbox')
    com = Comments.objects.create_comment(q, current_profile, text, 0)
    return redirect('/recipe/?q=' + q)


def remove_fav(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    current_user = request.user
    fav = Profile.objects.get(user_id=current_user.id)
    fav.fav = fav.fav.replace(q + ';', '')
    fav.save()
    return redirect('/favorite/')


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
            return redirect('/accounts/profile/')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)


def add_cart(request):
    ans = request.GET.getlist('dropdown')
    cart = Profile.objects.get(user_id=request.user.id)
    for i in ans:
        if i != 'Не требуется':
            if cart.cart.find(i + ';') == -1:
                cart.cart += i + ';'
    cart.save()
    return redirect('/')


def favorite(request):
    rec = list()
    current_user = request.user
    fav = Profile.objects.get(user_id=current_user.id)
    allfav = fav.fav.split(';')
    fav.save()
    for i in allfav:
        if len(i) >= 1:
            params_search = i.strip(';')
            rec.append(get('https://recipes-db-api.herokuapp.com/api/recipes/' + params_search, auth=basic).json())
    context = dict(
        fav=rec
    )
    return render(request, 'favorite.html', context)


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
