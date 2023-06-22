from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect
from Food.models import *
from Customer.models import*
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from datetime import date

from django.contrib.auth import authenticate , login as auth_login , logout
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from Customer.utils import *

from math import ceil
import uuid

# Create your views here.
def home(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get('action')

        if action == 'login':
            username = data.get('userName')
            password = data.get('passWord')

            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, 'Invalid Username/Password')
            else:
                auth_login(request, user)
                return redirect('/dashboard/{}/'.format(user.id))

        elif action == 'signup':
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            copassword = data.get('copassword')

            user = User.objects.filter(username=username)

            if user.exists():
                messages.error(request, "This user already exists, try another!")
            elif len(password) < 4:
                messages.error(request, "Your password is too short!")
            elif not password == copassword:
                messages.error(request, "Passwords do not match!")
            else:
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()
                
                profile = Profile.objects.create(user= user , token = str(uuid.uuid4()))
                profile.save()
                
                messages.success(request, "Successfully registered your account!")
                # return redirect('/register/')

    return render(request, 'home.html')

def customer_dashboard(request, id):
    userData = User.objects.get(id=id)
    profile = Profile.objects.filter(user=userData)

    order_count = Order.objects.filter(user=userData).count()

    context = {'order_count': order_count}

    if request.method == 'POST':
        data = request.POST
        action = data.get('action')

        if action == 'verify':
            email = userData.email
            token = profile.first().token

            send_verification(email, token)

            context['sentCode'] = 'Successfully Sent Your Verification Code'

    name = userData.username
    email = userData.email
    verification_status = profile.first().is_verified

    recipe_data = Recipe.objects.all()
    context.update({'datas': recipe_data, 'id': id})  # Merge dictionaries using update()

    veg = recipe_data.filter(recipe_category='veg')
    nonveg = recipe_data.filter(recipe_category='nonveg')
    beverage = recipe_data.filter(recipe_category='beverage')

    # Calculate the number of slides needed
    n_nonveg = len(nonveg)
    nSlides = ceil(n_nonveg / 4)
    context.update({'no_of_slides': nSlides})

    search = request.GET.get('search')
    if search:
        veg = veg.filter(recipe_name__icontains=search)
        nonveg = nonveg.filter(recipe_name__icontains=search)
        beverage = beverage.filter(recipe_name__icontains=search)


    context.update({
        'vegData': veg,
        'nonVegData': nonveg,
        'beverageData': beverage,
        'username': name,
        'id': id,
    })

    if not veg and not nonveg and not beverage:
        context['error_message'] = 'No such item found'

    if not verification_status:
        context['verification_error'] = 'Please verify your account'

    return render(request, 'dashboard.html', context)




def customer_order(request, cid, id):
    querySet = Recipe.objects.filter(id=id).first()
    user = User.objects.get(id=cid)

    today = date.today()
    orderData = Order.objects.filter(user=user)
    
    if request.method == 'POST':
        
        data = request.POST
        
        name = data.get('item')
        itemPrice = data.get('price')
        quantity = data.get('quantity')
        order_date = today
        total_price = data.get('totalprice')
        address = data.get('address')
        
        try:
            recipe = Recipe.objects.get(recipe_name=name)
        except Recipe.DoesNotExist:
            return HttpResponse("recipe doesn't exists")
            pass
        
        if total_price == "":
            messages.error(request, 'Please provide the quantity of price that you want to order')
        else:
            # Process the address data here
            # Save the address to the database or perform any required operations
            order = Order.objects.create(
                order_item=name,
                total_price=total_price,
                order_quantity=quantity,
                order_date=order_date,
                address=address,
                user=user,
                recipe = recipe
            )
            messages.success(request, "Successfully ordered your item")
            return redirect(f'/dashboard/{cid}')
    
    search = request.GET.get('search')
    if search:
        orderData = orderData.filter(order_item__icontains=search)
    
    context = {
        'data': querySet,
        'date': today,
        'orderData': orderData,
        'cid': cid,
        'id': id
    }
    if not orderData:
        context['error_message'] = 'No ordered items found'

    return render(request, 'order.html', context)

def OrderHistory(request, cid):
    user = User.objects.get(id=cid)
    orderData = Order.objects.filter(user=user)
    
    if request.method == 'POST':
        data = request.POST
        action = data.get('action')
        
        if action == "update":
            id = data.get('id')
            item_name = data.get('item')
            quantity = data.get('quantity')
            address = data.get('address')
            
            recipe = Recipe.objects.get(recipe_name = item_name)
            item_price = recipe.recipe_price
            
            total_price = item_price * int(quantity)
            
            order = Order.objects.get(id = id)
            order.address = address
            order.order_quantity = quantity
            order.total_price = total_price
            
            order.save()
            messages.success(request, "Successfully updated you Order")
            
    search = request.GET.get('search')
    if search:
        orderData = orderData.filter(order_item__icontains=search)
    context = {'orderData': orderData, 'customerId': cid  }
    
    if not orderData:
        context['error_message'] = 'No orders found.'
    
    return render(request, 'OrderHistory.html', context)

def deleteOrder(request, id):
    previous_page = request.META.get('HTTP_REFERER')
    try:
        data = Order.objects.get(id=id)
        data.delete()
        messages.success(request, "Successfully Deleted Your Ordered Item")
        return HttpResponseRedirect(previous_page)
    except Order.DoesNotExist:
        return render(request, 'OrderHistory.html')

def updateOrder(request, cid, id):
    try:
        orderDetails = Order.objects.get(id=id)
        orderItem = orderDetails.order_item
        foodDetails = Recipe.objects.filter(recipe_name=orderItem).first()  # Retrieve the first matching Recipe object
        
        # Check if foodDetails is None (no matching recipe found)
        if foodDetails is None:
            raise Recipe.DoesNotExist

        itemPrice = foodDetails.recipe_price
        today = date.today()

        if request.method == 'POST':
            data = request.POST
            itemName = data.get('item')
            itemPrice = data.get('price')
            quantity = data.get('quantity')
            totalPrice = data.get('totalprice')

            orderDetails.order_item = itemName
            orderDetails.total_price = totalPrice
            orderDetails.order_quantity = quantity
            orderDetails.order_date = today

            orderDetails.save()
            messages.success(request, 'Successfully Updated Your Order')
            return redirect(f'/orderhistory/{cid}/')

    except Order.DoesNotExist:
        pass
    except Recipe.DoesNotExist:
        pass

    context = {'order': orderDetails, 'price': itemPrice, 'date': today}
    return render(request, 'UpdateOrder.html', context)


def sendMail(request):
    if request.method == 'POST':
        data = request.POST
        
        subject = data.get('subject')
        message = data.get('message')
        to = data.get('to')
        
        attachment = request.FILES.get('attachment')
        
    
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='romanhmgn6999@gmail.com',
            to=[to],
        )
        
        if attachment:
            attachment_name = attachment.name
            attachment_content_type = attachment.content_type
            attachment_content = attachment.read()
            email.attach(attachment_name, attachment_content, attachment_content_type)
        email.send()
        
    return render(request , 'mail.html')

def logout_account(request):
    logout(request)
    return redirect('/')

def verify(request , token):
    try:
        profile = Profile.objects.get(token = token)
        profile.is_verified = True
        profile.save()
        return HttpResponse('Congratulation! Successfully Verified Your Account !')
    except Exception as e:
        return HttpResponse("Sorry! Couldn't Verify Your Account !")