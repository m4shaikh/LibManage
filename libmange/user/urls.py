from django.urls import path
from . import views
url_paterns = [
    path('/signup' , views.signup , name = 'signup'),
    path('/login',views.login , name = 'login')
]