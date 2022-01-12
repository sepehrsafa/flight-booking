from keys import nira_key
import requests
from app1.models import sale
def ticketissue(OrderID):
    saleobject = sale.objects.get(pk=OrderID)
    flightdataobject = saleobject.flightdata.first()
    print(flightdataobject)
    if int(flightdataobject.FlightProvider) ==1000:
        Airline = flightdataobject.FlightAirline
        print(Airline)
        user = nira_key(Airline,'user')
        password = nira_key(Airline,'password')
        requesturl = nira_key(Airline,'ETISSUE')+'/ETIssueJS'
        params = {'PNR':saleobject.PNR,'Airline':Airline,'EMail':'safasepehr@gmail.com','OfficeUser':user,'OfficePass':password}
        res = requests.get(url = requesturl, params = params, timeout=3)

        print(res.text)


