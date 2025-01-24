from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import (Amenities,Hotel)
# Create your views here.
def home(request):
    Amenities_obj=Amenities.objects.all()
    Hotel_obj=Hotel.objects.all()
    context={'amenities_obj': Amenities_obj,'hotel_obj':Hotel_obj}
    return render(request,'home.html',context)

def search_page(request):
    Amenities_obj=Amenities.objects.all()
    Hotel_obj=Hotel.objects.all()
    sort_by=request.GET.get("sort_by")
    if sort_by:
        if(sort_by=='price-asc'):
            Hotel_obj=Hotel_obj.order_by('hotel_price')
        elif(sort_by=='price-desc'):
            Hotel_obj=Hotel_obj.order_by('-hotel_price')
        elif(sort_by=='rating-asc'):
            Hotel_obj=Hotel_obj.order_by('hotel_rating')
        elif(sort_by=='rating-desc'):
            Hotel_obj=Hotel_obj.order_by('-hotel_rating')
    context={'amenities_obj': Amenities_obj,'hotel_obj':Hotel_obj,'sort_by':sort_by}
    return render(request,"city.html",context)

def logout_page(request):
    auth.logout(request)
    messages.info(request, "Successfully logged out")
    return redirect('/')

def login_page(request):
    if request.method=="POST":
        user_name_=request.POST.get('username')
        user_=auth.authenticate(username=user_name_,password=request.POST.get('password'))
        if(user_ is not None):
            auth.login(request,user_)
            messages.info(request,"successfully logged in")
            return redirect('/')
        else:
            messages.info(request,"Invalid Username or Password")
            return render(request,'login.html')
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
                user_=auth.authenticate(username=username_,password=request.POST.get('password2'))
                auth.login(request,user_)
                messages.info(request,'User created')
                return redirect('/')
            
    return render(request,'signin.html')
