from django.db import models

class Waitlist(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)  # ✅ Make sure this is unique
    location = models.CharField(max_length=255, default="Unknown")  # ✅ Make sure this exists
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, null=True, blank=True)
    preference = models.CharField(max_length=20, null=True, blank=True)
    social_handle = models.CharField(max_length=100, null=True, blank=True)
    mbti = models.CharField(max_length=10, null=True, blank=True)
    partner_preferences = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.fullname} - {self.email}"