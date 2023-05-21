from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from  cart.forms import CartAddProductForm
from yoga.models import kvvk, Blog
from .models import Category, Product, Rules, Images


def Show(request, category_slug = None):
    blogs = Blog.objects.all().order_by('-id')
    done = kvvk.objects.all()
    cate = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('-id')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,'shop/products/show.html',{'category':category,'products':products,'cate':cate,'done':done,'blogs':blogs})





def product_list(request):
    done = kvvk.objects.all()
    me = CartAddProductForm()

    cate = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('?')

    return render(request, 'shop/products/list.html',{'products':products,
                                                      'me':me,'cate':cate,'done':done})




def product_detail(request,id, slug):
    blogs = Blog.objects.all().order_by('-id')
    done = kvvk.objects.all()
    cart = Cart(request)
    cate = Category.objects.all()
    smiller = Product.objects.filter(list=True,available=True)
    product = get_object_or_404(Product, id = id , slug=slug, available=True)
    images = Images.objects.filter(product_id=id)
    form = CartAddProductForm()





    return render(request,'shop/products/detail.html',{'product':product,'form':form,'smiller':smiller,'cart':cart,'cate':cate,'done':done,'images':images,'blogs':blogs})







