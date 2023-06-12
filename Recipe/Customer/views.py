from django.shortcuts import render , redirect
from Food.models import *
from Customer.models import*
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
# Create your views here.

def customer_dashboard(request, id):
    userData = User.objects.filter(id=id)
    name = ""
    if userData.exists():
        name = userData.first().username

    querySet = Recipe.objects.all()
    context = {'datas': querySet, 'id': id}  # Include 'id' in the context
    veg = Recipe.objects.filter(recipe_category='veg')
    nonveg = Recipe.objects.filter(recipe_category='nonveg')
    beverage = Recipe.objects.filter(recipe_category='beverage')

    if request.GET.get('search'):
        veg = veg.filter(recipe_name__icontains=request.GET.get('search'))
        nonveg = nonveg.filter(recipe_name__icontains=request.GET.get('search'))
        beverage = beverage.filter(recipe_name__icontains=request.GET.get('search'))

    context = {'datas': querySet, 'vegData': veg, 'nonVegData': nonveg, 'beverageData': beverage,
               'username': name, 'id': id}
    return render(request, 'dashboard.html', context)

def customer_order(request, cid, id):
    querySet = Recipe.objects.filter(id=id).first()
    user = User.objects.get(id=cid)

    today = date.today()
    orderData = Order.objects.filter(user= user)
    
    if request.method == 'POST':
        data = request.POST
        name = data.get('item')
        itemPrice = data.get('price')
        quantity = data.get('quantity')
        order_date = today
        total_price = data.get('totalprice')
        
        order = Order.objects.create(
            order_item=name,
            total_price=total_price,
            order_quantity=quantity,
            order_date=order_date,
            user=user  # Assign the Customer instance
        )
        
        # messages.success(request, "Successfully ordered your item ")
        return redirect(f'/dashboard/{cid}')

    context = {
        'data': querySet,
        'date': today,
        'orderData':orderData,
    }
    return render(request, 'order.html', context)

def OrderHistory(request, cid):
    user = User.objects.get(id=cid)
    orderData = Order.objects.filter(user=user)
    
    search = request.GET.get('search')
    if search:
        orderData = orderData.filter(order_item__icontains=search)
    context = {'orderData': orderData, 'customerId': cid}
    
    if not orderData:
        context['error_message'] = 'No orders found.'
    
    return render(request, 'OrderHistory.html', context)


