from django.urls import path

from ads.views import index, AdListView, AdDetailedView, AdUpdateView, AdDeleteView, AdCreateView, CatListView, \
    CatDetailedView, CatCreateView, CatUpdateView, CatDeleteView, AdImageView

urlpatterns = [
    path("", index),
    path('ad/', AdListView.as_view()),
    path('ad/<int:pk>/', AdDetailedView.as_view()),
    path('ad/create/', AdCreateView.as_view()),
    path('ad/<int:pk>/update/', AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', AdImageView.as_view()),
    path('cat/', CatListView.as_view()),
    path('cat/<int:pk>/', CatDetailedView.as_view()),
    path('cat/create/', CatCreateView.as_view()),
    path('cat/<int:pk>/update/', CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CatDeleteView.as_view()),
]
