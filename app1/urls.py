from django.urls import path
from . import views
app_name = 'app1'
urlpatterns = [
    path("",views.index, name = "index"),
    #path("flights", views.flights, name = 'flights'),
    path("flightbuy", views.flightbuy, name='flightbuy'),
    path('captcha',views.captcha, name='captcha'),
    path('bank/<str:bankname>',views.bankretrun, name='bankreturn'),
    path('issue/<str:id>',views.issue, name='issue'),
    path('pay',views.pay,name='pay'),
    path('getticket',views.getticket,name="getticket"),
    path('api/autofill/trainstations/<str:name>',views.irantrainstationsapi, name="irantrainstationsapi"),
    path('Search/Flights/<str:Origin>/<str:Destination>/<str:DepartureDate>/<str:PassengerCount>',views.flights, name = 'flights'),
    path('Search/Flights/<str:Origin>/<str:Destination>/<str:DepartureDate>/<str:DestinationDate>/<str:PassengerCount>',views.flights, name = 'flights1'),
    path('Search/Trains/<int:OriginCode>/<int:DestinationCode>/<str:MoveDate>/<int:PassengerCount>/<int:Type>',views.trains, name = 'trains'),
]

