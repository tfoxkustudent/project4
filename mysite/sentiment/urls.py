from django.urls import path
from sentiment import views


"""
URL's that get checked when you reference another location in your html file
"""

urlpatterns = [
        path('', views.HomePageView, name='home'),
        path('about', views.AboutPageView, name='about'),
        path('basic', views.BasicPageView, name='basic'),
        path('election', views.ElectionFrame, name="election"),
        path('stocks', views.StocksFrame, name="stocks")
        ]
