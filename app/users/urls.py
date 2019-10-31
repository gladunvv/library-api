from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserAuthToken, UserLogIn, UserDelete


app_name = 'users'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserAuthToken.as_view(), name='create_user'),
    path('login/', UserLogIn.as_view(), name='login'),
    path('delete', UserDelete.as_view(), name='delete'),
]
