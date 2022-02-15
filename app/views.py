from multiprocessing import context
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
import json
import datetime
from .models import * 
from django.contrib.auth import *

from .forms import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from .forms import UpdateUserForm, UpdateProfileForm,UpdateProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from project.settings import EMAIL_HOST_USER 
#from django.contrib.auth.models import User
import csv
from django.http import HttpResponse



# Create your views here.

class HomeView(TemplateView):
    
    template_name = "index.html"
all_users = User.objects.filter(is_employee=True).values()
print(all_users)
class AboutView(TemplateView):
    template_name = "about.html"


class orderView(TemplateView):
    template_name = "orders.html"
class ContactView(TemplateView):
    template_name = "contact.html"
class aloginView(TemplateView):
    template_name = "alogin.html"
class adminView(TemplateView):
    template_name = "admin.html"


#---------------------------------------------------------------------------------------------------------------------------
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .forms import CustomerSignUpForm, EmployeeSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
       
        # else process dispatch as it otherwise normally would
        return super(customer_register, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            

        return render(request, self.template_name, {'form': form})



class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    initial = {'key': 'value'}
    template_name = 'memberRegisterbackup.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
       
        # else process dispatch as it otherwise normally would
        return super(employee_register, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            email= form.cleaned_data.get('email')
            message= 'Thank you for registering with Milco, please wait for 3 days for your account to be approved. NOTE THAT YOU WILL NOT BE ABLE TO LOGIN BEFORE BEING APPROVED. it will show account inactive while you login '
            send_mail(
                'Milco registration',
                     'Hi '+ username +',\n'+'\n' + message,
                     EMAIL_HOST_USER,
                         [email],
                         fail_silently=True,
                                )
            messages.success(request, f'Account created for {username}')
            

        return render(request, self.template_name, {'form': form})

def login_request(request):
    initial = {'key': 'value'}
    
    if request.method=='POST':
        form = LoginForm(data=request.POST,)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
           
    else:
         form = LoginForm()        
    return render(request, 'login.html',
    context={'form':form})

def memberlogin_request(request):
    if request.method=='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_employee==True :
                login(request,user)
                return redirect('/')
    else:  
        form = LoginForm()  
    return render(request, 'memberLogin.html',
context={'form':form})

def aloginView(request):
    if request.method=='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('admin-up')
    else:  
        form = LoginForm()  
    return render(request, 'alogin.html',
context={'form':form})
#----------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('/')
#-----------------------------------------------------------------------------------------------------------------------------



def ProductView(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request,'Products.html',context)  
    
   
       

def CartView(request):
   data = cartData(request)
   cartItems = data['cartItems']
   order = data['order']
   items = data['items']

   context = {'items':items, 'order':order, 'cartItems':cartItems}
   return render(request, 'cart.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer.user, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
    
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
    
	elif action == 'delete':
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)	
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
        
		order, created = Order.objects.get_or_create(customer=customer.user, complete=False)
	else:
        
		Guest.user, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()
     
	if order.shipping == True and request.user.is_authenticated:
      
      
		ShippingAddress.objects.create(
		customer=request.user.customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],

		zipcode=data['shipping']['zipcode'],
		)
         
        
	elif order.shipping == True and request.user.is_anonymous:	ShippingAddress.objects.create(
		
        guest=Guest.user, 
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
	)
    
	return JsonResponse('Payment submitted..', safe=False)
def ProfileView(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.member)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.member)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'changepassword.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')   
@staff_member_required
def UploadView(request):
    if request.method == 'POST':
      
        product_form = UpdateProductForm(request.POST,request.FILES)

        if product_form.is_valid():
            
            product_form.save()
           # messages.success(request, 'Your profile is updated successfully')
            return redirect(to='aproductsView')
    else:
            product_form = UpdateProductForm()
            
            

    return render(request, 'admin.html',{'product_form': product_form,'UpdateProductForm':UpdateProductForm})
@login_required(login_url='/admin', redirect_field_name='')
def aproductsView(request):
   
    products = Product.objects.all()
    
     
    
    context = {'products':products,}
    return render(request,'aproducts.html',context) 

def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, f'successfully deleted')
    return redirect('aproductsView')
@login_required(login_url='/alogin', redirect_field_name='')
def memberList(request):
   
    #members=Member.objects.all()
    members = Member.objects.filter(active=False).select_related().all()
    
    context = {'members':members}
    return render(request,'memberList.html',context) 

def activeuser(request, pk):
    active_user = User.objects.get(id=pk)
    member = Member.objects.get(user_id=pk)
    active_user.is_active=True
    member.active=True
    active_user.save()
    member.save()
    username = member.user.username
    email= member.user.email
    message= 'Thank you for registering with Milco, your account has been approved. NOTE THAT YOU WILL BE ABLE TO LOGIN. '
    send_mail(
                'Milco registration:APPROVAL ',
                     'Hi '+ username +',\n'+'\n' + message,
                     EMAIL_HOST_USER,
                         [email],
                         fail_silently=True,
                            )
    
    messages.success(request, f'successfully activated')
    return redirect('memberListview')

def declineuser(request, pk):
    active_user = User.objects.get(id=pk)
    member = Member.objects.get(user_id=pk)
   
    username = member.user.username 
    email= member.user.email
    message= 'Thank you for registering with Milco, your account has been approved. NOTE THAT YOU WILL BE ABLE TO LOGIN. '
    send_mail(
                'Milco registration:APPROVAL ',
                     'Hi '+ username +',\n'+'\n' + message,
                     EMAIL_HOST_USER,
                         [email],
                         fail_silently=True,
                            )
    
    messages.success(request, username + f' successfully declined')
    active_user.delete()
    member.delete()

  
    return redirect('memberListview')


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="active_members.csv"'

    writer = csv.writer(response)
    writer.writerow(['phone','passport_number', 'district', 'village', 'beneficiary','bank','acc_type','acc_number','branch','month_save','save_date' ])

    users = Member.objects.filter(active=True).select_related().all().values_list('phone','passport_number', 'district', 'village', 'beneficiary','bank','acc_type','acc_number','branch','month_save','save_date')
    for user in users:
        writer.writerow(user)

    return response
