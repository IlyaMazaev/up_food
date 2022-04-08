from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.timezone import now

from .models import Profile, RecipeModel


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput())
    email = forms.EmailField(label='Почта')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            'Эта почта уже используется в другом аккаунте. Если вы забыли пароль, воспользуйтесь сбросом пароля')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileRegisterForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('NS', 'Не указано')
    )
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES)
    birth_date = forms.DateField(label='Дата рождения',
                                 widget=DateInput(attrs={'max': str(now().year - 13) + '-01-01', 'min': '1917-11-07'}))

    class Meta:
        model = Profile
        fields = ['gender', 'birth_date']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('NS', 'Не указано')
    )
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES)
    image = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['gender', 'image']


class AddNewRecipe(forms.ModelForm):
    name = forms.CharField(label='Название')
    ingredients = forms.CharField(label='Продукты',
                                  help_text='Вводите ингредиенты  и их граммовки через  точку запятую. '
                                            'Пример: Грудка курина 300 гр; Картофель молодой 1 кг; ...')
    instructions = forms.CharField(label='Инструкция по приготовлению')
    tags = forms.CharField(label='Тэги', required=False)
    image = forms.ImageField(label='Изображение', required=False)
    products = forms.CharField(required=False, label='Продукты')
    portions = forms.IntegerField(label='Количество порций')
    time = forms.CharField(label='Время готовки')

    class Meta:
        model = RecipeModel
        fields = ['name', 'ingredients', 'instructions', 'tags', 'image', 'products', 'portions', 'time']
