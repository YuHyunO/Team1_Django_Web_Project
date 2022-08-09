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
    path('logout/', views.logout, name='logout'),
    #path('mypage/', views.mypage, name='mypage'),
    
    path('b_notice/', views.b_notice, name='b_notice'), #공지사항 게시판
    path('b_notice/<int:no>', views.b_notice_read, name='b_notice_read'), #글읽기
    path('b_notice_write/', views.b_notice_write, name='b_notice_write'), #글쓰기
    path('b_notice_delete/<int:no>', views.b_notice_delete, name='b_notice_delete'), #글 삭제
    path('b_notice_update/<int:no>', views.b_notice_update, name='b_notice_update'), #글 수정
    path('b_notice_update_ok/<int:no>', views.b_notice_update_ok, name='b_notice_update_ok'), #글 수정 성공

    path('b_free/', views.b_free, name='b_free'), #자유게시판
    path('b_free/<int:no>', views.b_free_read, name='b_free_read'), #글읽기
    path('b_free_write/', views.b_free_write, name='b_free_write'), #글쓰기
    path('b_free_delete/<int:no>', views.b_free_delete, name='b_free_delete'), #글 삭제
    path('b_free_update/<int:no>', views.b_free_update, name='b_free_update'), #글 수정
    path('b_free_update_ok/<int:no>', views.b_free_update_ok, name='b_free_update_ok'), #글 수정 성공
    
    path('b_anony/', views.b_anony, name='b_anony'), #익명게시판
    path('b_anony/<int:no>', views.b_anony_read, name='b_anony_read'), #글읽기
    path('b_anony_write/', views.b_anony_write, name='b_anony_write'), #글쓰기
    path('b_anony/anony_delete/<int:no>', views.b_anony_delete, name='b_anony_delete'), #글 삭제
    path('b_anony/anony_update/<int:no>', views.b_anony_update, name='b_anony_update'), #글 수정
    path('b_anony/anony_update/free_update_ok/<int:no>', views.b_anony_update_ok, name='b_anony_update_ok'), #글 수정 성공
    
]
