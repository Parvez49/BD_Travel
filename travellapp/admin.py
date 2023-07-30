from django.contrib import admin

# Register your models here.

from .models import Contact,News, Package, Booking


class ContactAttr(admin.ModelAdmin):
    list_display=['email','subject','response_status']
admin.site.register(Contact,ContactAttr)

class NewsAttr(admin.ModelAdmin):
    list_display=['id','place','categories',"created_date"]
admin.site.register(News,NewsAttr)

class PackageAttr(admin.ModelAdmin):
    list_display=['name','duration','start_location','end_location','is_active','price']
admin.site.register(Package,PackageAttr)

class BookingAttr(admin.ModelAdmin):
    list_display=['package','user','booking_date']
admin.site.register(Booking,BookingAttr)
