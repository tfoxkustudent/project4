from django.urls import path
from sentiment import views

urlpatterns = [
        path('', views.HomePageView, name='home'),
        path('about', views.AboutPageView, name='about'),
        path('one_item', views.OneItemFrame, name="one_item"),
        path('two_item', views.TwoItemFrame, name="two_item"),
        path('three_item', views.ThreeItemFrame, name="three_item"),
        path('four_item', views.FourItemFrame, name="four_item"),
        path('results', views.Results, name='results')
]
