from django.urls import path
from .           import views

app_name = 'user'
urlpatterns = [
    path('/signup', views.SignUpView.as_view()),
    path('/activate', views.ActivateView.as_view()),
    path('/signin', views.SignInView.as_view()),
    path('/googlesignin', views.GoogleSignInView.as_view()),
]