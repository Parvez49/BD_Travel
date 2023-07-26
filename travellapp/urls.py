

from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

app_name='travelapp'

urlpatterns = [
    path('',views.home,name='index_page'),

    path("news/", views.news, name="news_page"),
    path("destination/",views.destination,name="destination_page"),


    path('contact/',views.contact,name="contact_page"),
    path('about/',views.about,name="about_page"),

    path('logout/',views.user_logout,name="logout_view")

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
