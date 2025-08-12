from django.db import models

# Create your models here.
class Patient(models.Model):
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()

    def __str__(self):
        return self.firstname + " " + self.surname

class Doctor(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    speciality = models.CharField(max_length=100)
    maritalstatus = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    birthdate = models.DateField()
    appointmenttime = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return self.fullname

class Ward(models.Model):
    wardname = models.CharField(max_length=100)
    capacity = models.IntegerField()
    department = models.CharField(max_length=100)
    description = models.TextField()
    staff = models.IntegerField()
    visitinghours = models.TimeField()
    rules = models.TextField()

    def __str__(self):
        return self.wardname

class Appoint(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    date = models.DateTimeField()
    department = models.CharField(max_length=100)
    doctor = models.CharField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"
