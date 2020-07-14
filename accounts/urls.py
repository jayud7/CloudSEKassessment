from django.urls import path

from . import views

urlpatterns = [
    path("",views.call_api, name='call_api'),
    path("register",views.register, name='register'),
    path("login",views.login, name='login'),
    path("logout",views.logout, name='logout'),
    path("call_api",views.call_api, name='call_api')
]