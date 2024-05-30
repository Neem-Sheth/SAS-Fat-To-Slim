from django.contrib.auth.models import AbstractUser
from django.db import models

from simple_history.models import HistoricalRecords


class User(AbstractUser):

    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f'{self.username}' 
    
    history = HistoricalRecords()
    
# class Phone(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     phone = models.DecimalField(max_digits=10, decimal_places=0)

#     class Meta:
#         verbose_name = 'Phone'
#         verbose_name_plural = 'Phone'
#     def __str__(self):
#         return f'{self.phone}'
 

class FoodCategory(models.Model):
    category_name = models.CharField(max_length=50)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return f'{self.category_name}'

    @property
    def count_food_by_category(self):
        return Food.objects.filter(category=self).count()


class Food(models.Model):
    food_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    calories = models.IntegerField(default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=7, decimal_places=2)
    protein = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='food_category')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.food_name} - category: {self.category}'


class Image(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='get_images')
    image = models.ImageField(upload_to='images/')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.image}'


class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    # date_logged = models.DateField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Log'

    def __str__(self):
        return f'{self.user.username} - {self.food_consumed.food_name}'


class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    entry_date = models.DateField()
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Weight'
        verbose_name_plural = 'Weight'

    def __str__(self):
        return f'{self.user.username} - {self.weight} kg on {self.entry_date}'
