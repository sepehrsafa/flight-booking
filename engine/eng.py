from keys import amadeus_key, nira_key
from tokens import amadeus_Token
import requests
from threading import Thread

#params for amadeus API
#non required are = None
def amadeus_Flight_Offers_Search(originLocationCode, destinationLocationCode, departureDate, adults , returnDate = None, children = 0,\
 infants = 0, travelClass = None, includedAirlineCodes = None, excludedAirlineCodes = None, nonStop = 'false', currencyCode = 'CAD'):

    #FUNCTION VALUSE IN TERMS OF PYTHON DICT
    args = locals()
    # DICT FOR API PARAMS
    params = {}
    #IF THE VALUE PROVIDED BY USER IS NOT NONE, ADD TO PARAMS DICT FOR API
    for key in args:
        if args[key] != None:
            params[key] = args[key]
    # GETTING AMADEUS URL FOR FLIGHT OFFERS SEARCH
    amadeus_searcheurl = amadeus_key('test','Flight_Offers_Search')
    # GETTING TOKEN FROM AMADEUS AUTHORIZATION API
    headers = {"authorization":amadeus_Token('test')}
    # MAKING GET REQUEST TO AMADEUS FLIGHT OFFERS SEARCH API
    res = requests.get(url = amadeus_searcheurl[0] , headers= headers, params=params)
    res = res.json()
    return res

def nira_AvailabilityJS(Airline, cbSource, cbTarget, cbDay1, cbMonth1, cbAdultQty = '1', cbChildQty = '0', cbInfantQty = '0'):

    # DICT FOR API PARAMS
    params = {'cbSource':cbSource,'cbTarget':cbTarget,'cbDay1':cbDay1,'cbMonth1':cbMonth1}

    #GETTING URL, PASS AND USER FROM PYTHON DICT IN KEYS.PY
    airline_nira_url = nira_key(Airline,'Availability')+'/AvailabilityJS.jsp'
    airline_nira_fare_url = nira_key(Airline,'Fare')+'/Fare.jsp'
    user = nira_key(Airline,'user')
    password = nira_key(Airline,'password')
    params['OfficeUser'] = user
    params['OfficePass'] = password
    #MAKING GET REQUEST
    res = requests.get(url = airline_nira_url, params = params)
    #CHEACKING THE API RESPONSE
    if res.status_code != 200:
         return res.status_code
    data = res.json()
    count = 0
    #CREATING AN EMPTY DICT FOR ALL FLIGHTS
    filterd_flights = {
    'count': count,
    'flights':[]
    }
    # TOTAL AVAILABLE FLIGHTS
    number_of_flights = len(data["AvailableFlights"])
    #IF ANY FLIGHT IS AVAILABLE
    if number_of_flights > 0:
        #LOOPING THROUGH THE FLIGHTS
        for flight in range(number_of_flights):
            '''each_flight:{}
            each_flight['Origin'] = data["AvailableFlights"][flight]["Origin"]
            each_flight['Destination'] = data["AvailableFlights"][flight]["Destination"]'''

            print(data['AvailableFlights'][flight]['ClassesStatus'],'\n\n\n')
            #GETTING ALL THE CLASSES
            all_classes= data['AvailableFlights'][flight]['ClassesStatus']
            #REMOVING THE '/'
            all_classes = all_classes.replace('/','')
            #SPLITING THE STRING INTO A LIST
            all_classes = all_classes.split()
            #all_prices = all_prices.split()
            print(all_classes)
            #CREATING AN EMPTY DICT FOR AVAILABLE CLASSES
            available_classes = {}
            #FOR
            for i in range(len(all_classes)):
                each_class = all_classes[i][-1]
                if  each_class != ('C' or 'X'):
                    free = all_classes[i]
                    if each_class == 'A':
                        available_classes[free[:-1]] = '9+'
                    else:
                        available_classes[free[:-1]] = each_class
            for key in available_classes:
                params_fare ={'Route':cbSource+'-'+cbTarget,'RBD':key,'OfficeUser':user,'OfficePass':password}
                fare = requests.get(url = airline_nira_fare_url, params = params_fare)
                #fare = fare.json()





            print(available_classes,'all')

            #print('the',all_classes,'          .')


            #{'MD': '9+', 'N': '7'}
    {'AvailableFlights': [{'DepartureDateTime': '2020-07-14 15:55:00', 'Airline': 'ZV', 'ArrivalDateTime': '2020-07-14 17:25:00',
     'AdultTotalPrices': 'M:2330000 O:2391000 N:2572000 R:2773000 RD:2879000 B:2985000 D:3388000 G:21280000', 'Origin': 'THR',
     'FlightNo': 4043, 'Destination': 'KER', 'ClassesStatus': '/MC OC NC RC RDC BC DC GC', 'AircraftTypeCode': 'M83'}]}
    return res.json()



if __name__ == '__main__':
    #print(nira_AvailabilityJS('zv','thr','ker','1','5','1'))
    #print(threading.Thread(target=amadeus_Flight_Offers_Search('YTO','THR','2020-08-01','1')).start())
    print(Thread(target = nira_AvailabilityJS('zv','thr','mhd','25','4','1')).start())
    print(Thread(target = amadeus_Flight_Offers_Search('yyz','ika','2020-08-1','1')).start())

    #print(nira_AvailabilityJS('zv','thr','mhd','25','4','1'))




    #nira_AvailabilityJS('zv','thr','ker','1','5',1,1,1)
