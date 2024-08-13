from django.db import models

class LinkedInSession(models.Model):
    email = models.EmailField()  # Store the associated email to link session cookies
    cookies = models.JSONField()  # Store cookies as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for {self.email} - Created at {self.created_at}"