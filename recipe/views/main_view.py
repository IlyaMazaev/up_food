from django.shortcuts import render
from django.utils.timezone import now
from requests import get
from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('api_user', 'super_secret_password')


def main_page(request):
    q = ''
    day_time = ''
    d_t = now().hour + 3
    if 12 > d_t > 4:
        day_time = 'morning'
    elif 12 < d_t < 17:
        day_time = 'afternoon'
    elif d_t > 17 and d_t != 0:
        day_time = 'evening'
    else:
        day_time = 'night'
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    if q != '':
        params_search = {'search_request': q}
        rec = get('https://takecook-api.herokuapp.com/api/recipes/search', auth=basic, params=params_search).json()
    else:
        rec = get('https://takecook-api.herokuapp.com/api/recipes', auth=basic).json()
    context = dict(
        recipe=rec,
        q=q,
        day_time=day_time,
    )
    return render(request, 'main_page.html', context)


def menu(request):
    user_photo = request.user.image
    context = dict(
        image=user_photo
    )
    return render(request, 'menu.html', context)


def privacy(request):
    return render(request, 'info/privacy.html')


def about(request):
    return render(request, 'info/about.html')


def contacts(request):
    return render(request, 'info/contacts.html')
