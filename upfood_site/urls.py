"""upfood_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from recipe.views import main_page, recipe, register, profile, order, add_cart, add_fav, favorite, cart, clear_cart, remove_fav
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from upfood_site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),
    path('recipe/', recipe),
    path('accounts/profile/', profile),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register),
    path('order/', order),
    path('order/add_cart', add_cart),
    path('recipe/add_fav_recipe', add_fav),
    path('recipe/remove_fav_recipe', remove_fav),
    path('favorite/', favorite),
    path('cart/', cart),
    path('cart/clearcart', clear_cart),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
