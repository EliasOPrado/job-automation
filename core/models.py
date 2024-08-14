from django.db import models


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

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
