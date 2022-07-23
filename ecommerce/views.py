from email.policy import default
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product , Contact , Order , Order_Update
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

def contact(request):
    thank = False
    if request.method == 'POST':

        name = request.POST.get('name',default='')
        email = request.POST.get('email',default='')
        phone = request.POST.get('phone',default='')
        desc = request.POST.get('desc',default='')
        contact = Contact(name=name,phone=phone,email=email,desc=desc)
        contact.save()
        thank = True

    return render(request, 'ecommerce/contact.html',{'thank':thank})

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address1',default='') + ' ' + request.POST.get('address2',default='')
        city = request.POST.get('city',default='')
        state = request.POST.get('state',default='')
        zip_code = request.POST.get('zip_code',default='')
        Json_Items = request.POST.get('Json_Items',default='')
        order = Order(name=name,phone=phone,email=email,address=address,city=city,state=state,zip_code=zip_code,Json_Items=Json_Items)
        order.save()
        thank_you = True
        id = order.order_id
        order_update = Order_Update(order_id=order.order_id,update_desc='The Order has been placed!')
        order_update.save()
        return render(request, 'ecommerce/checkout.html', {'thank':thank_you,'id':id})
    return render(request, 'ecommerce/checkout.html')


def tracker(request):
    if request.method=="POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order)>0:
                update = Order_Update.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps(updates, default=str)
                response = json.loads(response)
                responsa = {'response':response[0]['text'],'time':response[0]['time']}
                return render(request, 'ecommerce/tracker.html',responsa)
                
            else:
                response = 'Please check your order_id and email again!'
                responsa = {'response':response}
                return render(request, 'ecommerce/tracker.html',responsa)
                
        except Exception as e:
            response = 'Please check your order_id and email again!'
            responsa = {'response':response}
            return render(request, 'ecommerce/tracker.html',responsa)
    else:
        response = 'In order to check the status of your order, please fill the details and than click on track order!'        
        responsa = {'response':response}
        return render(request, 'ecommerce/tracker.html',responsa)
    return render(request, 'ecommerce/tracker.html')

def about(request):
    return render(request, 'ecommerce/about.html')


def search(request):
    return render(request, 'ecommerce/search.html')


def cart(request):
    return render(request, 'ecommerce/cart.html')