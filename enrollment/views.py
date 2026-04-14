from django.shortcuts import render, redirect
from django.contrib import messages
import hashlib
from .models import StudentInfo, Users, Payment

def index(request):
    if request.method == 'POST':
        if 'showinfo' in request.POST:
            choose = request.POST.get('choose')
            roll = request.POST.get('roll')
            if choose and roll:
                student = StudentInfo.objects.filter(roll=roll, class_field=choose).first()
                if student:
                    return render(request, 'enrollment/index.html', {'found': True, 'student': student, 'form_submitted': True})
                else:
                    messages.error(request, "Your input doesn't match any records!")
            else:
                messages.error(request, "Please fill all required fields!")
        return render(request, 'enrollment/index.html', {'form_submitted': True, 'found': False})

    if 'clear' in request.GET:
        return redirect('index')

    return render(request, 'enrollment/index.html')

def sha1_md5(password):
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    return hashlib.sha1(md5_hash.encode()).hexdigest()

def admin_login(request):
    if request.session.get('admin_logged_in'):
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = Users.objects.filter(username=username).first()
        if user:
            # Check passwords against multiple hashing methods implemented in PHP legacy
            plain = password
            md5_h = hashlib.md5(password.encode()).hexdigest()
            sha1_h = hashlib.sha1(password.encode()).hexdigest()
            sha1_md5_h = sha1_md5(password)
            
            # Check if stored password matches ANY of the legacy methods
            if user.password in [plain, md5_h, sha1_h, sha1_md5_h]:
                if user.status == 'active':
                    request.session['admin_logged_in'] = True
                    request.session['admin_username'] = user.username
                    return redirect('dashboard')
                else:
                    messages.error(request, "Your status is inactive, please contact admin!")
            else:
                messages.error(request, "This password is incorrect!")
        else:
            messages.error(request, "Username Not Found!")
            
    return render(request, 'enrollment/login.html')

def admin_logout(request):
    request.session.flush()
    return redirect('index')

def dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    students_count = StudentInfo.objects.count()
    users_count = Users.objects.count()
    current_user = Users.objects.get(username=request.session['admin_username'])
    
    context = {
        'total_students': students_count,
        'total_admin': users_count,
        'user': current_user
    }
    return render(request, 'enrollment/dashboard.html', context)

from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import os

