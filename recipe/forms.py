from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('NS', 'Не указано')
    )
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Эта почта уже используется в другом аккаунте. Если вы забыли пароль, воспользуйтесь сбросом пароля')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        model2 = Profile
        fields2 = ['gender']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']