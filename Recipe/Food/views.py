from django.shortcuts import render, redirect , HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from . models import *
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login as auth_login , logout
from django.contrib.auth.decorators import login_required
from Food.utils import *
from Customer.models import *
from django.conf import settings
# Create your views here.

# @login_required(login_url = '/login/')
def recipe(request):
    if request.method == 'POST':
        
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_price = data.get('recipe_price')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        recipe_category = data.get('category')
        
        if recipe_name == "" and recipe_description == "" and recipe_price == "":
            return render(request, 'recipe.html', {'error': True , 'message': 'Please provide all the details in the field!'})
        elif not recipe_image:
            return render(request, 'recipe.html', {'error': True , 'message': 'Please provide recipe image!'})
        else:  
            Recipe.objects.create(
                recipe_name=recipe_name,
                recipe_description=recipe_description,
                recipe_image=recipe_image,
                recipe_price=recipe_price,
                recipe_category = recipe_category
            )
            messages.success(request, 'Successfully Added Recipe')
        return redirect('/recipe/')
    
    querySet = Recipe.objects.all()
    vegSet = Recipe.objects.filter(recipe_category = "veg")
    nonVegSet = Recipe.objects.filter(recipe_category = "nonveg")
    beverageSet = Recipe.objects.filter(recipe_category = "beverage")
    
    if request.GET.get('search'):
        querySet = querySet.filter(recipe_name__icontains = request.GET.get('search'))
        vegSet = vegSet.filter(recipe_name__icontains = request.GET.get('search'))
        nonVegSet = nonVegSet.filter(recipe_name__icontains = request.GET.get('search'))
        beverageSet = beverageSet.filter(recipe_name__icontains = request.GET.get('search'))
        
    context = {'data': querySet, 'veg':vegSet, 'nonVeg':nonVegSet, 'beverage':beverageSet}
    return render(request, 'recipe.html', context)

@login_required(login_url='/login/')
def deleteRecipe(request, id):
    data = Recipe.objects.get(id = id)
    data.delete()
    return redirect('/recipe/')

@login_required(login_url = '/login/')
def updateRecipe(request, id):
    querySet = Recipe.objects.get(id=id)
    
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_price = data.get('recipe_price')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        recipe_category = data.get('category')
        
        querySet.recipe_name = recipe_name
        querySet.recipe_description=recipe_description
        querySet.recipe_price = recipe_price
        querySet.recipe_category = recipe_category
    
        if recipe_image:
            querySet.recipe_image = recipe_image
            
        querySet.save()
        return redirect('/recipe/')
    
    return render (request, 'update.html', {'data':querySet})

def logout_page(request):
    logout(request)
    return redirect('/')

def UserTable(request):
    users = User.objects.all()
    querySet =[]
    
    if request.method == 'POST':
        data = request.POST
        action = data.get('action')
        
        if action == 'send':
            subject = data.get('subject')
            message = data.get('message')
            to = data.get('to')
            
            attachment = request.FILES.get('attachment')
            
        
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[to],
            )
            
            if attachment:
                attachment_name = attachment.name
                attachment_content_type = attachment.content_type
                attachment_content = attachment.read()
                email.attach(attachment_name, attachment_content, attachment_content_type)
            email.send()
            messages.success(request ,"Successfully Sent Your Email")
            return redirect('/recipe/table/')
                
    if request.GET.get('search'):
        users = users.filter(username__icontains =request.GET.get('search'))
    if not users:
        messages.error(request, 'No User Found !')    
        return render(request , 'table.html' , {'querySet': querySet})
    for user in users:
        order_count = Order.objects.filter(user=user).count()
        querySet.append({'user':user ,'order_count':order_count})
        
    context = {'querySet':querySet }
    
    return render(request, 'table.html' , context)


def get_user_email(request, cid):
    user = User.objects.get(id=cid)  # Replace with your logic to retrieve the user
    email = user.email
    response = {
        'email': email
    }
    return JsonResponse(response)

def user_order(request , uid):
    user = User.objects.get(id = uid)
    
    order = Order.objects.filter(user = user)
    
    search = request.GET.get('search')
    if search:
        order = order.filter(order_item__icontains = search)
    
    context = {'orderData':order , 'user':user , 'uid':uid}
    
    if not order:
        context['error_message']='No order Items Found'
       
    return render(request , 'orderDetails.html' , context)

def approval(request , oid):
    try:
        order = Order.objects.get(id = oid)
        order.order_status = "Approved"
        order.save()
        messages.success(request , 'successfully approved user request ' )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    except Exception as e:
        return render(request , 'orderDetails.html')
    