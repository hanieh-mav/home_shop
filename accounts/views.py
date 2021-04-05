from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate


# Create your views here.
def register(request):
    if request.method == 'POST':
        #GET FORMS VALUE
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        username = request.POST['username']
        email= request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #CHECK PASSWORD
        if password == password2:
            #CHECK USERNAME
            if User.objects.filter(username=username).exists():
                messages.error(request,'This username is taken')
                return redirect('register')
            else:
                #CHECK EMAIL 
                if User.objects.filter(email=email).exists():
                    messages.error(request,'This email is being used')
                    return redirect('register')
                else:
                    #REGISTER USER
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    user.save()
                    messages.success(request,'You are now register you can log in')
                    return redirect('login')  

        else:
            messages.error(request,'Paawords do not match')
            return redirect('register')    
    else:    
        return render(request,'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
    else:    
        return render(request,'accounts/login.html')    


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now Logout')
        return redirect('index') 



def dashboard(request):
    return render(request,'accounts/dashboard.html')         