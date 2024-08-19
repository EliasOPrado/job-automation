from django.urls import path
from core.views import LinkedinJobSearchView, DjangoJobsSearchView

urlpatterns = [
    path(
        "linkedin-job-application-automation-job/",
        LinkedinJobSearchView.as_view(),
        name="linkedin-job-application",
    ),
    path(
        "django-job-application-automation-job/",
        DjangoJobsSearchView.as_view(),
        name="django-job-application",
    ),
]