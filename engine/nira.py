import multiprocessing
from keys import nira_key
import requests
import requests_cache
from datetime import datetime, date
import time
import ast
from threading import Thread
from IATAAircraftTypeCodes import IATAAircraftTypeCodes
from operator import getitem
from collections import OrderedDict
import persian
from persiantools.jdatetime import JalaliDate
import concurrent.futures
t1 = time.time()



def nira_AvailabilityJS(Airline, cbSource, cbTarget, cbDay1, cbMonth1, cbAdultQty = '1', cbChildQty = '0', cbInfantQty = '0'):
    requests_cache.install_cache('test_cache', backend='sqlite', expire_after=300)

    fare_req = requests.Session()
    count = 0
    #GETTING URL, PASS AND USER FROM PYTHON DICT IN KEYS.PY
    airline_nira_url = nira_key(Airline,'Availability')+'/AvailabilityJS.jsp'

    airline_nira_fare_url = nira_key(Airline,'Fare')+'/FareJS.jsp'

    print(f'Airline = {Airline} cbSource = {cbSource} cbTarget = {cbTarget} ')
    #GETTING USER AND PASSWORD
    user = nira_key(Airline,'user')
    password = nira_key(Airline,'password')
    #SETTING PRAAMS
    params = {'cbSource':cbSource,'cbTarget':cbTarget,'cbDay1':cbDay1,'cbMonth1':cbMonth1,'OfficeUser':user,'OfficePass':password}
    #MAKING GET REQUEST

    with requests_cache.disabled():
        res = requests.get(url = airline_nira_url, params = params )
    #CHEACKING THE API RESPONSE
    b = time.time()
    if res.status_code != 200:
         return res.status_code


    try:
        data = res.json()
    except:
        return 400
    #CREATING AN EMPTY DICT FOR ALL FLIGHTS
    filterd_flights = {
    'Flights':[]
    }

    #LOOPING THROUGH THE FLIGHTS
    for flight in data['AvailableFlights']:

        Flight = {
        'Flight_Data':[],
        'Flight_Fare':'',
        'Flight_Rule':'',
        'Flight_Issuer':{},
        }

        #GETTING ALL THE CLASSES
        all_classes= flight['ClassesStatus']
        all_fares = flight['AdultTotalPrices']
        all_fares = all_fares.split()
        all_fares = dict(x.split(':') for x in all_fares)

        #REMOVING THE '/'
        all_classes = all_classes.replace('/','')
        #SPLITING THE STRING INTO A LIST
        all_classes = all_classes.split()

        #CREATING AN EMPTY list FOR AVAILABLE CLASSES
        available_classes = []
        fares = {}
        #FOR
        flight_is_good = False

        for flight_class in all_classes:
            class_is_good = False
            #last word inside the str (/WX LX MX OX RX BX DX EX SX TX GX) here would be X for all of them
            class_sets = flight_class[-1]
            if (class_sets != 'X') and (class_sets != 'C'):

                #this gets the whole class with the number at the end
                class_name = flight_class[:-1]
                fares[class_name] = {}

                #if the last chr is 'A' in means more than 9 is available
                if class_sets == 'A':
                    available_classes.append(class_name)
                    flight_is_good = True
                    class_is_good = True
                    fares[class_name]['AvailableSets'] = '9+'
                # else the json has a number at the end to show the available segments
                #here we are comparing the available sets to the total sets that we need based on the user input
                elif int(class_sets) >= (int(cbAdultQty) + int(cbChildQty) + int(cbInfantQty)):
                        available_classes.append(class_name)
                        flight_is_good = True
                        class_is_good = True
                        fares[class_name]['AvailableSets'] = class_sets

                if class_is_good == True:
                    params_fare ={'Route':cbSource+'-'+cbTarget,'RBD': class_name,'OfficeUser':user,'OfficePass':password}
                    fare = fare_req.get(url = airline_nira_fare_url, params = params_fare)
                    fare_data = fare.json()

                    fares[class_name]['AdultBaseFare'] = fare_data['AdultFare']
                    fares[class_name]['AdultTotalPrice'] = int(all_fares[class_name])
                    fares[class_name]['AdultTax'] = str(int(all_fares[class_name]) - int(fare_data['AdultFare']))
                    fares[class_name]['AdultTotalCost'] = str(int(all_fares[class_name])*int(cbAdultQty))

                    fares[class_name]['ChildBaseFare'] = fare_data['ChildFare']
                    fares[class_name]['ChildTotalFare'] = fare_data['ChildTotalPrice']
                    fares[class_name]['ChildTax'] = str(int(fare_data['ChildTotalPrice']) - int(fare_data['ChildFare']))
                    fares[class_name]['ChildTotalCost'] = str(int(fare_data['ChildTotalPrice'])*int(cbChildQty))

                    fares[class_name]['InfantBaseFare'] = fare_data['InfantFare']
                    fares[class_name]['InfantTotalFare'] = fare_data['InfantTotalPrice']
                    fares[class_name]['InfantTax'] = str(int(fare_data['InfantTotalPrice']) - int(fare_data['InfantFare']))
                    fares[class_name]['InfantTotalCost'] = str(int(fare_data['InfantTotalPrice'])*int(cbInfantQty))
                    Flight['FlightRule']=fare_data['CRCNRules']


        if flight_is_good == True:

            count += 1
            fares = {k: v for k, v in sorted(fares.items(), key=lambda item: item[1]['AdultTotalPrice'])}

            Flight['Flight_Fare'] = fares


            Flight['Flight_Issuer']['Source'] = 'ParseOwj Nira '+Airline.upper()
            Flight['Flight_Issuer']['InstantTicketingRequired'] = True
            Flight['Flight_Issuer']['lastTicketingDate'] = date.today()
            Flight['Flight_Issuer']['Charter'] = False


            each_flight = {}
            each_flight['Airline'] = flight['Airline']

            each_flight['Origin'] = flight["Origin"]
            each_flight['Destination'] = flight["Destination"]
            departureInfo = datetime.strptime(flight["DepartureDateTime"], '%Y-%m-%d %H:%M:%S')
            arrivalInfo =  datetime.strptime(flight["ArrivalDateTime"],'%Y-%m-%d %H:%M:%S' )
            print(departureInfo.date(),'\n\n')

            each_flight['DepartureDate'] =str(departureInfo.date())
            each_flight['DepartureDateShamsi'] = str(JalaliDate(departureInfo.date()))
            each_flight['DepartureTime'] =str(departureInfo.time())
            each_flight['ArrivalDate'] = str(arrivalInfo.date())
            each_flight['ArrivalDateShamsi'] = str(JalaliDate(arrivalInfo.date()))
            each_flight['ArrivalTime'] = str(arrivalInfo.time())
            each_flight['Duration'] =  str(arrivalInfo - departureInfo)
            each_flight['FlightNo'] = str(flight["FlightNo"])
            each_flight['ClassType'] = 'Economy'
            each_flight['AvailableClasse(s)'] = available_classes
            planeCode = flight["AircraftTypeCode"]
            each_flight['AircraftTypeCode'] = planeCode
            each_flight['AircraftName'] = IATAAircraftTypeCodes(planeCode)

            Flight['Flight_Data'].append(each_flight)
            filterd_flights['Flights'].append(Flight)

    if count!= 0:
        filterd_flights['NumofFlights'] =  count
        return filterd_flights


