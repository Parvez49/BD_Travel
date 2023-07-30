from django.shortcuts import render

# Create your views here.

from django.core.cache import cache
from .models import Package
def home(request):
    packages=cache.get('packages')
    if packages is None:
        packages=Package.objects.all()[:5]

    
    if request.method=='POST':
        fromplace=request.POST.get('from')
        to=request.POST.get('to')
        jdate=request.POST.get('date')
        budget=request.POST.get('budget')

        search_packages = Package.objects.filter(start_location__iexact=fromplace, end_location__iexact=to,start_date=jdate,is_active=True) # __iexact: case-insensitive query

        return render(request, 'app/index.html',{"packages":packages,"search_packages":search_packages})
    

    return render(request, 'app/index.html',{"packages":packages})


from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    packages=Package.objects.all()[:5]
    return render(request,'app/index.html',{"packages":packages})



def about(request):
    return render(request,'app/about.html')



from .models import Contact
from django.contrib import messages

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        myquery=Contact(name=name,email=email,subject=subject,message=message)
        # myquery.save()
        print(myquery.name,myquery.response_status)
        messages.info(request,"we will get back to you soon..")
        return render(request,"app/contact.html")

    return render(request,"app/contact.html")


# --------------------- News view ---------------------------------

# helper function for news caching
from django.core.cache import cache
def get_news(page_number):
    paginator = cache.get('paginator')
    if paginator is None:
        place_news = News.objects.filter(categories='tra').order_by('-created_date')
        per_page = 2
        paginator = Paginator(place_news, per_page)
        cache.set('paginator', paginator, timeout=3600)  # Cache for 1 hour

    try:
        place_obj = paginator.get_page(page_number)
    except Exception:
        place_obj = paginator.get_page(1)
    num_pages_range = range(1, paginator.num_pages + 1)
    return (place_obj,num_pages_range)


from django.db.models import Count
from .models import News, CategoriesChoice
from django.core.paginator import Paginator


def news(request):
    category_counts = News.objects.values('categories').annotate(count=Count('id'))
    category_data=list()
    for category_count in category_counts:
        category_name = dict(CategoriesChoice.choices).get(category_count['categories'])
        print(f"{category_name}: {category_count['count']} news")
        category_data.append((category_name,category_count['count']))

    latest_news = News.objects.order_by('-created_date')[:3]
    # ---------------

    page_number = request.GET.get('page',1)
    place_obj,num_pages_range=get_news(page_number)

    return render(request,'app/news.html',{"category_data":category_data,"place_news":place_obj,"num_pages_range":num_pages_range,"latest_news":latest_news})

# ------------------- Destinations --------------------------

def destination(request):

    packages=Package.objects.all()[:5]

    return render(request,'app/destinations.html',{"packages":packages})



from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .serializers import BookingSerializer
from .models import Booking

@login_required(login_url='/auth/accounts/login/')
def booking(request,package):

    package=Package.objects.get(package_id=package)
    if request.method=="POST":
        user = request.user
        existing_booking=Booking.objects.filter(user=user,package=package).first()
        
        num_of_travelers=int(request.POST.get('num_of_travelers',0))
        if existing_booking:
            existing_booking.num_of_travelers = num_of_travelers
            existing_booking.total_price = package.price * num_of_travelers
            existing_booking.save()
        else:
            new_booking = Booking.objects.create(
                package=package,
                user=user,
                booking_date=package.start_date,
                num_of_travelers=num_of_travelers,
                total_price=package.price * num_of_travelers
            )
            print(new_booking.package.price)
            new_booking.save()

        messages.success(request,"Your booking added")

        """
        # ------------- Using Serializer -------------------------
        booking_data = {
                'package': package.pk,
                'user': user.pk,
                'booking_date': package.start_date,
                'num_of_travelers': request.POST.get('num_of_travelers'),  # You can change this to the actual number of travelers
            }
        if existing_booking: # update code
            bookingobj=BookingSerializer(existing_booking,data=booking_data,partial=True)
            if bookingobj.is_valid():
                bookingobj.save()
                print(bookingobj['package'].name)
            else:
                print("Error")
                print(bookingobj.errors)
            
        else:
            bookingobj=BookingSerializer(data=booking_data)
            if bookingobj.is_valid():
                bookingobj.save()
            else:
                print("ERROR")
        """

    return render(request,'app/Booking_form.html',{'package':package})



















# ------------------Api---------------------------------
# ------------------------------------------------------

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed

import jwt, datetime
from jwt.exceptions import ExpiredSignatureError, DecodeError

from .serializers import NewsSerializer, PackageSerializer

@api_view(['POST'])
def api_post_News(request):
    token=request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("Authentication Failed")

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    except DecodeError:
        raise AuthenticationFailed('Unauthenticated!')
    
    newsobj=NewsSerializer(data=request.data)
    if newsobj.is_valid():
        newsobj.save()
        return Response(" News saved ")
    return Response(" ERROR ")

@api_view(['POST'])
def api_post_Package(request):
    token=request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("Authentication Failed")
    try:
        payload=jwt.decode(token,'secret',algorithms=['HS256'])
    except ExpiredSignatureError:
        raise AuthenticationFailed("Authentication Failed")
    except DecodeError:
        raise AuthenticationFailed("Authentication Failed")
    
    packageobj=PackageSerializer(data=request.data)
    if packageobj.is_valid():
        packageobj.save()
        return Response(" Package Saved ")
    return Response(" ERROR ")



    
