from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),   
    path('cafe/', views.cafe, name='cafe'),   
    path('theme/', views.theme, name='theme'), 
    path('login/', views.login, name='login'),    
    path('signup/', views.signup, name='signup'),
]
