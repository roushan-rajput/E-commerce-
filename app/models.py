from django.db import models 

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    useremail = models.EmailField(unique=True)
    usercontact = models.CharField(max_length=15)
    userprofile = models.ImageField(upload_to='profile_pictures/')
    usergender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    userpassword = models.CharField(max_length=100)
    userconfirmpassword = models.CharField(max_length=100)

    def __str__(self):
        return self.username