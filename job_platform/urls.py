from django.urls import path, include
from .views import (
    HomeView, 
    SignUpView, 
    SignInView, 
    JobListView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('sign-up/', SignUpView.as_view(), name='signup-page'),
    path('sign-in/', SignInView.as_view(), name='signin-page'),
    path('job-list/', JobListView.as_view(), name='job-list-page'),
]