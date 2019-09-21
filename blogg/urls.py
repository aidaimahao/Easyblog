from django.urls import path, include,re_path
from blogg import views

urlpatterns = [
    path('login/', views.login),
    path('index/', views.index),
    path('get_valid_img/', views.get_valid_img),
    path('get_geetest/', views.get_geetest),
    path('register/',views.register),
    path('index/',views.index),
    path('logout/',views.logout),
    path('up_down/',views.up_down),
    path('comment/',views.comment),
    re_path(r'comment_tree/(\d+)/',views.comment_tree),
    path('backend/addarticle/',views.add_article),

    re_path(r'(\w+)/articleDtl/(\d+)',views.articleDtl),
    path('',views.index),

    re_path(r'home/(?P<username>\w+)/',views.selfhome)
]
