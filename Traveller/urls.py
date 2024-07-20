from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('login',views.login,name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('destination', views.destination, name='destination'),
    path('travelplace/<int:id>/', views.travelplace, name='travelplace'),
    path('travelplace/<int:id>/bookthetrip', views.bookthetrip, name='bookthetrip'),
    path('travelplace/<int:id>/tripquery', views.tripquery, name='tripquery'),
    path('mytrips',views.mytrips,name='mytrips'),
    path('myprofile',views.myprofile,name='myprofile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('search_destination',views.search_destination,name="search_redirect"),
]