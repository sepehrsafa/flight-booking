from keys import charter724_key,nira_key
from tokens import charter724_Token
import requests
import requests_cache
from datetime import datetime, date

from IATAAircraftTypeCodes import IATAAircraftTypeCodes

import persian
from persiantools.jdatetime import JalaliDate
import concurrent.futures

import time

def iranreserve(airline,source,originLocationCode,destinationLocationCode,departureDate,departureTime, flightClass, flightNum, passengerInfo,passengerMobile, passengerEmail,captchCode,requestID):
    passengerids = {}
    def nirareserve():
        datefornira = datetime.strptime(departureDate, "%Y-%m-%d")
        datefornirairani = JalaliDate(datefornira)
        departureDateShamsiDay = datefornirairani.day
        departureDateShamsiMonth = datefornirairani.month
        #GETTING URL, PASS AND USER FROM PYTHON DICT IN KEYS.PY
        airline_nira_url = nira_key(airline,'Reserve')
        print(airline_nira_url)

        #print(f'Airline = {Airline} cbSource = {cbSource} cbTarget = {cbTarget} ')
        #GETTING USER AND PASSWORD
        user = nira_key(airline,'user')
        password = nira_key(airline,'password')
        #SETTING PRAAMS
        params = {'Airline':airline,'cbSource':originLocationCode,'cbTarget':destinationLocationCode,'FlightClass':flightClass,'FlightNo':flightNum,'Day':departureDateShamsiDay,'Month':departureDateShamsiMonth,'edtContact':passengerMobile,'OfficeUser':user,'OfficePass':password}
        passengercount = 0
        for Passenger in passengerInfo:
            params['edtName'+str(passengercount+1)] = Passenger['FirstName']
            params['edtLast'+str(passengercount+1)] = Passenger['LastName']
            params['edtID'+str(passengercount+1)] = Passenger['IDNum']
            if Passenger['Type'] == 'Adult':
                params['edtAge'+str(passengercount+1)] = '30'
            elif Passenger['Type'] == 'Child':
                params['edtAge'+str(passengercount+1)] = '8'
            elif Passenger['Type'] == 'Infant':
                params['edtAge'+str(passengercount+1)] = '1'
            passengercount +=1
            passengerids[Passenger['FirstName'].lower()]=Passenger['IDNum']

        params['No'] = str(passengercount)


        #MAKING GET REQUEST
        res = requests.get(url = airline_nira_url, params = params )

        #CHEACKING THE API RESPONSE
        if res.status_code != 200:
             return res.status_code
        try:
            data = res.json()
        except:
            return {'statuscode':401, 'PNRData':''}

        PNR = data['AirReserve'][0]['PNR']


        rturl = nira_key(airline,'RT')
        rtprams = {'Airline':airline,'PNR':PNR,'OfficeUser':user,'OfficePass':password}
        rt = requests.get(url = rturl, params = rtprams )

        try:
            rt = rt.json()
        except:
            return {'statuscode':201, 'PNRData':PNR}


        PNRData = {
            'IssuerAgency': 1,
            'Charter724FaktorID' : '',
            'PNRTotalPrice':rt['TotalPrice']//10,
            'PNR':PNR,
            'NUMPassengers':0,
            'Passengers':[]

        }
        for passengerrt in rt['Passengers']:
            passengerjson = {}
            passengerjson['FirstName'] = (passengerrt['PassenferFirstName'].lower()).capitalize()
            passengerjson['LastName'] = (passengerrt['PassenferLastName'].lower()).capitalize()
            passengerType = passengerrt['PassenferAgeType']
            passengerType = passengerType[:-1]
            passengerType = passengerType[1:]
            passengerjson['Type'] = passengerType
            passengerjson['IDNumber'] = passengerids[passengerrt['PassenferFirstName'].lower()]
            passengerprice = int(rt[passengerType+'TP']/rt[passengerType+'QTY'])//10
            passengerjson['Price'] = passengerprice
            PNRData['Passengers'].append(passengerjson)
            PNRData['NUMPassengers'] +=1

        return {'statuscode':200, 'PNRData':PNRData}



    def chrter724reserve():
        charter724token = charter724_Token()

        passengerslist = []
        for passenger in passengerInfo:
            passengerobject = {}
            passengerobject['fnameen'] = passenger['FirstName']
            passengerobject['lnameen'] = passenger['LastName']

            if passenger['Type'] == 'Adult':
                passengerobject["passengerType"] = "ADL"
            elif passenger['Type'] == 'Child':
                passengerobject["passengerType"] = "CHD"
            elif passenger['Type'] == 'Infant':
                passengerobject["passengerType"] = "INF"
        
            if passenger['Gender'] == 'Male':
                passengerobject['gender'] = 1
            else:
                passengerobject['gender'] = 2

            if passenger['Nationality'] == 'IRN':
                passengerobject['nationality'] = 1
                passengerobject['nationalitycode']='IRI'
            else:
                passengerobject['nationality'] = 2
                passengerobject['nationalitycode']=passenger['Nationality']

            passengerobject['passengerCode'] = passenger['IDNum']
            if passenger['EXdate'] != '':
                passengerobject['expdate']= passenger['EXdate']
            passengerslist.append(passengerobject)
            passengerids[passenger['FirstName'].lower()]=passenger['IDNum']

        json  = { "id_request": requestID, "captchcode": captchCode, "mobile": passengerMobile, 'email':passengerEmail , 'passengers':passengerslist}
        header = {"Content-Type": "application/json-patch+json",'Authorization':charter724token}

       
        res = requests.post(url = charter724_key('Reservation'), headers = header, json = json)
      
        if res.status_code != 200:
            return {'statuscode':res.status_code, 'data':''}

        data = res.json()

        PNRData = {
            'IssuerAgency': 2,
            'Charter724FaktorID' : data['data']['id_faktor'],
            'PNRTotalPrice':int(data['data']['totalprice_request'])//10,
            'PNR':'',
            'NUMPassengers':0,
            'Passengers':[],

        }
        for passenger724 in data['data']['passenger_info']:
            passengerjson = {}
            passengerjson['FirstName'] = (passenger724['fname'].lower()).capitalize()
            passengerjson['LastName'] = (passenger724['lname'].lower()).capitalize()
            passengerType = passenger724['type']
            if passengerType == 'ADL':
                passengerjson['Type'] = 'Adult'
            elif passengerType == 'CHD':
                passengerjson['Type'] = 'Child'
            elif passengerType == 'INF':
                passengerjson['Type'] = 'Infant'
            passengerjson['IDNumber'] = passengerids[passenger724['fname'].lower()]        
            passengerjson['Price'] = int(passenger724['real_price']//10)
            PNRData['Passengers'].append(passengerjson)
            PNRData['NUMPassengers'] +=1

        return {'statuscode':200, 'PNRData':PNRData}


    





    if int(source) == 1000:
        return nirareserve()

    else:
        return chrter724reserve()

'''
test = [
{
'FirstName':'sepehr',
'LastName':'shamsi',
'Type':'Adult',
'IDNum':'3256654120',
'EXdate': '',
'Nationality' : 'IRN',
'Gender' : 'Male',
}
]

iranreserve('zv','32','thr','mhd','2020-07-29','23:00:00', '', 'ch6256',test,'09133410118','sepehr@gmail.com',1854,900592)
'''
'''
{"result":"true","msg":"Reservation",
"data":{"id_request":932175,"id_faktor":18924913,"msg":null,"duplicate":0,"totalprice_request":"2294000",
"passenger_info":[{"fname":"sepehr","lname":"safa","type":"ADL","real_price":2294000,"fare":2088000}]}}

{"result":"true","msg":"Reservation",
"data":{"id_request":932230,"id_faktor":18925633,"msg":null,"duplicate":0,"totalprice_request":"2030000",
"passenger_info":[{"fname":"sepehr","lname":"safa","type":"ADL","real_price":2030000,"fare":0}]}}

{"Passengers":[
    {"PassenferLastName":"TEAST","PassenferFirstName":"ATEST","PassenferAgeType":"{Adult}"}
    ], 
    "AdultQTY":1,"ChildTP":610000,"TotalPrice":1140000,"Contact":"09338877426",
    "Segments":[
        {"AFlightNo":"ZV1000", "DepartureDT":"2018-04-18 22:00:00","FlightClass":"Z","Origin":"UGT","FlightNo":"1000","Destination":"TTQ"}
        ], "InfantTP":186000,"AdultTP":1140000,
        "Tickets":[{"PassengerET":"TEST/TEST:0002440382095"}],"DOCS":[],"ChildQTY":0,"InfantQTY":0,"Status":"ACTIVE","Office":"NSTHR007"}
'''
