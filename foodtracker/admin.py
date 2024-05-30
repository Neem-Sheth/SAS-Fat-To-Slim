from django.contrib import admin
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import *

from simple_history.admin import SimpleHistoryAdmin
class FoodCategoryAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        # Aggregate food count by category
        chart_data = (
            FoodCategory.objects.annotate(food_count=Count("food_category"))
            .values("category_name", "food_count")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
    

class WeightRangeAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        # Define weight ranges
        weight_ranges = [
            {"min": 0, "max": 50, "label": "0-50 kg"},
            {"min": 50, "max": 70, "label": "50-70 kg"},
            {"min": 70, "max": 90, "label": "70-90 kg"},
            {"min": 90, "max": 110, "label": "90-110 kg"},
            {"min": 110, "max": 999, "label": "110+ kg"},
        ]

        # Calculate user count in each weight range
        chart_data = []
        for range in weight_ranges:
            user_count = Weight.objects.filter(weight__gte=range["min"], weight__lt=range["max"]).count()
            chart_data.append({"weight_range": range["label"], "user_count": user_count})

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
    
class FoodAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'calories', 'category')  
    ordering = ('calories',)  

class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'phone']

admin.site.register(Food, FoodAdmin)
admin.site.register(User, UserAdmin)

admin.site.register(FoodCategory, FoodCategoryAdmin)
# admin.site.register(User)
# admin.site.register(Food)
admin.site.register(Image, SimpleHistoryAdmin)
admin.site.register(FoodLog, SimpleHistoryAdmin)
# admin.site.register(Phone)
admin.site.register(Weight, WeightRangeAdmin)
