from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    # Personal Information
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    contact_no = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    age_range = models.CharField(max_length=20, choices=[
        ('kindergarten', 'Kindergarten (3-6 years)'),
        ('elementary', 'Elementary (6-12 years)'),
        ('high_school', 'High School (12-18 years)'),
        ('adult', 'Adult Learner (18+ years)'),
    ])
    date_of_birth = models.DateField()
    address = models.TextField()
    disability = models.CharField(max_length=50, choices=[
        ('none', 'None'),
        ('asd', 'Autism Spectrum Disorder (ASD)'),
        ('twice-exceptional', 'Twice-Exceptional Learner'),
        ('other', 'Other (Specify in Bio)'),
    ])
    bio = models.TextField(blank=True, null=True)
    account_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Userdetail(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=30, blank=True, null=True)
    bio = models.CharField(max_length=100)
    mob = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    teacher = models.BooleanField()
    city = models.CharField(max_length=30,null=True,blank=False)
    count = models.IntegerField(null=True,blank=False)
    plan = models.CharField(max_length=20,null=True,blank=False)

    def __str__(self):
        return self.email

class Contact(models.Model):
    stu = models.ForeignKey(User, related_name='stu', on_delete=models.CASCADE,blank=True, null=True)
    teacher = models.ForeignKey(User, related_name='teacher', on_delete=models.CASCADE)
    date = models.DateTimeField()
    subject = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)


