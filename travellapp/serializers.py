



from rest_framework import serializers
from .models import News, CategoriesChoice, Package

class NewsSerializer(serializers.ModelSerializer):
    choices = [(choice[0], choice[1]) for choice in CategoriesChoice.choices]
    categories = serializers.ChoiceField(choices=choices)

    def validate_picture(self, value):
        if not value.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError("Only JPEG and PNG images are allowed.")
        return value

    class Meta:
        model = News
        fields = ('id', 'place', 'description', 'categories', 'created_date', 'picture')


class PackageSerializer(serializers.ModelSerializer):

    def validate_cover_image(self, value):
        if not value.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError("Only JPEG and PNG images are allowed.")
        return value
    
    class Meta:
        model=Package
        fields=('name','description','duration','start_location','end_location','cover_image','start_date','price')



from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Package, Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'package', 'user', 'booking_date', 'num_of_travelers']

    def create(self, validated_data):
        package = validated_data['package']
        num_of_travelers = validated_data['num_of_travelers']

        package_price = package.price
        total_price = package_price * num_of_travelers

        validated_data['total_price'] = total_price
        booking = Booking.objects.create(**validated_data)

        return booking
    
    def update(self, instance, validated_data):
        num_of_travelers = validated_data.get('num_of_travelers', instance.num_of_travelers)
        package_price = instance.package.price
        total_price = package_price * num_of_travelers
        instance.num_of_travelers = num_of_travelers
        instance.total_price = total_price
        instance.save()
        return instance
