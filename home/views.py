from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'home.html')

def login_page(request):
    
    return render(request,'login.html')

def register_page(request):
    if request.method=="POST":
        first_name=request.POST.get('FirstName')
        last_name=request.POST.get('LastName')
        username_=request.POST.get('username')
        email_=request.POST.get('email')
        if(request.POST.get('password1')==request.POST.get('password2')):
            if(User.objects.filter(username=username_).exists()):
                messages.info(request,'Username exists')
                return render(request,'signin.html')
            elif(User.objects.filter(email=email_).exists()): 
                messages.info(request,'email already exists')
                return render(request,'signin.html')
            else:
                user=User.objects.create_user(username=username_,email=email_,password=request.POST.get('password1'),first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request,'User created')
                return redirect('/')
            
    return render(request,'signin.html')
