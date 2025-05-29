from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_rented = models.BooleanField(default=False)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Tenant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    property=models.OneToOneField(Property,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.user.username

class RentPayment(models.Model):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    amount_paid=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.tenant} - {self.date}"
    
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('tenant', 'Tenant'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    

class RentalApplication(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)  # New field
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])