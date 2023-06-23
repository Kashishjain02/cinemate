from django.shortcuts import render
from account.models import Account, Freelancer, Client,Order,UpcomingOrder,AvailableProjects,Portfolio
from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # freelancer = Freelancer.objects.get(email=request.user.email)
        portfolio = Portfolio.objects.all()
        return render(request, "client/home.html",{ 'portfolio': portfolio })
    else:
        return redirect("../login")

def profile(request,id):
    if request.user.is_authenticated:
        freelancer = Freelancer.objects.get(pk=id)
        portfolio = Portfolio.objects.filter(freelancer=freelancer)
        return render(request, "client/crew_profile.html",{ 'freelancer': freelancer, 'portfolio': portfolio })
    else:
        return redirect("../login")

def upcoming_order(request):
    if request.user.is_authenticated:
        upcoming_order = UpcomingOrder.objects.filter(client=Client.objects.get(email=request.user.email))
        # print(upcoming_order)
        return render(request, "client/upcoming_projects.html",{ 'upcoming_orders': upcoming_order })
    else:
        return redirect("../login")

def invoices(request):
    pass

def settings(request):
    user=Account.objects.get(email=request.user.email)
    if request.method == 'POST':
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.about = request.POST['about']
        user.username = request.POST['username']
        user.save()
        return redirect("../client/settings")
    return render(request, "client/settings.html",{ 'user': user })