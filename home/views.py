from django.shortcuts import render
# Create your views here.
def home(request):
    return render(request,'home.html')

def login_page(request):
    return render(request,'login.html')

def register_page(request):
    if request.method=="POST":
        
        pass
    return render(request,'signin.html')