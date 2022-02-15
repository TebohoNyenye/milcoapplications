from app import views
from django.contrib.auth import views as auth_views
from django.urls import path
urlpatterns = [

path('',views.HomeView.as_view(), name="home"),
path('about/',views.AboutView.as_view(),name="about"),
path('orders/',views.orderView.as_view(),name="aorders"),
path('products/',views.ProductView,name="products"),
path('contact/',views.ContactView.as_view(),name="contact"),
path('login/',views.login_request,name="login"),
path('memberLogin/',views.memberlogin_request,name="memberLogin"),
path('customer_register/',views.customer_register.as_view(),name="customer_register"),
path('Member_register/',views.employee_register.as_view(),name="Member_register"),
path('admin-panel/',views.UploadView,name="admin-up"),
path('cart/',views.CartView,name="cart"),
path('checkout/', views.checkout, name="checkout"),
path('update_item/', views.updateItem, name="update_item"),
path('process_order/', views.processOrder, name="process_order"),
path('change_password/', views.ChangePasswordView.as_view(), name="change_password"),
path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
path('accounts/profile/', views.ProfileView, name="profile"),
path('aproducts/',views.aproductsView,name="aproductsView"),
path('delete/<int:id>/', views.delete, name='product_delete'),
path('alogin/',views.aloginView,name="alogin"),
path('memberList/',views.memberList,name="memberListview"),
path('activateuser/<int:pk>/', views.activeuser, name='activate'),
path('declineuser/<int:pk>/', views.declineuser, name='decline'),
path('export', views.export_users_csv, name='export_users_csv'),



]