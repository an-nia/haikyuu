from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
#router.register(r'nationals_travel', views.NationalsTravelModelViewSet)
#router.register(r'schools', views.SchoolsModelViewSet)
#router.register(r'stadiums', views.StadiumsModelViewSet)

urlpatterns = [
    path("hello_haikyuu/", views.HelloHaikyuu.as_view(), name="hello_haikyuu"),
    
    path('', include(router.urls)),
]