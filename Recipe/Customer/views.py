from django.http import HttpResponseRedirect
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
    search = request.GET.get('search')
    if search:
        veg = veg.filter(recipe_name__icontains=search)
        nonveg = nonveg.filter(recipe_name__icontains=search)
        beverage = beverage.filter(recipe_name__icontains=search)

    context = {'datas': querySet, 'vegData': veg, 'nonVegData': nonveg, 'beverageData': beverage,
               'username': name, 'id': id}
    
    if not veg and not nonveg and not beverage:
        context['error_message'] ='No items found'
        
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
        
        if total_price == "":
            messages.error(request , 'please provide the quantity of price that you want to order')
        else:    
            order = Order.objects.create(
                order_item=name,
                total_price=total_price,
                order_quantity=quantity,
                order_date=order_date,
                user=user  # Assign the Customer instance
            )
            messages.success(request, "Successfully ordered your item ")
            return redirect(f'/dashboard/{cid}')
    
    search = request.GET.get('search')
    if search:
        orderData = orderData.filter(order_item__icontains = search)
    
    context = {
        'data': querySet,
        'date': today,
        'orderData':orderData,
        'cid':cid,
        'id':id
        
    }
    if not orderData:
        context['error_message'] = 'No ordered items found '

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

def deleteOrder(request, id):
    previous_page = request.META.get('HTTP_REFERER')
    try:
        data = Order.objects.get(id=id)
        data.delete()
        messages.success(request, "Successfully Deleted Your Ordered Item")
        return HttpResponseRedirect(previous_page)
    except Order.DoesNotExist:
        return render(request, 'OrderHistory.html')

def updateOrder(request, cid ,id):
    try:
        orderDetails = Order.objects.get(id=id)
        orderItem = orderDetails.order_item
        foodDetails = Recipe.objects.get(recipe_name=orderItem)
        itemPrice = foodDetails.recipe_price
        today = date.today()
        if request.method == 'POST':
            data = request.POST
            itemName = data.get('item')
            itemPrice = data.get('price')
            quantity = data.get('quantity')
            totalPrice = data.get('totalprice')
                
            orderDetails.order_item = itemName
            orderDetails.total_price = itemPrice
            orderDetails.order_quantity = quantity
            orderDetails.order_date = today
                
            orderDetails.save()
            messages.success(request , 'Successfully Updated Your Order')
            return redirect(f'/orderhistory/{cid}/')
            
    except Order.DoesNotExist:
        pass
    except Recipe.DoesNotExist:
        pass

    context = {'order': orderDetails, 'price': itemPrice, 'date': today}
    return render(request, 'UpdateOrder.html', context)
