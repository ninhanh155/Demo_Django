from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .form import Bieumau_doimatkhau

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('cart/', views.cart, name='cart'),
    path('product/', views.product.as_view(), name='product'),
    # làm tăng số lượng sp trong giỏ hàng
    path('update_item/', views.updateItem, name='update_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_sucess/', views.checkout_sucess, name='checkout_sucess'),
    path('order/', views.order, name='order'),

    path('search/', views.search, name= 'search'),
    path('category/', views.category, name= 'category'),
    path('chitiet/<int:product_id>/', views.detail, name= 'chitiet'),
#  quản trị
    path('dangky/', views.dangky, name= 'dangky'),
    path("dangxuat/", auth_views.LogoutView.as_view(), name='dangxuat'),
    path("dangnhap/", auth_views.LoginView.as_view(template_name='dangnhap.html'), name='dangnhap'),
    path('taikhoan/', views.Taikhoan.as_view(), name='taikhoan'),
    path('doimatkhau/',auth_views.PasswordChangeView.as_view(template_name='doimatkhau.html',form_class = Bieumau_doimatkhau, success_url = '/hoanthanhdoimk'), name='doimatkhau'),
    path("hoanthanhdoimk/",auth_views.PasswordResetCompleteView.as_view( template_name='hoanthanh_doimk.html'),name='password_reset_complete'), 
    # phan hoi
    path('lien-he/', views.contact, name='contact'),

    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),
    path('wishlist/', views.wishlist, name= 'yeuthich'),
    
    
]