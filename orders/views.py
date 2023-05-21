from django.shortcuts import render, redirect

from yoga.models import Blog, kvvk
from .models import OrderItem, Order, Reservation, WebhookData, UserTokenData
from .forms import OrderCreateForm
from cart.cart import Cart
import time
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from shop.models import Category, Product

# iyzico modülü -> pip install iyzipay
import iyzipay

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.db.models import Q

# Bu verileri, admin panelinden eklenebilir yapacağız

api_key = 'sandbox-etkBOaBAec7Zh6jLDL59Gng0xJV2o1tV'
secret_key = 'sandbox-uC9ysXfBn2syo7ZMOW2ywhYoc9z9hTHh'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
    }
sozlukToken = list()




@login_required(login_url="user:login")
def order_create(request):
    blogs = Blog.objects.all().order_by('-id')
    cate = Category.objects.all()
    done = kvvk.objects.all()
    cart = Cart(request)


    for c in cart:
        print(c)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        print(form)
        if form.is_valid():
            order = form.save(commit=False)
            order.author=request.user
            order.save()



            #messages.success(request, "Rezervasyonunuz Oluşturuldu, En Yakın Zaman Size Ulaşıcağız.")
            #subject = "!!!Sipariş!!!"
            #from_email = settings.EMAIL_HOST_USER
            #to_email = [from_email, "tercuman4848@gmail.com"]
            #signup_message = "!!!!Müşteri Siparişi!!!"
            #send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message,
                      #fail_silently=True)

            for item in cart:
                 newItem = OrderItem.objects.create(order=order,author=request.user,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
                 #newItem.product.stock = newItem.product.stock - item['quantity']
                 newItem.product.save()
            # clear the cart
            cart.clear()

            return redirect('/')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        'blogs':blogs,'cate':cate,'done':done})

@login_required(login_url="user:login")
def take(request):

    cart = Cart(request)
    """
    jet = Category.objects.filter(name__contains='jet')
    fly = Category.objects.filter(name__contains='fly')
    tur = Category.objects.filter(name__contains='turlar')
    adre = Category.objects.filter(name__contains='adrenalin')
    korsan = Category.objects.filter(name__contains='tekne')
    """
    #show = OrderItem.objects.filter(Q(author=request.user) and Q(paid=False)).order_by('-id')

    #a = OrderItem.objects.all()
    #total = int()
    #for i in a:
        #print(i.order)
        #print(i.price)
        #total += float(i.price)

    #print(total)


    context = {
        #"show": show,
        "cart" : cart
    }
    #'jet':jet,'fly':fly,'tur':tur,'adre':adre,'korsan':korsan, 'success': 'Ödeme Alındı'
    return render(request,"orders/order/take.html",context)


