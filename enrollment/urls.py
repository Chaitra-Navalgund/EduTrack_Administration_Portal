from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('all_students/', views.all_students, name='all_students'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('all_payments/', views.all_payments, name='all_payments'),
    path('add_payment/', views.add_payment, name='add_payment'),
    path('edit_payment/<int:id>/', views.edit_payment, name='edit_payment'),
    path('delete_payment/<int:id>/', views.delete_payment, name='delete_payment'),
    path('all_admin/', views.all_admin, name='all_admin'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('register/', views.register, name='register'),
    path('edit_user/<int:id>/', views.edit_user, name='edit_user'),
    path('print_student/<int:id>/', views.print_student, name='print_student'),
    path('print_payment/<int:id>/', views.print_payment, name='print_payment'),
]
