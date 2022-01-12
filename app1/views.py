from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from datetime import datetime, date
import jdatetime
from persiantools.jdatetime import JalaliDate
import json
from django.views.decorators.csrf import csrf_exempt
from .models import sale, ipginfo, transaction,irantrainstations
import time
import persian
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
import pdfkit
import reportlab
from django.db.models import Q
from django.template import loader


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app1.serializers import irantrainstationsserializer

import sys
from projectparse.settings import BASE_DIR
sys.path.append(f'{BASE_DIR}/engine')

from final import iranflights
from captcha import captcha724
from book import iranreserve
from soap import PECsale,PECconfirm,PECrefund
from bpm import mellat,mellatverify,mellatsettel
from issue import ticketissue
#from raja import stations, availableTrains


def index(request):
    print('index:\n',request)
    return render(request, "index.html")

def trains(request,OriginCode,DestinationCode,MoveDate,Type,PassengerCount):
    DepartureDateList = MoveDate.split("-")
    MoveDateMiladi = jdatetime.date(int(DepartureDateList[0]),int(DepartureDateList[1]),int(DepartureDateList[2])).togregorian().strftime("%Y-%m-%d")
    trains = availableTrains(OriginCode,DestinationCode,MoveDateMiladi,Type,PassengerCount)
    print(trains)
    
    
    return render(request, 'train-results.html', {
    'trains': trains,
    
    })
    

def flights(request,Origin,Destination,DepartureDate,PassengerCount,DestinationDate=""):
    PassengerCount = PassengerCount.split("-")
    print(PassengerCount)
    DepartureDateList = DepartureDate.split("-")
    DepartureDateMiladi = jdatetime.date(int(DepartureDateList[0]),int(DepartureDateList[1]),int(DepartureDateList[2])).togregorian().strftime("%Y-%m-%d")
    x = iranflights(Origin,Destination,DepartureDateMiladi,DepartureDate,int(PassengerCount[0]),int(PassengerCount[1]),int(PassengerCount[2]))
    return render(request, 'flight-results.html', {
    'flights': x
    })


