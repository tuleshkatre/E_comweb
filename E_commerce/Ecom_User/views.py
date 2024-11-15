from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import SignupForm, ProductForm, AddressForm, UserUpdateForm
from .models import Product, Order, Cart, CartItem, OrderItem, Profile
from datetime import timezone
from .models import User


#Login section


def home(request):
    return render(request, 'home.html')


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = SignupForm(request.POST)
            if fm.is_valid():
                user = fm.save()
                user.save()
                role = fm.cleaned_data['role']
                Profile.objects.create(user=user, role=role)
                
                return redirect('/login/')
        else:
            fm = SignupForm()
        return render(request, 'signup.html', {'form': fm})
    else:
        return redirect('/login/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return redirect_user(user)
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form': fm})
    else:
        return redirect_user(request.user)
    

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == "POST":
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                return redirect_user(user)
        else:
            user_form = UserUpdateForm(instance=user)
        
        return render(request, 'user_update.html', {'user_form': user_form,})
    else:
        return redirect('/login/')


def user_logout(request):
    logout(request)
    return redirect('/login/')


def user_change_pass(request, user_id):
    user_id = request.user.id
    if request.user.is_authenticated and request.user.id == user_id:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                return redirect_user(user=request.user)
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'changepass.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')

#### ______________________________________________________________________________________####
def redirect_user(user):
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.profile.role == 'Vendor':
        return redirect('vendor_dashboard')
    elif user.profile.role == 'Customer':
        return redirect('customer_dashboard')
    else:
        return redirect('/dashboard/')

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all()
        orders = Order.objects.all()
        vendors = Profile.objects.filter(role = 'Vendor')
        customers = Profile.objects.filter(role = 'Customer')

        context = {'name': request.user.username,'products': products,'orders': orders,'vendors': vendors,'customers': customers}
        return render(request, 'admin_dashboard.html', context)
    else:
        return HttpResponseRedirect('/login/')

def customer_dashboard(request):
    if request.user.is_authenticated and request.user.profile.role == 'Customer' :
        cart = Cart.objects.filter(customer=request.user).first()
        orders = Order.objects.filter(customer=request.user)
        products = Product.objects.all() 

        return render(request, 'customer_dashboard.html', {'name': request.user.username,'cart': cart,'orders': orders,'products': products})
    return redirect('login')

def vendor_dashboard(request):
    if request.user.is_authenticated and request.user.profile.role == 'Vendor':
        products = Product.objects.filter(vendor=request.user)

        return render(request, 'vendor_dashboard.html', {
            'name': request.user.username,
            'products': products
        })
    return redirect('login')

#### ______________________________________________________________________________________####

def add_product(request):
    if request.user.is_authenticated and request.user.profile.role == 'Vendor':
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)  
            if form.is_valid():
                product = form.save(commit=False)
                product.vendor = request.user
                product.save()
                return redirect('vendor_dashboard')
        else:
            form = ProductForm()

        return render(request, 'add_product.html', {'form': form})
    else:
        return redirect('login')
    

def delete_product(request, id):
    if request.user.is_authenticated and request.user.profile.role == 'Vendor':
        del_pro = Product.objects.get(id = id)
        del_pro.delete()
        return redirect('vendor_dashboard')
    

def add_to_cart(request, product_id):
    if request.user.is_authenticated and request.user.profile.role == 'Customer':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(customer=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('customer_dashboard')
    else:
        return redirect('login')
    

def view_cart(request):
    if request.user.is_authenticated and  request.user.profile.role == 'Customer':
        cart = Cart.objects.filter(customer=request.user).first()
        cart_items = CartItem.objects.filter(cart=cart)

        return render(request, 'view_cart.html', {'cart_items': cart_items, 'cart': cart})
    else:
        return redirect('login')
    

def delete_cart(request, id):
    
    if request.user.is_authenticated and  request.user.profile.role == 'Customer':
        del_cart = CartItem.objects.get(id = id)
        if del_cart.quantity > 1:
            del_cart.quantity -= 1
            del_cart.save()
        else:
           del_cart.delete()
    return redirect('view_cart')


def checkout(request):
    if request.user.is_authenticated and  request.user.profile.role == 'Customer':
        cart = Cart.objects.filter(customer=request.user).first()
        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            item.total_price = item.product.price * item.quantity
        total_amount = sum(item.total_price for item in cart_items)

        if request.method == "POST":
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.customer = request.user
                address.save()
                order = Order.objects.create(customer=request.user,order_date=timezone.now(),status="Pending",total_amount=total_amount)
                for item in cart_items:
                    OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.p)
                cart_items.delete()
                return redirect('customer_dashboard')
        else:
            address_form = AddressForm()

        return render(request, 'checkout.html', {'cart_items': cart_items,'cart': cart,'total_amount': total_amount,'address_form': address_form})
    else:
        return redirect('login')






