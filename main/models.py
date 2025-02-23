from django.db import models

# Create your models here.

class Waitlist(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.fullname + " | " + self.email + " | " + str(self.date_joined) + " | " + str(self.date_of_birth)