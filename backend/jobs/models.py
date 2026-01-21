from django.db import models

class Job(models.Model):
    status = models.JSONField()
    category = models.JSONField()
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to="jobs/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
