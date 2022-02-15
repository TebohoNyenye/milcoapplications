from PIL import Image
# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Member(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    passport_number = models.CharField(max_length=20,null=True, blank=True)
    district = models.CharField(max_length=20,null=True, blank=True)
    village = models.CharField(max_length=20,null=True, blank=True)
    passport = models.ImageField(default='default.jpg',upload_to='passport')
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    beneficiary= models.CharField(max_length=20,null=True, blank=True)
    bank= models.CharField(max_length=30,null=True, blank=True) #length important
    acc_type= models.CharField(max_length=30,null=True, blank=True)
    acc_number= models.CharField(max_length=20,null=True, blank=True)
    branch= models.CharField(max_length=20,null=True, blank=True)
    month_save= models.CharField(max_length=20,null=True, blank=True)
    save_date= models.CharField(max_length=20,null=True, blank=True)
    proof = models.ImageField(default='default.jpg',upload_to='bank')
    active = models.BooleanField(default=False,null=True, blank=True)
   
   
   
    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 150 or img.width > 150:
            new_img = (150, 150)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
	

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,related_name ='customer', on_delete=models.CASCADE)
    email = models.CharField(max_length=20,null=True, blank=True)
    
    

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(null=True, blank=True)
    Beneficiary_name= models.TextField(null=True, blank=True)
    holder= models.TextField(null=True, blank=True)
    AccNo= models.TextField(null=True, blank=True)
   
    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 150 or img.width > 150:
            new_img = (150, 150)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Guest(models.Model):
    name = models.OneToOneField(User,null=True,related_name ='guest', on_delete=models.CASCADE)
    email = models.CharField(max_length=200)

    
   
    def __str__(self):
        return self.email

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
