from django.urls import path
from MyDiary import views

urlpatterns = [
    path('diary-entry/', views.manage_diaryentry),
    path('diary-entry/<int:pk>/', views.manage_diaryentry),

    path('user-setting/', views.manage_usersetting),
    path('user-setting/<int:pk>/', views.manage_usersetting),

    path('tags/', views.manage_tags),
    path('tags/<int:pk>/', views.manage_tags),

    path('diary-tags/', views.manage_diaryentry),
    path('diary-tags/<int:pk>/', views.manage_diaryentry),
]
