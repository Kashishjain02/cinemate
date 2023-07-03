from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from .models import Account, Freelancer, Client,Order,UpcomingOrder,AvailableProjects,Portfolio
# from cart.models import Cartdata
from django.contrib.auth.models import auth, User
from django.contrib.auth import logout, login, authenticate
from account.forms import AccountAuthenticationForm
import requests
import json
import datetime
import random
from datetime import date
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
# ---------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------



# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def register(request):
    user = request.user
    if user.is_authenticated:
        if user.is_freelancer:
            return redirect("dashboard")
        else:
            return redirect("home")
    return render(request, "account/account_notreg.html")

def userregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST.get('password')
        print("name: ", name)
        try:
            user = Account.objects.create_user(
                name=name, email=email, password=password,  viewpass=password
            )
            user.is_freelancer = True
            user.save()
            freelancer = Freelancer.objects.create(freelancer=user, email=email)
            freelancer.save()
            login(request, user)
            msg = "User Registration Successful"
            # return HttpResponse(msg)
            return redirect("dashboard")
        except IntegrityError as e:
            print(e)
            msg = email + " is already registered"
            return render(request, "account/register.html",{ 'msg': msg })
        except Exception as e:
            print(e)
            msg =" username is already registered"
            return render(request, "account/register.html",{ 'msg': msg })

        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return render(request, "account/register.html")


def clientregister(request):
    print("client register")
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST.get('password')
        print("name: ", name)
        try:
            user = Account.objects.create_user(
                name=name, email=email, password=password,  viewpass=password
            )
            user.is_client = True
            user.save()
            client = Client.objects.create(client=user, email=email)
            client.save()
            login(request, user)
            msg = "User Registration Successful"
            # return HttpResponse(msg)
            return redirect("home")
        except IntegrityError as e:
            msg = email + " is already registered"
            return render(request, "account/clientregister.html",{ 'msg': msg })
        except Exception as e:
            print(e)
            return render(request, "account/clientregister.html",{ 'msg': msg })

        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return render(request, "account/clientregister.html")


def userlogin(request):
    user = request.user
    if user.is_authenticated:
        if user.is_freelancer:
            return redirect("dashboard")
        else:
            return redirect("home")
    else:
        if request.POST:
            email = request.POST['email']
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                # request.user = user
                # next = request.POST.get('next', '../')
                # if next == "":
                #     next="../"
                # return redirect(next)
                if user.is_freelancer:
                    return redirect("dashboard")
                else:
                    return redirect("home")
            else:
                msg = "invalid Email or password"
                form = AccountAuthenticationForm()
                return render(request, 'account/login.html', {"form": form, "msg": msg})

        else:
            form = AccountAuthenticationForm()
        return render(request, 'account/login.html', {"form": form})
    # username=BaseUserManager.normalize_email(username)

@csrf_exempt
# @api_view(['GET','POST'])
def update_dp(request):
    if request.user.is_authenticated:
            print("user is authenticated")
            if request.method == 'POST' and request.FILES.get('file'):
                uploaded_file = request.FILES['file']

                # Process the uploaded file here
                
                user=Account.objects.get(email=request.user.email)
                user.image=uploaded_file
                user.save()
            return render(request, 'account/update_dp.html')
        
    else:
        return redirect("login")


@login_required(login_url="../login")
def logoutuser(request):
    logout(request)
    return redirect("../")

def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_freelancer:
            user = request.user
            freelancer = Freelancer.objects.get(email=user.email)
            orders=Order.objects.filter(freelancer=freelancer)
            upcoming_order=UpcomingOrder.objects.filter(freelancer=freelancer)
            available_projects=AvailableProjects.objects.first()
            return render(request, "account/dashboard.html",{'orders':orders,'freelancer':freelancer,'user':user,'upcoming_orders':upcoming_order,'available_project':available_projects})
        else:
            return redirect("home")
    else:
        return redirect("../login")

def myportfolio(request):
    if request.user.is_authenticated:
        if request.user.is_freelancer:
            freelancer = Freelancer.objects.get(email=request.user.email)
            portfolio = Portfolio.objects.filter(freelancer=freelancer)
            return render(request, "account/myportfolio.html",{ 'portfolio': portfolio })
        else:
            return redirect("home")
    else:
        return redirect("../login")

def editportfolio(request):
    if request.user.is_authenticated:
        if request.user.is_freelancer:
            freelancer = Freelancer.objects.get(email=request.user.email)
            portfolio = Portfolio.objects.filter(freelancer=freelancer)
            return render(request, "account/edit_portfolio.html",{ 'portfolio': portfolio })
        else:
            return redirect("home")
    else:
        return redirect("../login")


