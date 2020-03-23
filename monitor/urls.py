from django.urls import path, include
from monitor import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('skills/', views.SkillList.as_view()),
    path('skills/<int:pk>/', views.SkillDetail.as_view()),
    path('groups/', views.GroupList.as_view()),
    path('groups/<int:pk>/', views.GroupDetail.as_view()),
    path('user-messages/', views.UserMessageList.as_view()),
    path('site-users/', views.SiteUserList.as_view()),
    path('site-users/<int:pk>/', views.SiteUserDetail.as_view()),
]
