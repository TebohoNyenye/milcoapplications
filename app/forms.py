
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Customer,Member
#-------------------------------------------------------------------------------------------------------------------------------
class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'email',
                                                           'class': 'form-control',
                                                           }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.email =self.cleaned_data.get('email')
        customer.save()
        return user

class EmployeeSignUpForm(UserCreationForm):
    CHOICES = (('Maseru', 'Maseru'),('Butha Buthe', 'Butha Buthe'),('Leribe', 'Leribe'),('Berea', 'Berea'),('Mokhotlong', 'Mokhotlong'),('Thaba Tseka', 'Thaba Tseka'),('Mafeteng', 'Mafeteng'),('Mohales hoek', 'Mohales Hoek'),('Quthing', 'Quthing'),('Qachas Nek', 'Qachas Nek'),)
    Banks = (('Standard Lesotho Bank', 'Standard Lesotho Bank'),('Post Lesotho Bank', 'Post Lesotho Bank'),('Nedbank', 'Nedbank'),('First National Bank', 'First National Bank'),)
    AccTypes = (('Current account', 'Current account'),('Savings account', 'Savings account'),)
    Sdate = (('1ST', '1ST'),('16TH', '16TH'),)
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    branch = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Branch code',
                                                               'class': 'form-control',
                                                               }))
    month_save = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Amount you are saving',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'email',
                                                           'class': 'form-control',
                                                           }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'sername',
                                                             'class': 'form-control',
                                                             }))
    phone = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'phone number',
                                                             'class': 'form-control',
                                                             }))
    acc_number = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'account number',
                                                             'class': 'form-control',
                                                             }))
    
    passport_number = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'passport number',
                                                             'class': 'form-control',
                                                             }))
    
    village = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'village',
                                                             'class': 'form-control',
                                                             }))
    beneficiary = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'beneficiary(optional)',
                                                             'class': 'form-control',
                                                             }))
   
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    district= forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=CHOICES)
    
    bank= forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=Banks)
    
    acc_type= forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=AccTypes)
    save_date= forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=Sdate)
    passport = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    proof = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
  
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_staff = False
        user.is_active = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        employee = Member.objects.create(user=user)
        employee.phone=self.cleaned_data.get('phone')
        employee.village=self.cleaned_data.get('village')
        employee.beneficiary=self.cleaned_data.get('beneficiary')
        employee.passport_number=self.cleaned_data.get('passport_number')
        employee.district=self.cleaned_data.get('district')
        employee.passport=self.cleaned_data.get('passport')
        
         
        employee.bank=self.cleaned_data.get('bank')
        employee.acc_type=self.cleaned_data.get('acc_type')
        employee.acc_number=self.cleaned_data.get('acc_number')
        employee.branch=self.cleaned_data.get('branch')
        employee.month_save=self.cleaned_data.get('month_save')  
        employee.save_date=self.cleaned_data.get('save_date')  
        employee.proof=self.cleaned_data.get('proof')
        
        employee.save()
        return user
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)           
    
        return self.cleaned_data
#-------------------------------------------------------------------------------------------------------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']



class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email','last_name','first_name']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    beneficiary= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    phone = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    passport_number= forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    holder = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    acc_number= forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    acc_type= forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Member
        fields = ['avatar', 'bio','beneficiary','phone','passport_number','holder','acc_number','acc_type']
class UpdateProductForm(forms.ModelForm):
    CHOICES = ((0, 'No'),(1, 'yes'),('unknown', ''),)
    name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control' , 'id':'exampleInputName','placeholder':'Enter product name'}))
    price = forms.FloatField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control' , 'id':'exampleInputPrice','placeholder':'Enter product price'}))
    digital= forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=CHOICES)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Product
        fields = ['name','price','digital','image']