from django.urls import path
from .views import SignUpView, ProfileView, PasswordChangeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
]
