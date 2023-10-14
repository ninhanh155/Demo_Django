from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .form import *
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
import random
import string

# Create your views here.
from django.views.generic import ListView

class home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by =5
    ordering = ['price']  # Mặc định sắp xếp theo giá tăng dần

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_sub=False)
        context['active_category'] = self.request.GET.get('category', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', '')  # Lấy tham số sort từ URL

        if sort == 'price_asc':
            queryset = queryset.order_by('price')  # Sắp xếp theo giá tăng dần
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')  # Sắp xếp theo giá giảm dần

        return queryset 
        
class product(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'products'
    paginate_by =20
    ordering = ['price']  # Mặc định sắp xếp theo giá tăng dần

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_sub=False)
        context['active_category'] = self.request.GET.get('category', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort', '')  # Lấy tham số sort từ URL

        if sort == 'price_asc':
            queryset = queryset.order_by('price')  # Sắp xếp theo giá tăng dần
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')  # Sắp xếp theo giá giảm dần

        return queryset 

@login_required
def cart(req):
    if req.user.is_authenticated:
        customers = req.user.customer
        order, created = Order.objects.get_or_create(customer=customers, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        cartItems = order.get_cart_items
    categories = Category.objects.filter(is_sub = False)
    active_category = req.GET.get('category', '')
        # order = {'order.get_cart_items' :0, 'order.get_cart_total': 0}
    return render(req, 'cart.html', locals())

def checkout(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        cartItems = order.get_cart_items
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'checkout.html', locals())

def checkout_sucess(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        order_code = generate_order_code()
    else:
        items = []
        cartItems = order.get_cart_items
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'checkout_sucess.html', locals())

def order(req):
    if req.user.is_authenticated:
        customer = req.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        order_code = generate_order_code()
    else:
        items = []
        cartItems = order.get_cart_items
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'order.html', locals())

def generate_order_code(length=8):
    letters_and_digits = string.ascii_uppercase + string.digits
    order_code = ''.join(random.choice(letters_and_digits) for _ in range(length))
    return order_code


def dangky(req):
    if req.method == 'POST' :
        ucf = Bieumau_dangky_thanhvien(req.POST)
        if ucf.is_valid():
            user = ucf.save()
            qldangnhap(req, user)

            return redirect('home')
    else:
        ucf = Bieumau_dangky_thanhvien()

    return render(req, 'dangky.html', {'form': ucf})
    
@method_decorator(login_required, name='dispatch')
class Taikhoan(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email' )
    template_name = 'taikhoan.html'
    success_url = reverse_lazy('taikhoan')

    def get_object(self):
        return self.request.user

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customers = request.user.customer
    product = Product.objects.get(id= productID)
    order, created = Order.objects.get_or_create(customer= customers, complete= False)
    orderitem, created = Orderitem.objects.get_or_create(order= order, product= product)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('added', safe=False)

def search(req):
    if req.method == "POST":
        searched = req.POST['searched']
        keys = Product.objects.filter(product_name__contains = searched)
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub = False)
    active_category = req.GET.get('category', '')
    return render(req, 'timkiem.html', locals())

def category(req):
    categories = Category.objects.filter(is_sub = False)
    active_category = req.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    # hiển thị số lượng sp trong cart

    
    return render (req, 'danhmuc.html' , locals())

# chi tiết sản phẩm
# def detail(req):
#     id = req.GET.get('id','')
#     product = Product.objects.filter(id=id)
#     pd = Product.objects.filter(id=id)
#     wishlist = Wishlist.objects.filter(product = pd)
#     categories = Category.objects.filter(is_sub = False)
#     active_category = req.GET.get('category', '')
#         # order = {'order.get_cart_items' :0, 'order.get_cart_total': 0}
#     return render(req, 'chitiet.html', {'product': pd, 'categories': categories, 'wishlist': wishlist })

def detail(req, product_id):
    product = Product.objects.filter(id=product_id)
    wishlist = Wishlist.objects.filter(product = product_id)
    categories = Category.objects.filter(is_sub = False)
    active_category = req.GET.get('category', '')

    return render(req, 'chitiet.html', {'product': product, 'categories': categories, 'wishlist': wishlist } )


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Xử lý dữ liệu liên hệ từ form gửi đi
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Lưu dữ liệu vào cơ sở dữ liệu hoặc thực hiện các hành động khác
            
            # Hiển thị thông báo thành công hoặc chuyển hướng đến trang khác
            return render(request, 'contact_sucess.html')
    else:
        form = ContactForm()
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    return render(request, 'contact.html', locals())

@login_required
def wishlist(req):
    user = req.user
    wishlist = user.wishlist.all()
    categories = Category.objects.filter(is_sub=False)
    active_category = req.GET.get('category', '')
    return render(req, 'wishlist.html', locals())

def plus_wishlist(req):
    if req.method == "GET":
        prod_id = req.GET['prod_id']
        product = Product.objects.get(id=prod_id)

        user = req.user
        wishlist, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            data = {
                'message': 'Product added to wishlist successfully'
            }
        else:
            data = {
                'message': 'Product already exists in wishlist'
            }
        return JsonResponse(data)

def minus_wishlist(req):
    if req.method == "GET":
        prod_id = req.GET['prod_id']
        product = Product.objects.get(id=prod_id)

        user = req.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Product removed from wishlist successfully'
        }
        return JsonResponse(data)


