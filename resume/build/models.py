from django.db import models
from django.contrib.auth.models import User
    
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(
        max_length=10,
        choices=[
            ('student', 'Student'),
            ('teacher', 'Teacher')
        ]
    )
    def __str__(self):
        return self.username

class Resume(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    experience = models.TextField()
    education = models.TextField()
    college = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    skills = models.TextField()
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    projects = models.TextField(null=True, blank=True)
    certifications = models.TextField(null=True, blank=True)
    theme = models.CharField(max_length=10, default='1')   
    def __str__(self):
        return self.profile.username

class ConnectionRequest(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

class ConnectionRequest(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    request_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Pending")