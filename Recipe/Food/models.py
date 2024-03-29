from django.db import models

# Create your models here.

class Recipe(models.Model):
  recipe_name = models.CharField(max_length=200)
  recipe_description = models.TextField(max_length=100)
  recipe_category = models.TextField(max_length=100, default='Uncategorized')
  recipe_price = models.IntegerField(default=0)
  recipe_image = models.ImageField(upload_to='images')
  recipe_view_count = models.IntegerField(default=1)
  
  def __str__(self) -> str:                   
    return self.recipe_name
  