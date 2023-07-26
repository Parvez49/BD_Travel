
from django.urls import path, include
from .views import *



app_name='Auth'



urlpatterns = [
    #path('' ,  home  , name="home"),
    path('register/' , register_attempt , name="register_attempt"),
    path('accounts/login/' , login_attempt , name="login_attempt"),
    path('activate/<uidb64>/<token>',ActivateAccountView.as_view(),name='activate'),
    path('accounts/logout/',user_logout,name="user_logout"),
    path('forgot-password/',ForgotPassword,name="forgot_password"),
    path('set-new-password/<uidb64>/<token>',SetNewPasswordView.as_view(),name='set-new-password'),


]
