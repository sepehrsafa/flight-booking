from django.shortcuts import render
from app1.models import sale
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.template.response import TemplateResponse
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboardpanel:login"))
    #return render(request, "dash-index.html")
    return render(request, "dash-index.html")

def salesinfo(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboardpanel:login"))
    else:
        salesinfos= sale.objects.all().order_by('-OrderNumber')[:20]
        saledata = []
        for salesinfo in salesinfos:
            saleinfodata = {}
            saleinfodata["OrderNumber"] = salesinfo.OrderNumber
            saleinfodata["FirstName"] = salesinfo.passenger.first().FirstName
            saleinfodata["LastName"] = salesinfo.passenger.first().LastName
            saleinfodata["FlightNumber"] = salesinfo.flightdata.first().FlightNumber
            saleinfodata["FlightOriginAirport"] = salesinfo.flightdata.first().FlightOriginAirport
            saleinfodata["FlightDestinationAirport"] = salesinfo.flightdata.first().FlightDestinationAirport
            saleinfodata["FlightDepartureDataTime"] = salesinfo.flightdata.first().FlightDepartureDataTime.strftime("%d/%m/%Y - %H:%M")
            saleinfodata["PNR"] = salesinfo.PNR
            saleinfodata["FlightAirline"] = salesinfo.flightdata.first().FlightAirline
            saleinfodata["OrderTime"] = salesinfo.OrderTime.strftime("%d/%m/%Y - %H:%M")
            saleinfodata["TotalPrice"] = "{:,}".format(salesinfo.TotalPrice)
            
            saledata.append(saleinfodata)
            print(salesinfo)
        print(saledata)
        return JsonResponse({'saledata':saledata})
    #print(salesinfo)



def login_view(request):
    if request.method == "POST":
        # Accessing username and password from form data
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to index page:
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboardpanel:index"))
        # Otherwise, return login page again with new context
        else:
            return render(request, "auth_login.html")

    return render(request, "auth_login.html")

def logout_view(request):
    # Pass is a simple way to tell python to do nothing.
    logout(request)
    return render(request, "auth_login.html")