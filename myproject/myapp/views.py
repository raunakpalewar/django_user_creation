from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from datetime import datetime, timedelta
from django.utils import timezone
from .email import otp_generator,mail
from django.db.models import Q
from django.contrib import messages  # Import the messages module
from django.contrib.auth import logout

# Create your views here.

def welcome_page(request):
    request.session.flush()  # Clear all session data

    return render(request,'welcome.html')

def login_page(request):
    if request.method=='POST':
        request.session.flush()  # Clear all session data

        if 'loginbtn' in request.POST:
            username=request.POST['username']
            password=request.POST['password']
            try:
                if User.objects.filter(Q(email=username) & Q(password=password)).exists():
                    user=User.objects.get(email=username)
                    request.session['user_id'] = user.id
                    return render(request,'home.html')
                else:
                    context={
                        'error':"wrong credentials"
                    }
                    return render(request,'login.html',{'context':context})
            except:
                context={
                    'error':'user not register'
                }
                return render(request,'register.html',{'context':context})
        if 'otplogin' in request.POST:
            username=request.POST.get('username')
            otp_time=timezone.now()
            main_otp=sendmail(username)
            try:
                user=User.objects.get(email=username)
                user.otp=main_otp
                user.otp_created_at=otp_time
                user.save()
                request.session['user_id'] = user.id

                context={
                    "email":username
                }
                
                return render(request,'otplogin.html',{'user':context})
            except Exception as e:
                print(e)
                context={
                    'error':'user not register \n please register here'
                }
                return render(request,'register.html',{'context':context})

    return render(request,'login.html')

def register_page(request):
    if request.method=='POST':
        request.session.flush()  # Clear all session data

        fullname=request.POST['username']
        email=request.POST.get('emailid')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        
        if cpassword==password:
            otp_time=timezone.now()
            main_otp=sendmail(email)
            print(main_otp)
            try:
                user=User.objects.create(fullname=fullname,profile=None,email=email,phone=phone,password=password,cpassword=cpassword,is_registered=True,otp=main_otp,otp_created_at=otp_time)
                user.save()
                context={
                    'email':user.email
                }
                return render(request,'otplogin.html',{'user':context})
            except:
                user=User.objects.get(Q(email=email) & Q(is_verified=False))
                user.otp=main_otp
                user.otp_created_at=otp_time
                user.save()
                context={
                    'email':user.email
                }
                return render(request,'otplogin.html',{'user':context})
    return render(request,'register.html')
            
def sendmail(to_email):
    
    try:
        otp=mail(to_email)
        print("at send mail",to_email)
        print("otp generated ",otp)
        return otp
    except:
        print("error")
        context={'error_msg':"wrong email provided"}
        return context

def verifyotp(request):
    if request.method=='POST':
        email=request.POST['username']
        entered_otp=request.POST['otp']
        
        otp_time=timezone.now()
        
        user=User.objects.get(email=email)
        if user.otp==int(entered_otp):
            time_difference =otp_time - user.otp_created_at
            print(time_difference)
            if time_difference <= timedelta(minutes=3):
                user.is_verified=True
                user.save()
                # return HttpResponse('done')
                return render(request,'home.html')
    return render (request,'otplogin.html')

def resend(request):
    email = request.GET.get('email') # Retrieve the email frothe 
    
    print("resend email" , email)
        
    if email:
        user = User.objects.get(email=email)
        otp=sendmail(email)
        print("new", otp)
        user.otp = otp  # Update the user's OTP with the new one
        user.save()
        
        context = {
            'email': email,
            'msg': 'New OTP has been sent to:',
        }
        return render(request,'otplogin.html',{'context':context})
    return render(request,'otplogin.html')


def profile_page(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            context = {
                'fullname': user.fullname,
                'email':user.email,
                'phone':user.phone,
                'password':user.password,
                'cpassword':user.cpassword,
                'image':user.profile,
            }
            print(user)
            return render(request,'profile.html',{'context':context})
        except User.DoesNotExist:
            pass
        finally:
            if request.method=='POST':
                if 'submit' in request.POST:
                    fullname=request.POST.get('fullname')
                    email=request.POST.get('email')
                    phone=request.POST.get('phone')
                    image=request.FILES.get('image')
                    password=request.POST.get('password')
                    cpassword=request.POST.get('cpassword')
                    
                    if password==cpassword:
                        user.fullname=fullname
                        user.email=email
                        user.phone=phone
                        user.profile=image
                        user.password=password
                        user.cpassword=cpassword
                        
                        user.save()
                        context = {
                        'fullname': user.fullname,
                        'email':user.email,
                        'phone':user.phone,
                        'password':user.password,
                        'cpassword':user.cpassword,
                        'image':user.profile,}
                        return render(request,'profile.html',{'context':context})
                    return render(request,'profile.html',{'context':context})

    return render(request,'profile.html')


def logout_view(request):
    logout(request)  # Log the user out
    request.session.flush()  # Clear all session data
    
    return redirect('welcome')  # Redirect to the login page or another appropriate URL