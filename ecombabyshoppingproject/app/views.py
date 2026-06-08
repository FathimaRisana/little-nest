from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Q
import random
from django.core.mail import send_mail
import razorpay
from .models import Product, Category, CartItem

# Create your views here.
def index(request):
    query = request.GET.get('q')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    categories = Category.objects.all()

    context = {
        'products': products[:8],  # featured
        'categories': categories
    }
    return render(request, 'index.html', context)


def product(request):
    category_slug = request.GET.get('category')
    query = request.GET.get('q')

    products = Product.objects.all()

    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'product.html', {
        'products': products
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'product_detail.html', {
        'product': product
    })


# razorpay

client=razorpay.Client(
auth=("YOUR_KEY","YOUR_SECRET")
)

def create_payment(request):

    payment=client.order.create({
    "amount":50000,
    "currency":"INR"
    })

    return JsonResponse(payment)


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('login')
    return render(request, 'login_new.html')


def register(request):

    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # validation
        if not name or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('register')

        if "@" not in email:
            messages.error(request, "Enter valid email")
            return redirect('register')

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # create user
        user = User.objects.create_user(
            username=name,
            email=email,
            password=password
        )

        # login automatically
        login(request, user)

        # return to clicked page
        if next_url:
            return redirect(next_url)

        return redirect('home')

    return render(
        request,
        'register_new.html',
        {'next': next_url}
    )

def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = str(random.randint(100000, 200000))
        request.session['otp'] = otp
        request.session['email'] = email
        send_mail(
            "your otp code",
            f"your otp is:{otp}",
            'djangopython305@gmail.com',
            [email],
        )
        return redirect("ver_otp")
    return render(request, 'send_otp.html')

def ver_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("otp")
        if entered_otp == saved_otp:
            return redirect("/")
        else:
            return render(request, "ver_otp.html")
    return render(request, 'ver_otp.html')




def product_list(request):

    category = request.GET.get('category')
    query = request.GET.get('q')
    price = request.GET.get('price')

    products = Product.objects.all()

    # Search
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Category filter
    if category and category != "all":
        products = products.filter(category__slug=category)

    # Price filter
    if price:
        price = int(price)

        if price == 500:
            products = products.filter(price__lt=500)

        elif price == 1000:
            products = products.filter(price__gte=500, price__lte=1000)

        elif price == 5000:
            products = products.filter(price__gt=1000)

    return render(request, 'product.html', {
        'products': products
    })




@login_required(login_url='register')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return redirect('view_cart')


@login_required(login_url='register')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total_price = sum(item.get_total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })



def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )
    cart_item.delete()
    return redirect('view_cart')


def logout_view(request):
    auth.logout(request)
    return redirect('login')


