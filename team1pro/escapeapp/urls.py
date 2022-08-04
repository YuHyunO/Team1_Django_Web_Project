from django.urls import path
from . import views
   
urlpatterns = [
    path('', views.index, name='index'), #메인화면
    path('theme/', views.theme, name='theme'), #
    path('cafe/', views.cafe, name='cafe'), #
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    #path('logout/', views.logout, name='logout'),
    #path('mypage/', views.mypage, name='mypage'),

    path('board_announce/', views.b_announce, name='board_announce'), #공지사항 게시판
    path('board_free/', views.b_free, name='board_free'), #자유게시판
    path('board_anonymous/', views.b_anony, name='board_anonymous'), #익명게시판
]