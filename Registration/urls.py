
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

    # ---- Social Accounts --------------
    path('<str:provider>/', authenticate_with_provider, name='authenticate_with_provider'),
    path('<str:provider>/callback/', provider_callback, name='provider_callback'),

    # -------- API --------------------

    
    path('api/register/',api_create_profile,name="create_admin"),
    path('api/verify/<str:token>/',api_account_verify),
    path('api/login/',api_login_user),
    path('api/logout/', api_logout_user, name="lgout"),


    #path('api/request-password-reset/', views.request_password_reset, name='request-password-reset'),

    #path('api/reset-password/<str:token>/', views.reset_password, name='reset-password'),

    
    
]
