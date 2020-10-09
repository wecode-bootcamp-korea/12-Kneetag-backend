from django.urls import path
from .           import views

app_name = 'user'
urlpatterns = [
    path('/signup', views.SignUpView.as_view()),
    path('/activate', views.ActivateView.as_view()),
]