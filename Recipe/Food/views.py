from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login as auth_login , logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url = '/login/')
def recipe(request):
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_price = data.get('recipe_price')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        recipe_category = data.get('category')
        
        print(recipe_category)

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


def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username = username)
        
        if not user.exists():
            messages.error(request , 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)
        
        if user is None:
            messages.error(request , 'Invalid Username/Password')
            return redirect('/login/')
        else:
             auth_login(request, user)
             return redirect('/recipe/')
        
    
    return render(request,'login.html')
def register(request):
    if request.method == 'POST':
        data = request.POST
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        copassword = data.get('copassword')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.error(request , "this user already exists, try another !!")
        elif len(password)<4:
            messages.error(request , "your password too short !!")   
        elif not password == copassword:
            messages.error(request , "password didn't matched ") 
        else:
            user = User.objects.create(username = username , email = email)
            user.set_password(password)
            user.save()
            messages.success(request , "successfully registered your account :)")
            return redirect('/register/')
      
    return render(request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def home(request):
    return render(request , 'home.html')

def UserTable(request):
    data = User.objects.all()
    
    if request.GET.get('search'):
        data = data.filter(username__icontains =request.GET.get('search'))
    
    context = {'querySet':data}
    
    return render(request, 'table.html' , context)