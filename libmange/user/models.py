from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User (AbstractUser):
    phone = models.IntegerField(null = False)
    
class Author(models.Model):
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='author_profile'
    )
    # Permissions for this author
    can_create_tags = models.BooleanField(default=True, help_text="Can this author create tags?")
    can_add_books = models.BooleanField(default=True, help_text="Can this author add new books to the library?")

    # Optional: additional fields for author details
    bio = models.TextField(blank=True, null=True, help_text="Short biography of the author.")
    website = models.URLField(blank=True, null=True, help_text="Author's personal website.")

    def __str__(self):
        return f"{self.user.username} (Author Profile)"
