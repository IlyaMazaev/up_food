from django.contrib import messages
from django.shortcuts import render, redirect
from requests import get

from recipe.forms import UserUpdateForm, ProfileUpdateForm
from recipe.models import Profile, Comments


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
    return render(request, 'registration/../../templates/profile/profile.html', context)


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
    return render(request, 'profile/favorite.html', context)
