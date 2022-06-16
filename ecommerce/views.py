from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from math import ceil

# Create your views here.
def index(request):
    # products = Product.objects.all()

    allprods = []

    # allprods = [[products,range(1,nslides),nslides],
    #             [products,range(1,nslides),nslides],
    #             [products,range(1,nslides),nslides]]
    # params = {'allprods':allprods}

    cats_dict = Product.objects.values('category','id')
    cats = {items['category'] for items in cats_dict}
    for cat in cats:
        product = Product.objects.filter(category = cat)
        n = len(product)
   # This is a formula to find the no. of slides if there are n items and each slide contains 4 items in it
        nslides = n//4 + ceil((n/4) - (n//4))
        allprods.append([product, range(1,nslides), nslides])

    params = {'allprods':allprods}
    return render(request, 'ecommerce/index.html', params)

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    product = product[0]
    print(product.images)
    return render(request, 'ecommerce/prodView.html',{'product':product})

def about(request):
    return render(request, 'ecommerce/about.html')

def contact(request):
    return render(request, 'ecommerce/contact.html')

def tracker(request):
    return render(request, 'ecommerce/tracker.html')

def search(request):
    return render(request, 'ecommerce/search.html')

def checkout(request):
    return render(request, 'ecommerce/checkout.html')