from django.urls import path
from MyDiary import views  # Ensure this is the correct app name and path

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('tags/', views.TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', views.TagRetrieveUpdateDestroyView.as_view(), name='tag-detail'),
    path('diary-entries/', views.DiaryEntryListCreateView.as_view(), name='diaryentry-list-create'),
    path('diary-entries/<int:pk>/', views.DiaryEntryRetrieveUpdateDestroyView.as_view(), name='diaryentry-detail'),
      path('search/', views.search_diaries, name='search_diaries'),
]