@require_http_methods(['POST'])
@csrf_exempt
def payment(request):
    cart = Cart(request)

    if 'btnSubmit' in request.POST:

        if True:
            price = request.POST.get('price')
            print('NAME', price)
            name = request.POST.get('name')
            print('NAME', name)
            lastname = request.POST.get('lastname')
            print('NAME', lastname)
            tc = request.POST.get('tc')
            print('NAME', tc)
            email = request.POST.get('email')
            print('NAME', email)
            phone = request.POST.get('phone')
            print('NAME', phone)
            city = request.POST.get('city')
            print('NAME', city)
            adres = request.POST.get('adres')
            print('NAME', adres)

            newRezervation = Reservation.objects.create(price=price, name=name, lastname=lastname, tc=tc, email=email,
                                                        phone=phone, city=city, adres=adres,
                                                        cardHolderName='K.K Kayıt Altına Alınmıyor',
                                                        cardNumber='K.K Kayıt Altına Alınmıyor',
                                                        expireMonth='K.K Kayıt Altına Alınmıyor', expireYear='expireYear',
                                                        cvc='cvc',
                                                        tokenCheck='DATA', paid=True)

            newRezervation.save()
            if request.method == 'POST':
                form = OrderCreateForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    order.author = request.user
                    order.save()

            for item in cart:
                newItem = OrderItem.objects.create(order=order, author=request.user,
                                                   product=item['product'],
                                                   price=item['price'],
                                                   quantity=item['quantity'],
                                                   )
                # newItem.product.stock = newItem.product.stock - item['quantity']
                newItem.product.save()

            cart.clear()
            return redirect('/order/success/')


    """

    payment_card = {
        'cardHolderName': str(cardHolderName),
        'cardNumber': str(cardNumber),
        'expireMonth': str(expireMonth),
        'expireYear': str(expireYear),
        'cvc': str(cvc),
        'registerCard': '0'
    }

    buyer = {
        'id': str(tc),
        'name': str(name),
        'surname': str(lastname),
        'gsmNumber': str(phone),
        'email': str(email),
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': str(adres),
        'ip': '85.34.78.112',
        'city': str(adres),
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address = {
        'contactName': str(name),
        'city': str(adres),
        'country': 'Turkey',
        'address': str(adres),
        'zipCode': '34732'
    }

    basket_items = [
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': str(price)
        },

    ]

    request = {
        'locale': 'tr',
        'conversationId': str(tc),
        'price': str(price),
        'paidPrice': str(price),
        'currency': 'TRY',
        'installment': '1',
        'basketId': 'B67832',
        'paymentChannel': 'WEB',
        'paymentGroup': 'PRODUCT',
        'paymentCard': payment_card,
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items
    }

    payment = iyzipay.Payment().create(request, options)

    check = payment.read().decode('utf-8')

    data = json.loads(check, object_pairs_hook=list)



    print('''PAYMENT''',data)




    #print('''MANİN''',data[0][1],data[18][1])



    if data[0][1] == 'success':
        newRezervation = Reservation.objects.create(price=price,name=name,lastname=lastname,tc=tc,email=email,phone=phone,city=city,adres=adres,
         cardHolderName='K.K Kayıt Altına Alınmıyor', cardNumber='K.K Kayıt Altına Alınmıyor',
                                                    expireMonth='K.K Kayıt Altına Alınmıyor', expireYear=expireYear, cvc=cvc,
                                                    tokenCheck=data[18][1],paid=True)

        newRezervation.save()

        sendOrder = Reservation.objects.filter(Q(tc=data[3][1]) and Q(tokenCheck=data[18][1]))
        mail = ''
        emaill = ''

        for i in sendOrder:
            # print(i.product.description)
            mail += str(i.name) + '\n' + str(i.adres) + '\n' + '\n'
            thanks = 'Thank You, Your Payment Done :)'
            emaill = i.email
            isim = i.name



        info = 'Your reservation is complete.'
        footer = 'Your ticket information . Before the transfer, you can reach us 24/7 from our chatbot .'
        name = isim


        email = emaill
        subject = 'Payment successful'

        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, email, 'djangomarmaris@gmail.com']
        contact_message = "WWW.TRANSFERCİDEN.COM\n Ödeme Durumu   : %s\n İnfo :  %s\n----------------------\n Name :  %s\n Note :  %s" % (
            thanks,
            info,
            name,
            footer
        )
        send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
        cart.clear()
        return redirect('/order/success/')

    else:
        newRezervation = Reservation.objects.create(price=price,name=name,lastname=lastname,tc=tc,email=email,phone=phone,city=city,adres=adres,
         cardHolderName='K.K Kayıt Altına Alınmıyor', cardNumber='K.K Kayıt Altına Alınmıyor',
                                                    expireMonth='K.K Kayıt Altına Alınmıyor', expireYear=expireYear, cvc=cvc,
                                                    tokenCheck='Ödeme Alınamacı Canım Benim',paid=False)

        newRezervation.save()


        return redirect('/order/failure/')
    """
    return HttpResponse(status=200)