def captcha(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    print(body)
   
    originLocationCode = body['originLocationCode']
    destinationLocationCode = body['destinationLocationCode']
    departureDate = body['departureDate']
    departureTime = body['departureTime']
    flightNum = body['flightNum']
    source = body['source']
    airlineName = body['airlineName']
    airlineIATAcode = body['airlineIATAcode']
    captchadata = captcha724(originLocationCode,destinationLocationCode,departureDate,departureTime,flightNum,source,airlineName,airlineIATAcode)

    return JsonResponse(captchadata)

def flightbuy(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data)

    airline=data['FlightObject']['Flight_Data'][0]['Airline']

    originLocationCode=data['FlightObject']['Flight_Data'][0]['Origin']

    destinationLocationCode=data['FlightObject']['Flight_Data'][0]['Destination']

    departureDate=data['FlightObject']['Flight_Data'][0]['DepartureDate']
    departureTime=data['FlightObject']['Flight_Data'][0]['DepartureTime']
    departureDateTime = departureDate +" "+departureTime
    departureDateTimeObject = datetime.strptime(departureDateTime, '%Y-%m-%d %H:%M:%S')

    flightClass=data['FlightObject']['Flight_Fare'][0]['CabinClassName']

    flightNum=data['FlightObject']['Flight_Fare'][0]['FlightNumberUsedbyIssuer']

    charter724IssuerCode=data['FlightObject']['Flight_Fare'][0]['IssuerCode']

    fareType = data['FlightObject']['Flight_Fare'][0]['ClassType']

    passengerInfo = data["Passengers"]
    passengerInfo = [passengerInfo]

    passengerMobile = data["PhoneNumber"]

    passengerEmail = data["Email"]

    captchCode = int(data["CaptchaCode"])

    requestID = int(data["Requestid"])
    TotalPrice =int(data['FlightObject']['Flight_Fare'][0]['AdultTotalPrice'])


    PNRData = iranreserve(airline,charter724IssuerCode,originLocationCode,destinationLocationCode,departureDate,departureTime, flightClass, flightNum, passengerInfo,passengerMobile, passengerEmail,captchCode,requestID)
    print(PNRData)
    if PNRData["statuscode"] == 200:
        IssuerAgency = PNRData['PNRData']['IssuerAgency']
        PNRTotalPrice = PNRData['PNRData']['PNRTotalPrice']
        NUMPassengers = PNRData['PNRData']['NUMPassengers']
        if IssuerAgency == 1:
            saleobject = sale(NumberofTickets=NUMPassengers,TotalPrice=PNRTotalPrice, PNR=PNRData['PNRData']['PNR']) 
            saleobject.save()
        
        elif IssuerAgency == 2:
             saleobject = sale(NumberofTickets=NUMPassengers,TotalPrice=PNRTotalPrice, RequestID=requestID, FaktorID= PNRData['PNRData']['Charter724FaktorID']) 
             saleobject.save()

        saleobject.flightdata.create(FlightNumber=flightNum,FlightDepartureDataTime=departureDateTimeObject,FlightProvider=charter724IssuerCode,\
            FlightType=fareType,FlightAirline=airline,FlightOriginAirport=originLocationCode,FlightOriginTerminal='',\
                FlightDestinationAirport=destinationLocationCode,FlightDestinationTerminal='')
                
        for passengerpnr in PNRData['PNRData']['Passengers']:
            print(passengerpnr)
            
            passengerobject = saleobject.passenger.create(FirstName = passengerpnr['FirstName'],LastName = passengerpnr['LastName'],Type = passengerpnr['Type'],\
                    IDNumber = passengerpnr['IDNumber'],IDEXP = None,Status = 'ok',TicketNumber = PNRData['PNRData']['PNR'])

            passengerobject.passengerprice.create(TicketBaseFare=0,TicketCommison=0,TicketTotalPrice=passengerpnr['Price'])
        print('\n\nthe order id = ',saleobject.pk)
        PNRData['SaleID'] = saleobject.pk
        print(saleobject.passenger.first().passengerprice.first())

    
    
    
    PNRData["FlightObject"] = data['FlightObject']
    print(PNRData)
    return JsonResponse(PNRData)

def pay(request):
    #return render(request, "flight-payment.html")
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    saleid = data['SaleID']
    OrderObject = sale.objects.get(pk=saleid)
    gatewayInfo = ipginfo.objects.get(pk=2)
    x = transaction(GatewayInfo=gatewayInfo, OrderNumber=OrderObject)
    x.save()
    #TransactionData = PECsale(gatewayInfo.Username,10000,x.TransactionID*20000+121, gatewayInfo.CallBackURL,SaleInfo='')
    TransactionData = mellat(gatewayInfo.Username,gatewayInfo.Password,gatewayInfo.TerminalID,x.TransactionID,11000,gatewayInfo.CallBackURL,'09133410118',CartItem='بلیز کرمان تهران')
    x.Token = TransactionData["Token"]
    x.save()
    print(TransactionData)
    return JsonResponse(TransactionData)

@csrf_exempt
def bankretrun(request, bankname):
    if request.method == 'POST':
        print(request.body)

        if bankname == "pec":
            Token = request.POST['Token']
            OrderID = request.POST['OrderId']
            Status = request.POST['status']

        elif bankname == "bpm":
            Status = int(request.POST['ResCode'])
            if Status == 0:
                Token = request.POST['RefId']
                OrderID = request.POST['SaleOrderId']
                SaleReferenceId = request.POST['SaleReferenceId']
                CardNumber = request.POST['CardHolderPan']
                AmountRecived =request.POST['FinalAmount']
                transactionobject = transaction.objects.filter(pk=OrderID)
                gatewayInfo = transactionobject.first().GatewayInfo
                if mellatverify(gatewayInfo.Username,gatewayInfo.Password,gatewayInfo.TerminalID,OrderID,SaleReferenceId)["status"] == (0 or 43):
                    print("1")
                    if mellatsettel(gatewayInfo.Username,gatewayInfo.Password,gatewayInfo.TerminalID,OrderID,SaleReferenceId)["status"] == (0 or 45):
                        print("2")
                        transactionobject.update(IPGTransactionReferenceID=SaleReferenceId,CardNumber=CardNumber,AmountRecived=AmountRecived)
                        return HttpResponse('<h1>yes</h1>')
    
    return HttpResponse('<h1>NOO</h1>')

def issue(request,id):

    return render(request, "bankreturn.html")

@api_view(["GET"])
def irantrainstationsapi(request,name):
    stations = irantrainstations.objects.filter(Q(StationNameFarsi2__startswith=name) | Q(StationNameFarsi__startswith=name) | Q(StationNameEnglish__startswith=name))
    serializer = irantrainstationsserializer(stations, many=True)
    return Response(serializer.data)





#Opens up page as PDF
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
}

    
    
def getticket(request):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    html = loader.render_to_string('in.html', {})
    output= pdfkit.from_string(html, output_path=False, configuration=config)
    response = HttpResponse(content_type="application/pdf")
    response.write(output)
    return response

    template = get_template(template_src)
	#html  = template.render(context_dict)

    options = {'encoding': "UTF-8", 'quiet': '','page-size':'A4'}
    bytes_array = pdfkit.PDFKit(resume_str, 'string', options=options).to_pdf()

    pdf = render_to_pdf('pdftem.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')




