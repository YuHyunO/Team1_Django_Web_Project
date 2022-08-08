from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),   
    path('cafe/', views.cafe, name='cafe'),   
    path('theme/', views.theme, name='theme'),   
    path('theme/theme_detail/', views.theme_detail, name='theme_detail'),  
    path('cafe/cafe_detail/', views.cafe_detail, name='cafe_detail'),  
    path('login/', views.login, name='login'),    
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    #path('logout/', views.logout, name='logout'),
    #path('mypage/', views.mypage, name='mypage'),
    path('b_announce/', views.b_announce, name='b_announce'), #공지사항 게시판
    path('b_announce/b_announce_read/<int:id>', views.b_announce_read, name='b_announce_read'), #글읽기
    path('b_announce_write/', views.b_announce_write, name='b_announce_write'), #글쓰기
    path('b_announce_write/announce_write_ok/', views.b_announce_write_ok, name='b_announce_write_ok'), #글쓰기 성공
    path('b_announce/announce_delete/<int:id>', views.b_announce_delete, name='b_announce_delete'), #글 삭제
    path('b_announce/announce_update/<int:id>', views.b_announce_update, name='b_announce_update'), #글 수정
    path('b_announce/announce_update/announce_update_ok/<int:id>', views.b_announce_update_ok, name='b_announce_update_ok'), #글 수정 성공


    path('b_free/', views.b_free, name='b_free'), #자유게시판
    path('b_free/<int:id>', views.b_free_read, name='b_free_read'), #글읽기
    path('b_free_write/', views.b_free_write, name='b_free_write'), #글쓰기
    path('b_free_write/free_write_ok/', views.b_free_write_ok, name='b_free_write_ok'), #글쓰기 성공
    path('b_free/free_delete/<int:id>', views.b_free_delete, name='b_free_delete'), #글 삭제
    path('b_free/free_update/<int:id>', views.b_free_update, name='b_free_update'), #글 수정
    path('b_free/free_update/free_update_ok/<int:id>', views.b_free_update_ok, name='b_free_update_ok'), #글 수정 성공
    
    path('b_anony/', views.b_anony, name='b_anonymous'), #익명게시판
    path('b_anony/<int:id>', views.b_anony_read, name='b_anony_read'), #글읽기
    path('b_anony_write/', views.b_anony_write, name='b_anony_write'), #글쓰기
    path('b_anony_write/anony_write_ok/', views.b_anony_write_ok, name='b_anony_write_ok'), #글쓰기 성공
    path('b_anony/anony_delete/<int:id>', views.b_anony_delete, name='b_anony_delete'), #글 삭제
    path('b_anony/anony_update/<int:id>', views.b_anony_update, name='b_anony_update'), #글 수정
    path('b_anony/anony_update/free_update_ok/<int:id>', views.b_anony_update_ok, name='b_anony_update_ok'), #글 수정 성공
    
]
