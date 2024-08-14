from django.urls import path
from core.views import JobSearchView

urlpatterns = [
    path(
        "linkedin-job-application-automation-job/",
        JobSearchView.as_view(),
        name="job-application",
    ),
]
