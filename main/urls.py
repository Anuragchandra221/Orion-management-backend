from django.urls import path, include
from rest_framework_simplejwt.views import (

    TokenRefreshView,
)
from .views import MyTokenObtainPairView
from . import views

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-count/', views.get_count),
    path('create-coordinator/', views.create_coordinator),
    path('create-guide/', views.create_guide),
    path('get-coordinator/', views.getCoordinator),
    path('get-guide/', views.getGuide),
    path('reset-password-confirm/', views.reset_password_confirm),
    path('reset-password/', views.reset_password),
] 