from django.urls import path

from users.views import UserListView, UserDetailedView, UserUpdateView, UserDeleteView, UserCreateView

urlpatterns = [
    path('user/', UserListView.as_view()),
    path('user/<int:pk>/', UserDetailedView.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),
]