def allnira (cbSource, cbTarget, cbDay1, cbMonth1, cbAdultQty = '1', cbChildQty = '0', cbInfantQty = '0'):
    count = 0
    all_filterd_flights = {
    'NumofFlights': 0,
    'Flights':[]
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        zv = executor.submit(nira_AvailabilityJS, 'zv',cbSource,cbTarget,cbDay1,cbMonth1,cbAdultQty,cbChildQty,cbInfantQty)
        i3 = executor.submit(nira_AvailabilityJS, 'i3',cbSource,cbTarget,cbDay1,cbMonth1,cbAdultQty,cbChildQty,cbInfantQty)

        zv = zv.result()
        print('hi')
        i3 = i3.result()
        #print(zv)
        #print(i3)

        for zvflight in zv['Flights']:
            all_filterd_flights['Flights'].append(zvflight)
            count +=1


        all_filterd_flights['NumofFlights'] = count

        return all_filterd_flights



if __name__ == '__main__':



    print(allnira('ker','thr','6','5'))

    #print(nira_AvailabilityJS('zv','thr','ker','1','5','1'))
    #print(threading.Thread(target=amadeus_Flight_Offers_Search('YTO','THR','2020-08-01','1')).start())
    #p1 = multiprocessing.Process(target=nira_AvailabilityJS, args = ('zv','mhd','thr','20','4','1'))
    #p1.start()
    #x = nira_AvailabilityJS('zv','ker','thr','30','4','1')
    #print(x)

    '''p2 = multiprocessing.Process(target=nira_AvailabilityJS, args = ('zv','thr','mhd','4','5','1'))

    p3 = multiprocessing.Process(target=nira_AvailabilityJS, args = ('i3','thr','mhd','4','5','1'))



    p3.start()
    p2.start()
    p2.join()
    p3.join()
    print(p2.return())'''
    t2  = time.time()
    print(f'T = {t2-t1}')



    #nira_AvailabilityJS('i3','mhd','thr','1','5','1')
    #nira_AvailabilityJS('zv','mhd','thr','1','5','1')



    #x = Thread(target = nira_AvailabilityJS('zv','mhd','thr','29','4','1')).start()
