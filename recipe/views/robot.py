from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /accounts/",
        "Disallow: /order/",
        "Disallow: /recipe/add_fav_recipe/",
        "Disallow: /recipe/remove_fav_recipe/",
        "Disallow: /cart/",
        "Disallow: /recipe/add_comment/",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
