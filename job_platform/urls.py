from django.urls import path, include
from .views import HomeView, SignUpView

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('sign-up/', SignUpView.as_view(), name='signup-page'),
]