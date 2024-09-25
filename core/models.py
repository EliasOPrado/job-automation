from django.db import models
from django.contrib.auth.models import User


class LinkedInSession(models.Model):
    email = models.EmailField()  # Store the associated email to link session cookies
    cookies = models.JSONField()  # Store cookies as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for {self.email} - Created at {self.created_at}"


class JobApplication(models.Model):
    url = models.URLField(max_length=500, unique=True)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_description = models.TextField()
    location = models.CharField(max_length=255, default="Remote")
    company_email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_applied = models.ForeignKey(JobApplication, on_delete=models.DO_NOTHING)
    date_applied = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set the date when the application is created
    status = models.CharField(
        max_length=50,
        choices=[
            ("applied", "Applied"),
            ("interview", "Interview"),
            ("offer", "Offer"),
            ("rejected", "Rejected"),
            ("withdrawn", "Withdrawn"),
        ],
        default="applied",
    )

    def __str__(self):
        return f"{self.user.username} applied for {self.job_applied.job_title} on {self.date_applied.strftime('%Y-%m-%d')}"
