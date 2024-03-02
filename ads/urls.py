from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads.views import ads, categories, users, selections

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

    path('selection/', selections.SelectionListView.as_view()),
    path('selection/<int:pk>/', selections.SelectionDetailView.as_view()),
    path('selection/create/', selections.SelectionCreateView.as_view()),
    path('selection/<int:pk>/update/', selections.SelectionUpdateView.as_view()),
    path('selection/<int:pk>/delete/', selections.SelectionDeleteView.as_view()),

    path('user/token/', TokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
]
