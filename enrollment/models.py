# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Payment(models.Model):
    student = models.ForeignKey('StudentInfo', models.DO_NOTHING, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'payment'


class StudentInfo(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    class_field = models.CharField(db_column='class', max_length=20)  # Field renamed because it was a Python reserved word.
    city = models.CharField(max_length=100)
    pcontact = models.CharField(max_length=30)
    photo = models.CharField(max_length=50)
    datetime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'student_info'


class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    photo = models.CharField(max_length=50)
    status = models.CharField(max_length=12)
    datetime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'users'
