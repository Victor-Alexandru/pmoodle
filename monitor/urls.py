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
    path('notifications/', views.NotificationList.as_view()),
    path('notifications/<int:pk>/', views.NotificationDetail.as_view()),
    path('user-groups/', views.UserGroupList.as_view()),
    path('user-groups-group/', views.UserGroupListByGroup.as_view()),
    path('user-groups/<int:pk>/', views.UserGroupDetail.as_view()),
    path('group-notifications/', views.GroupNotificationList.as_view()),
    path('user-skills/', views.UserSkillList.as_view()),
    path('user-skills/<int:pk>/', views.UserSkillDetail.as_view()),
    path('request-groups/', views.RequestToGroupList.as_view()),
    path('members/', views.MembersList.as_view()),
    path('request-groups/<int:pk>/', views.RequestToGroupDetail.as_view()),
    path('token-site-user/', views.site_user_detail),

]
