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