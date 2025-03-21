from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
import datetime
class CustomUser(AbstractUser):
    # Add custom fields if needed
    confirm_password  = models.CharField(max_length=15,default='Enter your password')
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('job_provider', 'Job Provider'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default="None")
    mobile_number=models.CharField(max_length=10)
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_pics/', default='ph.jpg')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills= models.CharField(max_length=255, blank=True)
    about_me= models.TextField (blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    percentage=models.FloatField(blank=True, null=True)
    passout_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Education"

class Certification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    passout_date = models.DateField(null=True, blank=True)
    certificate=models.ImageField(upload_to='certificates/',null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Certification"
class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=now)
    is_used = models.BooleanField(default=False)
    def is_valid(self):
        expiration_time = self.created_at + timedelta(minutes=5)  # OTP is valid for 5 minutes
        return now() <= expiration_time and not self.is_used

class Job(models.Model):
    job_type_choices=(('Work From Home','Work From Home'),('Work From Office','Work From Office'),('Hybrid','Hybrid'),)
    employee_type_choices=(('Fresher','Fresher'),('Experienced','Experienced'),)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    about_company=models.TextField()
    job_description = models.TextField()
    vacancy_total=models.CharField( max_length=5,blank=True,null=True)
    skills=models.TextField(blank=True,null=True)
    required_education=models.CharField(max_length=255,null=True,blank=True,default="Not Specified")
    logo=models.ImageField(upload_to='logo/', blank=True,null=True)
    location = models.CharField(max_length=255, default="Not Specified")
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    job_type=models.CharField(max_length=50,choices=job_type_choices)
    office_time_from=models.TimeField(default=datetime.datetime.now)
    office_time_to=models.TimeField(default=datetime.datetime.now)
    employee_type=models.CharField(max_length=50,choices=employee_type_choices,default="Fresher")
    is_active=models.BooleanField(default=True)
    email_address=models.EmailField(default="hr@fresher.com")
    def __str__(self):
        return self.title
class Application(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    status_choices=(('Applied','Applied'),('Shortlisted','Shortlisted'),('Selected','Selected'),('Rejected','Rejected'))
    status=models.CharField(max_length=50,choices=status_choices,default="Applied")
    resume=models.FileField(upload_to='sent_resume/')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} applied for {self.job.title}"