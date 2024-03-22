from django.shortcuts import render

def index(request):
    """
    Function for the main landing page
    """

    return render(
        request,
        "index.html",
    )
