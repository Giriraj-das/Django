from django.urls import path

from ads.views import ads, categories, users

urlpatterns = [
    path('ad/', ads.AdListView.as_view()),
    path('ad/<int:pk>/', ads.AdDetailView.as_view()),
    path('ad/create/', ads.AdCreateView.as_view()),
    path('ad/<int:pk>/update/', ads.AdUpdateView.as_view()),
    path('ad/<int:pk>/upload_image/', ads.AdUploadImageView.as_view()),
    path('ad/<int:pk>/delete/', ads.AdDeleteView.as_view()),

    path('cat/', categories.CategoryListView.as_view()),
    path('cat/<int:pk>/', categories.CategoryDetailView.as_view()),
    path('cat/create/', categories.CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', categories.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', categories.CategoryDeleteView.as_view()),

    path('user/', users.UserListView.as_view()),
    path('user/<int:pk>/', users.UserDetailView.as_view()),
    path('user/create/', users.UserCreateView.as_view()),
    path('user/<int:pk>/update/', users.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', users.UserDeleteView.as_view()),
]
