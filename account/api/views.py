from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from account.models import Account, Freelancer, Client,Order,UpcomingOrder,Portfolio
from client.models import AvailableProjects
from django.contrib.auth.models import auth, User
from django.contrib.auth import logout, login, authenticate
from account.forms import AccountAuthenticationForm
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import datetime
import random
from datetime import date
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# @csrf_exempt
# @api_view(['GET',])
# # @permission_classes([IsAuthenticated])
# @permission_classes([])
# def product_api(request, id=None):
#     if request.method == "GET":
#         if id is None:
#             data = Product.objects.all()
#             serializer = ProductSerializer(data, many=True)
#             # print("hellloooo",serializer.data[0])
#             for i in serializer.data:
#                 sub = SubCategory2.objects.get(id=i['subcategory2'])
#                 i['subcategory2'] = sub.name
#                 i['subcategory1'] = sub.subcategory1.name
#                 i['category'] = sub.subcategory1.category.name
#
#             return Response(serializer.data)
#
#         else:
#             # data = Product.objects.get(pk=id)
#             data = Product.objects.filter(pk=id)
#             serializer = ProductSerializer(data, many=True)
#             print(data[0])
#             serializer.data[0]['subcategory2'] = data[0].subcategory2.name
#             serializer.data[0]['subcategory1'] = data[0].subcategory2.subcategory1.name
#             serializer.data[0]['category'] = data[0].subcategory2.subcategory1.category.name
#             # print(serializer.data)
#             return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         # print(serializer.data)
#         if serializer.is_valid():
#             data = serializer.data
#             vendor = VendorAccount.objects.get(email=request.user.email)
#             data["vendor"]=vendor
#             data.save()
#
#             # serializer.save()
#             return Response({'msg', 'DATA CREATED'})
#         return Response(serializer.errors)
#
#     if request.method == 'PUT':
#         data = Product.objects.get(pk=id)
#         serializer = ProductSerializer(data, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             print("PUT data", serializer.data)
#             return Response({'msg', 'Data Updated'})
#         return Response(serializer.errors)
#
#     if request.method == 'DELETE':
#         data = Product.objects.get(pk=id)
#         data.delete()
#         return Response({'msg': 'data deleted'})


def increment_month(dictionary, date):
    # Convert date string to datetime object
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    # Extract the month from the date object
    month = date_obj.strftime('%B')
    
    # Increment the value of the month in the dictionary
    if month in dictionary:
        dictionary[month] += 1
    else:
        dictionary[month] = 1

@csrf_exempt
@api_view(['GET',])
# @permission_classes([IsAuthenticated])
@permission_classes([])
def monthly_report_api(request, id=None):
    if request.method == "GET":
        if id is None:
            freelancer = Freelancer.objects.get(email=request.user.email)
            orders=Order.objects.filter(freelancer=freelancer)
            # upcoming_order=UpcomingOrder.objects.filter(freelancer=freelancer)
            dictionary = {}
            for order in orders:
                date=order.deadline
                # Convert date string to datetime object
                # date_obj = datetime.strptime(date, '%Y-%m-%d')
                
                # Extract the month from the date object
                month = date.strftime('%B')
                
                # Increment the value of the month in the dictionary
                if month in dictionary:
                    dictionary[month] += 1
                else:
                    dictionary[month] = 1
            print(dictionary)
            return Response(dictionary)

        



