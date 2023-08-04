from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
# from .models import related models
from .restapis import (get_dealers_from_cf, get_dealer_by_id_from_cf, post_request,)
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.methos == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp/index')
        else:
            context['message'] = "Invalid username or password "
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New User")
        if not user_exist:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "User already exists!"
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/a51e16c4-ec5b-410a-8942-aa1da20c86cf/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/a51e16c4-ec5b-410a-8942-aa1da20c86cf/dealership-package/get_reviews"
        results = get_dealer_by_id_from_cf(url, dealer_id)
        review_contents= ' '.join([result.review for result in results])
        return HttpResponse(review_contents)
        
        
# def add_review(request, dealer_id):
#     user = request.user
#     context = {}
#     if user.is_authentificated:
#         if request.method == "GET":
#             return render(request, 'djangoapp/add_review.html', context)
#         elif request.method == "POST":
#             json_payload = {}
#             add.json_payload["review"]
#             review["name"] = request.POST['username']
#             review["time"] = datetime.utcnow().isoformat()
#             review["dealership"] = dealer_id
#             review["review"] = request.POST['review']
#             review["purchase"] = request.POST['purchase']
#             url = "your-cloud-function-domain/dealership-package/add-review"
#             post_request(url, json_payload, dealer_id)
#             return redirect(reverse(viewname='djangoapp:get_details', args=(dealer_id)))
#     else:
#         context = "Invalid user"
#         return render(request, 'djangoapp/get_details.html', context)
