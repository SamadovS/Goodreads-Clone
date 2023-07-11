from django.shortcuts import render


def landing_page(request):
    print(request.user.is_authenticated)
    return render(request, "landing.html")











