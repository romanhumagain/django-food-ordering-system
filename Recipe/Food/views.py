from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from django.contrib import messages


# Create your views here.
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

def deleteRecipe(request, id):
    data = Recipe.objects.get(id = id)
    data.delete()
    return redirect('/recipe/')


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