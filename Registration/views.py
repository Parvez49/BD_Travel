from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request , 'home.html')


from django.contrib.auth.models import User
from django.contrib import messages
import uuid
# from .models import Profile
from .email_server import validate_email
from django.template.loader import render_to_string
from .utils import generate_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail


def register_attempt(request):
    data={"email":"",
          "password":"",
          "conpassword":""}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        conpassword=request.POST.get('conpassword')

        try:
            data["email"]=email
            data["password"]=password
            data['conpassword']=conpassword

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is already registered.')
                #return redirect('/register')
                return render(request , 'register.html',{"data":data})
            if password!=conpassword:
                messages.warning(request,'Password are not matching')
                return render(request,'register.html',{"data":data})
            
            # ------Gmail validation cheking-----------
            """
            if not validate_email(email):
                messages.warning(request, 'Invalid or Inactive email!')
                #return redirect('/register')
                return render(request , 'register.html',{"data":data})
            """

            user=User.objects.create_user(username=email,email=email,password=password)
            user.is_active=False
            user.save()
            #profile_obj=Profile.objects.create(user=user)
            #profile_obj.save()

            email_subject="Activate your account"
            message=render_to_string('activate_mail.html',{
            'user':user,
            'domain':'127.0.0.1:8090',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
            })
            send_mail(email_subject,message,settings.EMAIL_HOST_USER,[email])
            messages.success(request,f"Activation link has been sent in your gmail")
            return render(request , 'register.html',{"data":data})

        except Exception as e:
            print(e)

    return render(request , 'register.html',{"data":data})


from django.views.generic import View
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifer:
            user=None
        
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activates Successfully")
            return redirect('/auth/accounts/login')
        else:
            messages.error("Error!")
            return render(request,'register.html')
    


from django.contrib.auth import authenticate,login
def login_attempt(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email,password)
        user_obj = User.objects.filter(username = email).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/auth/accounts/login')
        
        user = authenticate(email=email , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/auth/accounts/login')
        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')



    

def token_send(request):
    return render(request , 'token_send.html')

"""
def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/auth/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/auth/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
"""

from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return redirect("/")


from django.contrib.auth.tokens import PasswordResetTokenGenerator
def ForgotPassword(request):

    data={'email': ""}
    if request.method=='POST':
        email=request.POST['email']
        data['email']=email
        try:
            user=User.objects.filter(email=email)
            if user.exists():
                email_subject='Reset Your Password'
                message=render_to_string('reset_password_mail.html',{
                    'domain':'127.0.0.1:8000',
                    'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token':PasswordResetTokenGenerator().make_token(user[0])
                })

            send_mail(email_subject,message,settings.EMAIL_HOST_USER,[email])
            messages.info(request,f"WE HAVE SENT YOU AN EMAIL TO RESET THE PASSWORD." )
            return render(request,'forgot.html')
        except Exception as e:
            print(e)

    return render(request,"forgot.html",{"data":data})


from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64, 
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'forgot.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'reset_password.html',context)
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['password1']
        confirm_password=request.POST['password2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'reset_password.html',context)
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Successful")
            return redirect('/accounts/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'forgot.html')

        #return render(request,'reset_password.html',context)





