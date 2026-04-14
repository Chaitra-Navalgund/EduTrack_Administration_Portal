from django.contrib import admin
from .models import StudentInfo, Users, Payment

@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'roll', 'class_field', 'city', 'pcontact', 'datetime')
    search_fields = ('name', 'roll', 'city')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'email', 'status', 'datetime')
    search_fields = ('username', 'name', 'email')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'payment_date', 'payment_method', 'reference_no')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('reference_no', 'remarks')