def edit_portfolio(request):
    if request.user.is_authenticated:
        if request.user.is_freelancer:
            freelancer = Freelancer.objects.get(email=request.user.email)
            portfolio = Portfolio.objects.filter(freelancer=freelancer)
            # print("portfolio: ", portfolio)
            if request.method == 'POST':
                link = request.POST['video_link']
                # Extracts the video ID from a YouTube video link.
                # Parse the link using the urlparse function from the urllib.parse module
                if "youtube.com" in link:
                    video_id = link.split("v=")[1]
                    ampersand_pos = video_id.find("&")
                    if ampersand_pos != -1:
                        video_id = video_id[:ampersand_pos]
                elif "youtu.be" in link:
                    video_id = link.split("/")[-1]
                else:
                    msg="Invalid YouTube link"
                # freelancer.portfolio.insert(0, video_id)
                Portfolio.objects.create(freelancer=freelancer, link=video_id,is_image=False)
        
                # freelancer.save()
                return redirect("edit_portfolio")
            return render(request, "account/edit_portfolio.html",{ 'portfolio': portfolio ,"freelancer":freelancer})
        else:
            return redirect("unauthorized")
    else:
        return redirect("../login")


@csrf_exempt
# @api_view(['GET','POST'])
def upload_file(request):
    if request.user.is_authenticated:
        if request.user.is_freelancer:
            if request.method == 'POST' and request.FILES.get('file'):
                uploaded_file = request.FILES['file']

                # Process the uploaded file here
                print(uploaded_file.name)
                portfolio=Portfolio.objects.create(freelancer=Freelancer.objects.get(email=request.user.email), image=uploaded_file,is_image=True,date=datetime.date.today())
                portfolio.save()
            return render(request, 'account/upload.html')
        else:
            return redirect("unauthorized")
    else:
        return redirect("login")




def myprojects(request):
    if request.user.is_authenticated:
        if request.user.is_freelancer:
            freelancer = Freelancer.objects.get(email=request.user.email)
            orders=Order.objects.filter(freelancer=freelancer).order_by('completion_date')
            upcoming_order=UpcomingOrder.objects.filter(freelancer=freelancer).order_by('deadline')
            return render(request, "account/myprojects.html",{ 'orders': orders,'upcoming_orders':upcoming_order })
        else:
            return redirect("unauthorized")
    else:
        return redirect("login")

def home(request):
    # if request.user.is_authenticated:
    #     return redirect("../dashboard/")
    # else:
        return render(request, "account/home.html")


@login_required(login_url="../login")
def account_view(request):
    # if not request.user.is_authenticated:
    #     return redirect("../login")
    global msg
    context = {"name": request.user.name, "email": request.user.email, "contact_number": request.user.contact_number,
               "msg": msg}
    if request.POST:
        name = request.POST['name']
        contact_number = request.POST.get('contact_number')
        email = request.POST['email']
        password = request.POST.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user:
            userid = request.user.id
            Account.objects.filter(id=userid).update(name=name, email=email, contact_number=contact_number)
            context = {"name": name, "email": email, "contact_number": contact_number, "msg": ""}
        else:
            msg = "Wrong Password"
            context["msg"] = msg
    return render(request, 'account/myaccount.html', context)


@login_required(login_url="../login")
def changepassword(request):
    global msg
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    user = authenticate(email=request.user.email, password=password)
    if user:
        if new_password == confirm_password:
            userid = request.user.id
            u = Account.objects.get(id=userid)
            u.set_password(new_password)
            u.save()
            Account.objects.filter(id=userid).update(viewpass=new_password, )
            msg = "Password Changed"
        else:
            msg = "new password does not match with confirm password"
    else:
        msg = "Wrong password"
    return redirect("../account")


def unauthorized(request):
    return render(request, 'account/unauthorized.html')

def settings(request):
    user=Account.objects.get(email=request.user.email)
    if request.method == 'POST':
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.about = request.POST['about']
        user.username = request.POST['username']
        try:
            user.save()
        except:
            return render(request, "account/settings.html",{ 'user': user , 'error': "username already exists"})
        return redirect("dashboard")
    return render(request, "account/settings.html",{ 'user': user })


def report(request):
    if request.user.is_authenticated:
        if request.user.is_freelancer:
            freelancer = Freelancer.objects.get(email=request.user.email)
            orders=Order.objects.filter(freelancer=freelancer)
            upcoming_order=UpcomingOrder.objects.filter(freelancer=freelancer)
            return render(request, "account/report.html",{'orders':orders,'freelancer':freelancer,'upcoming_orders':upcoming_order})
        else:
            return redirect("unauthorized")
    else:
        return redirect("login")


def check(request):
    return render(request, 'account/temp.html')


