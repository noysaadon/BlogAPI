from django.urls import path
from authenticate.views import RegisterUser

urlpatterns = [
    path('users/register/', RegisterUser.as_view(), name='register'),
]