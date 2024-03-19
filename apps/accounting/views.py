from django.shortcuts import render

# Create your views here.


def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "accounting/index.html",
    )