@require_http_methods(['POST'])
@csrf_exempt
def result(request):

    a = Reservation.objects.filter(Q(author_id=request.user.id) and Q(paid=False))
    total = int()
    orderID = list()
    for i in a:
        orderID.append(i.tc)


    print(orderID)

    kim = UserTokenData.objects.filter(userlast= str(i.tc)).order_by('id')
    son = kim.last()
    print('SON DENEME',son.usertoken)

    context = dict()
    mesaj = request
    url = request.META.get('')
    request = {
        'locale': 'tr',
        'conversationId': str(i.tc) , #sepetClock[0] 'tu
        'token': str(son.usertoken),
        }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    #print(sozlukToken[0])   # Form oluşturulduğunda
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)


    #print(sozlukToken[0])
    print("************************")
    #print(sozlukToken)
    print("************************")
    time.sleep(3)
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        #idOrder = OrderItem.objects.filter(tokenCheck=str(sozlukToken[0])).update(paid=True)


        #iyzicoData = ReturnData.objects.create(status=sonuc[0][1],systemtime=sonuc[2][1],conversationİd=sonuc[3][1],price=sonuc[4][1],
                                               #paidPrice=sonuc[5][1],
                                               #paymentid=sonuc[7][1],
                                               #binNumber=sonuc[13][1],
                                               #result_token=sonuc[21][1],
                                               #payment_token=son.usertoken)
        #iyzicoData.save()


        #info = 'Çok Teşekkür Ederim Bizimle Beraber Olman Bizim İçin Çok Önemli Derslerde Görüşmek Üzere...'
        #name = idOrder.order.first_name
        #last = idOrder.order.last_name
        #linkNow = idOrder.product.description
        #email = idOrder.order.email
        #subject = 'Ödemeniz Alınmıştır'
        #from_email = settings.EMAIL_HOST_USER
        #to_email = [from_email, email]
        #contact_message = "WWW.ZEYNEBURAS.COM\n %s\n\İsim: %s\nSoyisim: %s\nLinkler:\n %s" % (
        #info,
        #name,
        #last,
        #linkNow,
        #)
        #send_mail(subject, contact_message, from_email, to_email,fail_silently=True)



        messages.success(mesaj,'Teşekkürler,Zoom Derslerin Email Adresine İletildi. ')
        return HttpResponseRedirect(reverse('transferciden:success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('tavport:failure'), context)

    return HttpResponse(url)



def success(request):



    return render(request, 'orders/order/ok.html')


def fail(request):
    context = dict()
    context['fail'] = 'Ödeme Alınamıştır Lütfen Tekrar Deneyiniz.'

    template = 'orders/order/fail.html'
    return render(request, template, context)





@require_POST
@csrf_exempt
def webhook(request):
    jsn = request.body
    my_json = jsn.decode('utf8').replace("'", '"')

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    print("data", data['iyziEventTime'])
    print("data", data['iyziEventType'])
    print("data", data['iyziReferenceCode'])
    print("data", data['merchantId'])
    print("data", data['paymentConversationId'])
    print("data", data['status'])
    print("data", data['token'])
    iyzicowebhook = WebhookData.objects.create(paymentConversation=data['paymentConversationId'],merchant=data['merchantId'],
                                               webhooktoken=data['token'],
                                               status=data['status'],
                                               iyziReferenceCode=data['iyziReferenceCode'],
                                               iyziEventType=data['iyziEventType'],
                                               iyziEventTime=data['iyziEventTime'])
    iyzicowebhook.save()

    if data['status'] == 'SUCCESS':

        a = Reservation.objects.filter(Q(author_id=request.user.id) and Q(paid=False))
        print(a,'gggggggggggggggg')
        orderID = list()
        for i in a:
            orderID.append(i.tc)


        kim = UserTokenData.objects.filter(usertoken=str(i.tokenCheck)).order_by('id')
        son = kim.last()
        print("sonnnnn", son)
        print('kim çalıştı', son.usertoken)

        idOrder = Reservation.objects.filter(tokenCheck=str(son.usertoken)).update(paid=True)
        print("idOrder", idOrder)
        sendOrder = Reservation.objects.filter(Q(paid=True) & Q(tokenCheck=str(son.usertoken)))
        mail = ''
        emaill =''

        for i in sendOrder:
            #print(i.product.description)
            mail += str(i.name) + '\n' + str(i.adres) + '\n' + '\n'
            thanks = 'Teşekkürler , Ödemeniz Gerçekleşti'
            emaill = i.email
            isim = i.name
            pick = i.pickup
            drop = i.dropup
            d = i.date
            p = i.person
            t = i.time
            po = i.phone

        info = 'Rezervasyonunuz Tamamlanmıştır.'
        footer = 'Bilet bilgileriniz Yukarıdaki gibidir,Transfer öncesi Tüm istek arzularınız için 05304478848 numaralı telefondan bizlere 7/24 ulaşa bilirsiz.İYİ YOLCULUKLAR'
        name = isim
        pickup = pick
        dropup = drop
        date = d
        person = p
        time = t
        telephone = po

        email = emaill
        subject = 'Ödemeniz Alınmıştır'

        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, email,'djangomarmaris@gmail.com']
        contact_message = "WWW.TRANSFERCİDEN.COM\n Ödeme Durumu   : %s\n İnfo :  %s\n----------------------\n Name :  %s\n Pickup :  %s\n Dropup :  %s\n Date :  %s\n Person :  %s\n Time :  %s\n Note :  %s" % (
            thanks,
            info,
            name,
            pickup,
            dropup,
            date,
            person,
            time,
            footer
            )
        send_mail(subject, contact_message, from_email, to_email,fail_silently=True)




    elif data['status'] == 'FAILURE':

        a = Reservation.objects.filter(Q(author_id=request.user.id) and Q(paid=False))
        print('aaaaa',a)
        orderID = list()
        for i in a:
            orderID.append(i.order)

        kim = UserTokenData.objects.filter(userlast=str(i.tokenCheck)).order_by('id')
        son = kim.last()


        sendOrder = Reservation.objects.filter(Q(paid=False) & Q(tokenCheck=str(son.usertoken)))

        emaill =''
        for i in sendOrder:
            #print(i.product.description)
            emaill = i.email

        info = 'Üzgünüm Ödemeniz Alınmadı , Tekrar Rezervasyon Yapınız.'

        email = emaill
        subject = 'Üzgünüm Ödemeniz Alınamadı'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, email]
        contact_message = " WWW.TRANSFERCİDEN.COM\nLinkler: %s" % (
            info,
            )
        send_mail(subject, contact_message, from_email, to_email,fail_silently=True)







    return HttpResponse(status=200)







