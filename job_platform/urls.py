from django.urls import path, include
from .views import (
    HomeView, 
    SignUpView, 
    SignInView, 
    JobListView,
    UserPageView,
    SignOutView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('sign-up/', SignUpView.as_view(), name='signup-page'),
    path('sign-in/', SignInView.as_view(), name='signin-page'),
    path('sign-out/', SignOutView.as_view(), name='signout'),
    path('job-applications/', JobListView.as_view(), name='job-list-page'),
    path('job-applications/<int:id>/', JobListView.as_view(), name='job-detail-page'),
    path('user-page/', UserPageView.as_view(), name='user-page'),
    path('user-page/<int:application_id>/', UserPageView.as_view(), name='user-page-form'),
]