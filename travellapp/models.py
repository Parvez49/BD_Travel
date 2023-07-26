from django.db import models

# Create your models here.




class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    subject=models.CharField(max_length=50)
    message=models.TextField(max_length=500)
    response_status=models.BooleanField(default=False)

    """
    def __int__(self):
        return self.id
    """



class CategoriesChoice(models.TextChoices):
    choice1 = 'tra', "Travels"
    choice2 = 'org', "Organizations"
    choice3 = 't&t', "Tips & Trics"   # Modified the database value to 'tnt'
    choice4 = 'unc', "Uncategories"

class News(models.Model):
    place=models.CharField(max_length=100)
    description=models.CharField(max_length=1000)
    categories=models.CharField(max_length=5,choices=CategoriesChoice.choices)
    created_date=models.DateTimeField(auto_now=True) #  modify and save the model object, the DateTimeField will be updated to the current date and time.
    # created_date=models.DateTimeField(auto_now_add=True) # if you modify and save the model object again, this field won't be updated to the current date and time.
    picture=models.ImageField(upload_to='News/Pictures/',max_length=50)



class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='Packages/Pictures/')
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    price=models.IntegerField()

    def __str__(self):
        return self.name














