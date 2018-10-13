from django.conf.urls import url
from sentiment import views


"""
URL's that get checked when you reference another location in your html file
"""

urlpatterns = [
        url(r'^$', views.HomePageView.as_view()),
        url(r'^about/$', views.AboutPageView.as_view()), 
        url(r'^search$',views.search),
         
        ]

