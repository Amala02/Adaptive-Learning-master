from django.shortcuts import render, redirect
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token
from .models import *
from .forms import *
from courses.models import *
import datetime
from django.contrib.auth.decorators import login_required
from courses.models import Enroll, Course

from quizzes.models import Result

from quizzes.models import SubmitAssignment

from quizzes.models import CreateQuiz_1

UserModel = get_user_model()

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .forms import RegistrationForm, LoginForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('thanks')  # Redirect to a thanks page after registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    # Simulate Django's auth login
                    request.session['user_id'] = user.id
                    return redirect('home')  # Redirect to home page after login
                else:
                    message = "Invalid password."
            except User.DoesNotExist:
                message = "User does not exist."
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'message': message})

def thanks(request):
    return render(request, 'thanks.html')
#Logout section
def logout(request):
    auth.logout(request)
    return render(request,'login.html',{})

#for activating the inactive account.
def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return render(request,'thanks.html',{
            'message':'Your Email has been Verified!!.You may now go ahead and login.',
            'user':user.first_name
            })
    else:
        return render(request,'error.html',{
            'error_message':'Activation Link Is Invalid!!'
            })

@login_required
def coursedetail(request,course_id):
    cour = Course.objects.filter(pk=course_id).first()
    stu = Enroll.objects.filter(course=cour)
    assign = SubmitAssignment.objects.filter(course=cour)
    return render(request, 'coursedetail.html', {'course': cour, 'student': stu, 'assign': assign})

@login_required
def contactsave(request):
    if request.method == 'POST':
        stu = User.objects.filter(pk=request.POST['student']).first()
        cc = Contact()
        cc.stu = stu
        cc.teacher = request.user
        cc.date = datetime.datetime.now().date()
        cc.subject = request.POST['sub']
        cc.message = request.POST['desc']
        cc.save()
        det = Userdetail.objects.filter(name=request.user).first()
        courses = Course.objects.filter(author=request.user)
        return render(request, 'dashboard.html', {'det': det, 'course': courses})

@login_required
def contact(request,stu_id):
    student = User.objects.filter(pk=stu_id).first()
    return render(request, 'contactstu.html',{'student': student})

@login_required
def stcontact(request):
    allPost = Contact.objects.filter(stu=request.user)
    return render(request, 'stcontact.html', {'allPost': allPost})

@login_required
def dashstu(request):
    cour = Enroll.objects.filter(student=request.user)
    det = Userdetail.objects.filter(name=request.user).first()
    return render(request, 'studentdash.html',{'course': cour, 'det':det})

@login_required
def dashteach(request):
    det = Userdetail.objects.filter(name=request.user).first()
    courses = Course.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'det': det, 'course': courses})

@login_required
def quizteach(request):
    quiz =Result.objects.filter(teach=request.user)
    return render(request, 'quizteach.html', {'quiz': quiz})

@login_required
def quizstu(request):
    quiz= Result.objects.filter(student=request.user)
    return render(request, 'quizstu.html', {'quiz': quiz})


@login_required
def dashboard(request):
    ud = Userdetail.objects.filter(name=request.user).first()
    if ud.teacher == True:
        return redirect('accounts:dashteach')
    else:
        return redirect('accounts:dashstu')
@login_required
def addquestion(request):
    quiz = CreateQuiz_1.objects.filter(author=request.user)
    return render(request, 'addquestion.html', {'quiz': quiz})