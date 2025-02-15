from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db.models import Q
from .models import (Amenities,Hotel,HotelBooking)
# Create your views here.
def home(request):
    Amenities_obj=Amenities.objects.all()
    Hotel_obj=Hotel.objects.all()
    context={'amenities_obj': Amenities_obj,'hotel_obj':Hotel_obj}
    return render(request,'home.html',context)

def check_bookings(uid,start_date,end_date,room_count):
    qs= HotelBooking.objects.filter(start_date=start_date,
    end_date=end_date,
    hotel__uid=uid)
    if(len(qs)>=room_count):
        return False
    return True

def hotel_detail(request,uid):
    hotel_obj=Hotel.objects.get(uid=uid)
    if request.method=='POST':
        check_in=request.POST.get('check-in')
        check_out=request.POST.get('check-out')
        hotel=Hotel.objects.get(uid=uid)
        if not check_bookings(uid,check_in,check_out,hotel.room_count):
            messages.info(request,'Sorry Room not available')
            return render(request,'hotel_detail.html',{'hotel_obj':hotel_obj})
        HotelBooking.objects.create(hotel=hotel, user=request.user,start_date=check_in,end_date=check_out,booking_type="pre paid")
        messages.info(request,"successfully booking")
        return render(request,'hotel_detail.html',{'hotel_obj':hotel_obj})
    return render(request,'hotel_detail.html',{'hotel_obj':hotel_obj})


def search_page(request):
    Amenities_obj=Amenities.objects.all()
    Hotel_obj=Hotel.objects.all()
    sort_by=request.GET.get("sort_by")
    search_hotel=request.GET.get("Search")
    amenities_list=request.GET.getlist("amenities")
    if sort_by:
        if(sort_by=='price-asc'):
            Hotel_obj=Hotel_obj.order_by('hotel_price')
        elif(sort_by=='price-desc'):
            Hotel_obj=Hotel_obj.order_by('-hotel_price')
        elif(sort_by=='rating-asc'):
            Hotel_obj=Hotel_obj.order_by('hotel_rating')
        elif(sort_by=='rating-desc'):
            Hotel_obj=Hotel_obj.order_by('-hotel_rating')

    if(search_hotel):
        Hotel_obj=Hotel_obj.filter(Q(hotel_name__icontains=search_hotel) | Q(description__icontains=search_hotel))
    if(amenities_list!=['default']):
        for amenity in amenities_list:
            Hotel_obj = Hotel_obj.filter(amenities__amenity_name=amenity)
    
    
    context={'amenities_obj': Amenities_obj,'hotel_obj':Hotel_obj,'sort_by':sort_by,"search_bar":search_hotel,'amenities_list':amenities_list}
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
