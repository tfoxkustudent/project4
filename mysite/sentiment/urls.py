from django.urls import path
from sentiment import views


"""
URL's that get checked when you reference another location in your html file
"""

urlpatterns = [
        path('', views.HomePageView, name='home'),
        path('about', views.AboutPageView, name='about'),
        path('one_item', views.OneItemFrame, name="one_item"),
        path('two_item', views.TwoItemFrame, name="two_item"),
        path('two_item_results', views.TwoItemResults, name='two_item_results')
]
