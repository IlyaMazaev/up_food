from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect

from recipe.forms import UserRegisterForm, ProfileRegisterForm
from recipe.models import Profile


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
