from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("hello_haikyuu/", views.HelloHaikyuu.as_view(), name="hello_haikyuu"),    

    #Rutas para tabla nationals_travel
    path('nationals_travel/<str:action>/', views.NationalsTravel.as_view(), name='nationals_travel'), # POST request
    path('nationals_travel/<str:action>/<int:id>/', views.NationalsTravel.as_view(), name='nationals_travel'), # GET request

    #Rutas para tabla schools
    path('schools/<str:action>/', views.Schools.as_view(), name='schools'), # POST request
    path('schools/<str:action>/<int:id>/', views.Schools.as_view(), name='schools'), # GET request

    #Rutas para tabla stadiums
    path('stadiums/<str:action>/', views.Stadiums.as_view(), name='stadiums'), # POST request
    path('stadiums/<str:action>/<int:id>/', views.Stadiums.as_view(), name='stadiums') # GET request

]