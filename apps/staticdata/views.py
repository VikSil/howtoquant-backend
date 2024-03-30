from django.shortcuts import render
import datetime as dt
import pandas as pd
import pandas_datareader as web




def index(request):
    """
    Function for the main landing page
    """



    return render(
        request,
        "index.html",
    )
