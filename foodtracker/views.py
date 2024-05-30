from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Food, FoodCategory, FoodLog, Image, Weight
from .forms import FoodForm, ImageForm


from twilio.rest import Client
from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.http import HttpResponse
from django.shortcuts import render

from django.db.models import Max


 
def index(request):
    '''
    The default route which lists all food items
    '''
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
                'categories': FoodCategory.objects.all()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.phone = phone
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
                'categories': FoodCategory.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html', {
            'categories': FoodCategory.objects.all()
        })


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.',
                'categories': FoodCategory.objects.all()
            })
    else:
        return render(request, 'login.html',  {
            'categories': FoodCategory.objects.all()
        })


# TWILIO_ACCOUNT_SID='AC3d59f402cb88c98ee578aea22848083d'
# TWILIO_AUTH_TOKEN='1197289632073f0aa812143a14a832d3'


def logout_view(request):
  
    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # user_phone_number = request.user.phone

    # food_log = FoodLog.objects.filter(user=request.user)
    # total_calories_consumed = sum(entry.food_consumed.calories for entry in food_log)
    # weight = Weight.objects.filter(user=request.user).order_by('-entry_date').first()

    # differnece_of_calories = total_calories_consumed-2000

    # if differnece_of_calories>0:
    #     message_body = f"Hello {request.user.username},\nYour weight is {weight}.\nYour total calories intake is {total_calories_consumed} calories.\nYou can still consume food of {differnece_of_calories} calories.\nThank you for connecting with SAS: Fat to Slim!"
    # else:
    #     message_body = f"Hello {request.user.username},\nYour weight is {weight}.\nYour total calories intake is {total_calories_consumed} calories.\nYou over consumed food of {abs(differnece_of_calories)} calories.\nThank you for connecting with SAS: Fat to Slim!"


    # message = client.messages.create(
    #     from_='whatsapp:+14155238886',
    #     body=message_body,
    #     to='whatsapp:+91{}'.format(user_phone_number)
    # )

    # print("Message SID:", message.sid)
    # print("User phone number:", user_phone_number)

    logout(request)
    
    return HttpResponseRedirect(reverse('index'))


def food_list_view(request):
    '''
    It renders a page that displays all food items without pagination
    '''
    foods = Food.objects.all()

    for food in foods:
        food.image = food.get_images.first()

    return render(request, 'food_list.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'title': 'Food List'
    })


def food_details_view(request, food_id):
    '''
    It renders a page that displays the details of a selected food item
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    food = Food.objects.get(id=food_id)

    return render(request, 'food.html', {
        'categories': FoodCategory.objects.all(),
        'food': food,
        'images': food.get_images.all(),
    })


@login_required
def food_add_view(request):
    '''
    It allows the user to add a new food item
    '''
    ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=2)

    if request.method == 'POST':
        food_form = FoodForm(request.POST, request.FILES)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if food_form.is_valid() and image_form.is_valid():
            new_food = food_form.save(commit=False)
            new_food.save()

            for food_form in image_form.cleaned_data:
                if food_form:
                    image = food_form['image']

                    new_image = Image(food=new_food, image=image)
                    new_image.save()

            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'success': True
            })

        else:
            return render(request, 'food_add.html', {
                'categories': FoodCategory.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
            })

    else:
        return render(request, 'food_add.html', {
            'categories': FoodCategory.objects.all(),
            'food_form': FoodForm(),
            'image_form': ImageFormSet(queryset=Image.objects.none()),
        })


@login_required
def food_log_view(request):
    '''
    It allows the user to select food items and
    add them to their food log
    '''
    if request.method == 'POST':
        foods = Food.objects.all()

        # get the food item selected by the user
        food = request.POST['food_consumed']
        food_consumed = Food.objects.get(food_name=food)

        # get the currently logged in user
        user = request.user

        # add selected food to the food log
        food_log = FoodLog(user=user, food_consumed=food_consumed)
        food_log.save()

    else:  # GET method
        foods = Food.objects.all()

    # get the food log of the logged in user
    user_food_log = FoodLog.objects.filter(user=request.user)

    return render(request, 'food_log.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'user_food_log': user_food_log
    })


@login_required
def food_log_delete(request, food_id):
    '''
    It allows the user to delete food items from their food log
    '''
    # get the food log of the logged in user
    food_consumed = FoodLog.objects.filter(id=food_id)

    if request.method == 'POST':
        food_consumed.delete()
        return redirect('food_log')

    return render(request, 'food_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })


@login_required
def weight_log_view(request):
    '''
    It allows the user to record their weight
    '''
    if request.method == 'POST':

        # get the values from the form
        weight = request.POST['weight']
        entry_date = request.POST['date']

        # get the currently logged in user
        user = request.user

        # add the data to the weight log
        weight_log = Weight(user=user, weight=weight, entry_date=entry_date)
        weight_log.save()

    # get the weight log of the logged in user
    user_weight_log = Weight.objects.filter(user=request.user)

    return render(request, 'user_profile.html', {
        'categories': FoodCategory.objects.all(),
        'user_weight_log': user_weight_log
    })


@login_required
def weight_log_delete(request, weight_id):
    '''
    It allows the user to delete a weight record from their weight log
    '''
    # get the weight log of the logged in user
    weight_recorded = Weight.objects.filter(id=weight_id)

    if request.method == 'POST':
        weight_recorded.delete()
        return redirect('weight_log')

    return render(request, 'weight_log_delete.html', {
        'categories': FoodCategory.objects.all()
    })


def categories_view(request):
    '''
    It renders a list of all food categories
    '''
    return render(request, 'categories.html', {
        'categories': FoodCategory.objects.all()
    })


def category_details_view(request, category_name):
    '''
    Clicking on the name of any category takes the user to a page that
    displays all of the foods in that category
    Food items are paginated: 4 per page
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    category = FoodCategory.objects.get(category_name=category_name)
    foods = Food.objects.filter(category=category)

    for food in foods:
        food.image = food.get_images.first()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'food_category.html', {
        'categories': FoodCategory.objects.all(),
        'foods': foods,
        'foods_count': foods.count(),
        'pages': pages,
        'title': category.category_name
    })
