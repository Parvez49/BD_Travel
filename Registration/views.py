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















import requests

# --------------- Multiple Social Media ------------------

import requests
from django.conf import settings
from django.shortcuts import redirect

def authenticate_with_provider(request, provider):
    # Check if the provider is supported
    if provider not in settings.SOCIAL_AUTH_PROVIDERS:
        return redirect('/auth/accounts/login/')  # Redirect to home page or show an error message

    # Get the provider's configuration from settings
    provider_config = settings.SOCIAL_AUTH_PROVIDERS[provider]

    # Redirect the user to the OAuth2 consent screen of the selected provider
    base_url = provider_config['AUTHORIZATION_URL']
    params = {
        'client_id': provider_config['CLIENT_ID'],
        'redirect_uri': request.build_absolute_uri(f'/auth/{provider}/callback/'),
        'response_type': 'code',
        'scope': provider_config['SCOPE'],
    }
    auth_url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    return redirect(auth_url)

def provider_callback(request, provider):
    # Check if the provider is supported
    if provider not in settings.SOCIAL_AUTH_PROVIDERS:
        return redirect('/auth/accounts/login/')  # Redirect to home page or show an error message

    # Handle the callback from the selected provider after user consent
    code = request.GET.get('code')

    # Get the provider's configuration from settings
    provider_config = settings.SOCIAL_AUTH_PROVIDERS[provider]

    # Exchange the authorization code for an access token
    token_url = provider_config['TOKEN_URL']
    data = {
        'code': code,
        'client_id': provider_config['CLIENT_ID'],
        'client_secret': provider_config['CLIENT_SECRET'],
        'redirect_uri': request.build_absolute_uri(f'/auth/{provider}/callback/'),
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()

    # Get user information using the access token
    user_info_url = provider_config['USER_INFO_URL']
    headers = {'Authorization': f"Bearer {token_data['access_token']}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    user=User.objects.filter(email=user_info['email']).first()
    if not user:
        user=User(username=user_info['email'],email=user_info['email'])
        user.save()

    login(request,user)

    return redirect('/')  # Redirect to home page or any other desired URL




#--------------------Api------------------------------------------



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.mail import send_mail
from .serializers import UserSerializer

from jwt.exceptions import ExpiredSignatureError, DecodeError
import jwt, datetime

@csrf_exempt
@api_view(['POST'])
def api_create_profile(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        email=serializer.data['email']
        user=User.objects.get(email=email)
        #user.is_active=False
        user.save()

        # ----------JSON Web Token--------------
        payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response() 
        response.set_cookie(key='activation', value=token, httponly=True) # Set cookie
        
        # ----------Emain Send------------
        """
        email_subject="Activate your account"
        message=f"http://127.0.0.1:8000/api/reset-password/{token}"
        send_mail(email_subject,message,settings.EMAIL_HOST_USER,[email])
        response.data="Activation token has been sent in your gmail"
        """

        return response
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def api_account_verify(request,token):
    #usertkn=request.data['token']
    #print(usertkn)
 
    tkn=request.COOKIES.get('activation')
    print("tkn",tkn)
    if not tkn:
        raise AuthenticationFailed('Failed')
    
    if token==tkn:
        try:
            payload = jwt.decode(tkn, 'secret', algorithms=['HS256'])
            print(payload)
        except ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except DecodeError:
            raise AuthenticationFailed('Unauthenticated!')
    

        user=User.objects.get(id=payload['id'])
        user.is_active=True
        user.save()
        
        return Response("Your account Activated")
    else:
        raise AuthenticationFailed('Failed')

    




from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import jwt, datetime
from .serializers import UserSerializer

@api_view(['POST'])
def api_login_user(request):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed('User not found!')
    if user.is_active==False:
        raise AuthenticationFailed('Check your Gmail for gmail validation')
    if not user.is_superuser:
        raise AuthenticationFailed('Your are not admin')

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password!')     
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    #response.data=UserSerializer(user).data
    
    #response.data = {'jwt': token}
    response.data = "Logged in Successfully"

    return response

@api_view(['GET'])
def api_logout_user(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response


"""

@csrf_exempt
@api_view(['POST'])
def request_password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=serializer.validated_data['email'])
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiration after 1 hour
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        reset_link = f"http://127.0.0.1:8000/reset-password/{token}"

        # Send the reset link to the user's email
        email_subject = "Password Reset"
        message = f"Click the link below to reset your password:\n{reset_link}"
        send_mail(email_subject, message, settings.EMAIL_HOST_USER, [user.email])

        return Response("Password reset link has been sent to your email.")
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
def reset_password(request,token):
    #token = request.data.get('token')
    new_password = request.data.get('new_password')
    confirm_new_password = request.data.get('confirm_new_password')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except ExpiredSignatureError:
        return Response("Token has expired.", status=400)
    except DecodeError:
        return Response("Invalid token.", status=400)

    user = User.objects.get(id=payload['id'])

    if new_password == confirm_new_password:
        user.set_password(new_password)
        user.save()
        return Response("Password has been reset successfully.")
    else:
        return Response("New passwords do not match.", status=400)






"""




