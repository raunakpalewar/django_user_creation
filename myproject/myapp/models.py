from django.db import models

# Create your models here.

class User(models.Model):
    fullname=models.CharField(max_length=255)
    profile=models.ImageField(upload_to='images/' ,null=True ,blank=True)
    email=models.EmailField(max_length=254,unique=True)
    phone=models.IntegerField(unique=True)
    password=models.CharField(max_length=255)
    cpassword=models.CharField(max_length=255)
    otp=models.IntegerField(null=True,blank=True)
    is_registered=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)  # Save creation time automatically

    def __str__(self):
        return self.email
    
class products(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    price=models.IntegerField()
    category=models.CharField(max_length=255)
    images=models.ImageField(upload_to='products/')
    
    def __str__(self):
        return self.title