def all_students(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    class_filter = request.GET.get('class', '')
    if class_filter:
        students = StudentInfo.objects.filter(class_field=class_filter).order_by('-datetime')
    else:
        students = StudentInfo.objects.all().order_by('-datetime')
        
    context = {
        'students': students,
        'class_filter': class_filter,
        'total': students.count()
    }
    return render(request, 'enrollment/all_students.html', context)

def add_student(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == 'POST':
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        address = request.POST.get('address')
        pcontact = request.POST.get('pcontact')
        class_name = request.POST.get('class')
        photo_file = request.FILES.get('photo')

        if photo_file:
            ext = photo_file.name.split('.')[-1]
            # mimic PHP: $roll.date('Y-m-d-m-s').'.'.$photo;
            filename = f"{roll}{datetime.now().strftime('%Y-%m-%d-%m-%S')}.{ext}"
            fs = FileSystemStorage(location=os.path.join(request.site.settings.BASE_DIR if hasattr(request, 'site') else 'static', 'images'))
            fs.save(filename, photo_file)
            photo_name = filename
        else:
            photo_name = ''

        try:
            StudentInfo.objects.create(
                name=name,
                roll=roll,
                class_field=class_name,
                city=address,
                pcontact=pcontact,
                photo=photo_name,
                datetime=timezone.now()
            )
            messages.success(request, "Student Inserted!")
            return redirect('add_student')
        except Exception as e:
            print(f"DEBUG INSERT ERROR: {e}")
            messages.error(request, f"Student Not Inserted: {str(e)}")

    return render(request, 'enrollment/add_student.html')

def edit_student(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    try:
        student = StudentInfo.objects.get(id=id)
    except StudentInfo.DoesNotExist:
        return redirect('all_students')

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll = request.POST.get('roll')
        student.city = request.POST.get('address')
        student.pcontact = request.POST.get('pcontact')
        student.class_field = request.POST.get('class')
        
        photo_file = request.FILES.get('photo')
        if photo_file:
            ext = photo_file.name.split('.')[-1]
            filename = f"{student.roll}{datetime.now().strftime('%Y-%m-%d-%m-%S')}.{ext}"
            fs = FileSystemStorage() # defaults to MEDIA_ROOT
            fs.save(filename, photo_file)
            student.photo = filename

        try:
            student.save()
            messages.success(request, "Student Edited Successfully!")
            return redirect('all_students')
        except Exception as e:
            messages.error(request, "Student Not Edited!")

    return render(request, 'enrollment/edit_student.html', {'student': student})

def delete_student(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    try:
        StudentInfo.objects.get(id=id).delete()
        messages.success(request, "Student Deleted Successfully!")
    except:
        messages.error(request, "Student Not Deleted!")
    return redirect('all_students')

def all_payments(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    payments = Payment.objects.select_related('student').order_by('-payment_date')
    total = sum(p.amount for p in payments)
    
    context = {
        'payments': payments,
        'total': total
    }
    return render(request, 'enrollment/all_payments.html', context)

def add_payment(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        reference_no = request.POST.get('reference_no')
        remarks = request.POST.get('remarks')
        
        try:
            student = StudentInfo.objects.get(id=student_id)
            Payment.objects.create(
                student=student,
                amount=amount,
                payment_date=payment_date,
                payment_method=payment_method,
                reference_no=reference_no,
                remarks=remarks,
                datetime=timezone.now()
            )
            messages.success(request, "Payment recorded successfully.")
            return redirect('all_payments')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            
    students = StudentInfo.objects.all().order_by('name')
    return render(request, 'enrollment/add_payment.html', {'students': students})

def edit_payment(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    try:
        payment = Payment.objects.get(id=id)
    except Payment.DoesNotExist:
        return redirect('all_payments')
        
    if request.method == 'POST':
        payment.amount = request.POST.get('amount')
        payment.payment_date = request.POST.get('payment_date')
        payment.payment_method = request.POST.get('payment_method')
        payment.reference_no = request.POST.get('reference_no')
        payment.remarks = request.POST.get('remarks')
        
        try:
            payment.save()
            messages.success(request, "Payment Updated Successfully!")
            return redirect('all_payments')
        except Exception as e:
            messages.error(request, "Payment Not Updated!")
            
    return render(request, 'enrollment/edit_payment.html', {'payment': payment})

def delete_payment(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    try:
        Payment.objects.get(id=id).delete()
        messages.success(request, "Payment Deleted Successfully!")
    except:
        messages.error(request, "Payment Not Deleted!")
    return redirect('all_payments')

def all_admin(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    admins = Users.objects.all().order_by('-datetime')
    return render(request, 'enrollment/all_admin.html', {'admins': admins})

def admin_profile(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    admin_username = request.session.get('admin_username')
    try:
        user = Users.objects.get(username=admin_username)
    except Users.DoesNotExist:
        return redirect('admin_login')
        
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        
        photo_file = request.FILES.get('photo')
        if photo_file:
            ext = photo_file.name.split('.')[-1]
            filename = f"admin_{user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            fs = FileSystemStorage(location=os.path.join(request.site.settings.BASE_DIR if hasattr(request, 'site') else 'static', 'images'))
            fs.save(filename, photo_file)
            user.photo = filename
            
        try:
            user.save()
            messages.success(request, "Profile Updated Successfully!")
        except Exception as e:
            messages.error(request, "Profile Not Updated!")
            
    return render(request, 'enrollment/admin_profile.html', {'user': user})

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        photo = request.FILES.get('photo')
        
        if not all([name, email, username, password, c_password, photo]):
            messages.error(request, "All fields are required!")
        elif password != c_password:
            messages.error(request, "Passwords do not match!")
        elif len(username) < 8:
            messages.error(request, "Username must be at least 8 characters!")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters!")
        else:
            if Users.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif Users.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
            else:
                hashed_password = sha1_md5(password)
                ext = photo.name.split('.')[-1]
                photo_name = f"{username}.{ext}"
                
                fs = FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images'))
                fs.save(photo_name, photo)
                
                Users.objects.create(
                    name=name,
                    email=email,
                    username=username,
                    password=hashed_password,
                    photo=photo_name,
                    status='inactive',
                    datetime=timezone.now()
                )
                messages.success(request, "Your Data Inserted!")
                return redirect('register')
                
    return render(request, 'enrollment/register.html')

def edit_user(request, id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    try:
        user = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return redirect('all_admin')
        
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.status = request.POST.get('status')
        
        photo_file = request.FILES.get('photo')
        if photo_file:
            ext = photo_file.name.split('.')[-1]
            photo_name = f"{user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            fs = FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images'))
            fs.save(photo_name, photo_file)
            user.photo = photo_name
            
        user.save()
        messages.success(request, "User updated!")
        return redirect('all_admin')
        
    return render(request, 'enrollment/edit_user.html', {'user_to_edit': user})

def print_student(request, id):
    try:
        student = StudentInfo.objects.get(id=id)
    except StudentInfo.DoesNotExist:
        return redirect('index')
        
    return render(request, 'enrollment/print_student.html', {'student': student, 'now': timezone.now()})

def print_payment(request, id):
    try:
        payment = Payment.objects.get(id=id)
    except Payment.DoesNotExist:
        return redirect('all_payments')
        
    return render(request, 'enrollment/print_payment.html', {'payment': payment, 'now': timezone.now()})

def search_print(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
        
    student = None
    if request.method == 'POST':
        roll = request.POST.get('roll')
        if roll:
            student = StudentInfo.objects.filter(roll=roll).first()
            if not student:
                messages.error(request, "Student not found with roll number: " + roll)
                
    return render(request, 'enrollment/search_print.html', {'student': student})
