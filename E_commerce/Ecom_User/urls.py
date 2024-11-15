from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('changepass/', views.user_change_pass, name='changepass'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('delete_cart/<int:id>', views.delete_cart, name='delete_cart'),
    
    path('dashboard/', views.redirect_user, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('vendor_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),

    path('add_product/', views.add_product, name='add_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),

 

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='reset_pass/password_reset_form.html',success_url ='/password-reset/done/'),
         name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='reset_pass/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='reset_pass/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_pass/password_reset_complete.html'),
         name='password_reset_complete'),
]






