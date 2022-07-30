from email.policy import default
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product, Contact, Order, Order_Update
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from ecommerce.paytm import cheksum
MERCHANT_KEY = '%p5Lmt%RNoqRjcPV'


# Create your views here.
def index(request):
    # products = Product.objects.all()

    allprods = []

    # allprods = [[products,range(1,nslides),nslides],
    #             [products,range(1,nslides),nslides],
    #             [products,range(1,nslides),nslides]]
    # params = {'allprods':allprods}

    cats_dict = Product.objects.values('category', 'id')
    cats = {items['category'] for items in cats_dict}
    for cat in cats:
        product = Product.objects.filter(category=cat)
        n = len(product)
   # This is a formula to find the no. of slides if there are n items and each slide contains 4 items in it
        nslides = n//4 + ceil((n/4) - (n//4))
        allprods.append([product, range(1, nslides), nslides])

    params = {'allprods': allprods}
    return render(request, 'ecommerce/index.html', params)

def searchMatch(query,item):
    if (query in item.prod_name.lower()) or (query in item.prod_desc.lower()) or (query in item.category.lower()):
        return True
    else:
        return False

def search(request):

    query = request.GET.get('search')
    allprods = []
    cats_dict = Product.objects.values('category', 'id')
    cats = {items['category'] for items in cats_dict}

    for cat in cats:
        tempproduct = Product.objects.filter(category=cat)
        product = [item for item in tempproduct if searchMatch(query,item)]
        n = len(product)
   # This is a formula to find the no. of slides if there are n items and each slide contains 4 items in it
        nslides = n//4 + ceil((n/4) - (n//4))
        if n !=0:
            allprods.append([product, range(1, nslides), nslides])


    params = {'allprods': allprods,'msg':''}
    if len(allprods) == 0:
        params = {'allprods':allprods,'msg':'please make a relevant search!'}
    return render(request, 'ecommerce/search.html', params)


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    product = product[0]
    return render(request, 'ecommerce/prodView.html', {'product': product})


def contact(request):
    thank = False
    if request.method == 'POST':

        name = request.POST.get('name', default='')
        email = request.POST.get('email', default='')
        phone = request.POST.get('phone', default='')
        desc = request.POST.get('desc', default='')
        contact = Contact(name=name, phone=phone, email=email, desc=desc)
        contact.save()
        thank = True

    return render(request, 'ecommerce/contact.html', {'thank': thank})


def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount', '')
        address = request.POST.get(
            'address1', default='') + ' ' + request.POST.get('address2', default='')
        city = request.POST.get('city', default='')
        state = request.POST.get('state', default='')
        zip_code = request.POST.get('zip_code', default='')
        Json_Items = request.POST.get('Json_Items', default='')
        order = Order(name=name, phone=phone, email=email, address=address, city=city,
                      state=state, zip_code=zip_code, Json_Items=Json_Items, amount=amount)
        order.save()
        thank_you = True
        id = order.order_id
        order_update = Order_Update(
            order_id=order.order_id, update_desc='The Order has been placed!')
        order_update.save()

        # return render(request, 'ecommerce/checkout.html', {'thank':thank_you,'id':id})

        param_dict = {

            'MID': 'xddZHG91586529286854',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(email),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }

        param_dict['CHECKSUMHASH'] = cheksum.generate_checksum(param_dict,merchant_key=MERCHANT_KEY)
        return render(request, 'ecommerce/paytm.html', {'param_dict':param_dict})


    return render(request, 'ecommerce/checkout.html')


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = Order_Update.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps(updates, default=str)
                response = json.loads(response)
                responsa = {
                    'response': response[0]['text'], 'time': response[0]['time']}
                return render(request, 'ecommerce/tracker.html', responsa)

            else:
                response = 'Please check your order_id and email again!'
                responsa = {'response': response}
                return render(request, 'ecommerce/tracker.html', responsa)

        except Exception as e:
            response = 'Please check your order_id and email again!'
            responsa = {'response': response}
            return render(request, 'ecommerce/tracker.html', responsa)
    else:
        response = 'In order to check the status of your order, please fill the details and than click on track order!'
        responsa = {'response': response}
        return render(request, 'ecommerce/tracker.html', responsa)
    return render(request, 'ecommerce/tracker.html')


def about(request):
    return render(request, 'ecommerce/about.html')


def cart(request):
    return render(request, 'ecommerce/cart.html')


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    
    verify = cheksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        return render(request, 'ecommerce/paymentStatus.html',{'response':response_dict})
    else:
        return HttpResponse('transaction failed')
