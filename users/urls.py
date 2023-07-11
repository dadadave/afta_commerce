from django.urls import path

from users.views import PasswordResetView, LoginView, LogoutView, CreateUserView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
