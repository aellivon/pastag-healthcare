from django.urls import path
from .views import LogInView

app_name = 'users'

urlpatterns = [
    path('login/', LogInView.as_view(), name='login')
]