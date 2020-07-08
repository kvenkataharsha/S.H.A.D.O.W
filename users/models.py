from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(
        max_length=50, default='Not Specified', null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Authority(models.Model):
    AUTHORITYTYPES_CHOICES = (('Department of consumer affairs','Department of consumer affairs'),('Department of food and public distribution','Department of food and public distribution'),('Serious Fraud Investigation Office','Serious Fraud Investigation Office'),('Forest Reserve Conservation Authority','Forest Reserve Conservation Authority'),('Criminal Investigation Department','Criminal Investigation Department'),('Labour Beauro','Labour Beauro'),('National Commission for Minorities','National Commission for Minorities'),('National Commission for Women','National Commission for Women'),('Incometax Department','Incometax Department'))
    


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Email_id = models.EmailField(default='shadow@gmail.com')
    Dept_id = models.CharField(max_length=50, default='123')
    Dept_name = models.CharField(max_length=50, default='Incometax Department',choices=AUTHORITYTYPES_CHOICES)
    profile_complete = models.BooleanField()
 


class Anonymous(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_complete = models.BooleanField()


class Journalist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Email_id = models.EmailField(default='shadow@gmail.com')
    Company_id = models.CharField(max_length=50, default='123')
    Company_name = models.CharField(max_length=50, default='BBC')
    profile_complete = models.BooleanField()
