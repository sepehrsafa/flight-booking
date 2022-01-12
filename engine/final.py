
from keys import charter724_key,nira_key
from tokens import charter724_Token
import requests
import requests_cache
from datetime import datetime, date

from IATAAircraftTypeCodes import IATAAircraftTypeCodes

import persian
from persiantools.jdatetime import JalaliDate
from persiantools import characters, digits
import concurrent.futures

import time


def iranflights (originLocationCode,destinationLocationCode,departureDate, departureDateShamsi,adultCount, childCount=0, infantCount=0, travelClass = None, nonStop = False, currencyCode = 'IRI', excludedAirlineCodes = []):


    filterd_flights_system = []
    filterd_flights_charter = []
    t1 =time.time()
    flight_is_there = []
    flight_is_there_time = []
    flight_is_there_charter = []
    flight_is_there_time_charter = []


    x = [0]
    def charter724_searche(excludedAirlineCodesFor724 = ['I3','ZV']):


        charter724token = charter724_Token()

        json  = { "from_flight": originLocationCode, "to_flight": destinationLocationCode, "date_flight": departureDate}
        header = {"Content-Type": "application/json-patch+json",'Authorization':charter724token}

        res = requests.post(url = charter724_key('Available'), headers = header, json = json, timeout=3)



        if res.status_code != 200:
             return res.status_code

        data = res.json()

        for flight in data['data']:
            print(flight,'\n')
           
            Flight = {
            "Flight_NUM":"",
            "Flight_Data":[],
            "Flight_Fare":[],
            "Flight_Rule":{}
            }

            if flight['price_final'] != 0 and flight['capacity'] >= adultCount+childCount+infantCount:

                each_flight = {}
                fares = {}

                last3char = flight['number_flight'][-2:]
                flighttime = flight['time_flight']
                class_name = flight['cabinclass']
                if class_name == '':
                    class_name = 'Y'

                if flight['iatA_code'].upper() not in excludedAirlineCodesFor724 and flight['type'] == 'system':

                    if (last3char in flight_is_there) and (flighttime in flight_is_there_time) :
                        index = flight_is_there.index(last3char)
                        index2 = flight_is_there_time.index(flighttime)

                        if index == index2:
                            if filterd_flights_system[index]['Flight_Data'][0]['Airline'] == flight['iatA_code']:

                                fares['CabinClassName'] = class_name
                                fares['AvailableSets'] = str(flight['capacity'])
                                fares['ClassType'] = flight['type'].upper()
                                fares['FareProvider'] = 'ParseOwj Charter 724'
                                fares['IssuerCode'] = flight['ajency_online_ID']
                                fares['FlightNumberUsedbyIssuer'] = flight['number_flight']
                                fares['AirlineName'] = flight['airline']

                                fares['AdultBaseFare'] = flight['price_final_fare']
                                fares['AdultTotalPrice'] = "{:,}".format(round(int(flight['price_final'])//10,-2))
                                fares['AdultTax'] = flight['price_final'] - flight['price_final_fare']
                                fares['AdultTotalCost'] = flight['price_final']*adultCount

                                fares['ChildBaseFare'] = flight['price_final_chd_fare']
                                fares['ChildTotalFare'] = flight['price_final_chd']
                                fares['ChildTax'] = flight['price_final_chd'] - flight['price_final_chd_fare']
                                fares['ChildTotalCost'] = flight['price_final_chd']*childCount

                                fares['InfantBaseFare'] = flight['price_final_inf_fare']
                                fares['InfantTotalFare'] = flight['price_final_inf']
                                fares['InfantTax'] = flight['price_final_inf'] - flight['price_final_inf_fare']
                                fares['InfantTotalCost'] = flight['price_final_inf']*infantCount

                                filterd_flights_system[index]['Flight_Fare'].append(fares)
                                filterd_flights_system[index]['Flight_Data'][0]['AvailableClasse(s)'].append(class_name)

                    else:
                        Flight['Flight_NUM'] = x[0]
                        x[0] +=1

                        each_flight['Airline'] = flight['iatA_code']
                        each_flight['Type'] = flight['type'].upper()
                        each_flight['Origin'] = flight["from"].upper()
                        each_flight['Destination'] = flight["to"].upper()
                        charter724date = flight['date_flight']
                        each_flight['DepartureDate'] =charter724date
                        chrter724dateshamsi = datetime.strptime(charter724date, "%Y-%m-%d")
                        each_flight['DepartureDateShamsi'] = str(JalaliDate(chrter724dateshamsi))
                        each_flight['DepartureTime'] =flight['time_flight'][:-3]
                        each_flight['ArrivalDate'] = ''
                        each_flight['ArrivalDateShamsi'] = ''
                        each_flight['ArrivalTime'] = ''
                        each_flight['Duration'] =  ''
                        each_flight['FlightNo'] = flight["number_flight"]
                        each_flight['AvailableClasse(s)'] = [class_name]
                        each_flight['ClassType'] = flight['type_flight']
                        each_flight['AircraftTypeCode'] = ''
                        each_flight['AircraftName'] = flight['carrier']

                        fares['CabinClassName'] = class_name
                        fares['AvailableSets'] = str(flight['capacity'])
                        fares['ClassType'] = flight['type'].upper()
                        fares['FareProvider'] = 'ParseOwj Charter 724'
                        fares['IssuerCode'] = flight['ajency_online_ID']
                        fares['FlightNumberUsedbyIssuer'] = flight['number_flight']
                        fares['AirlineName'] = flight['airline']

                        fares['AdultBaseFare'] = flight['price_final_fare']
                        fares['AdultTotalPrice'] = "{:,}".format(round(int(flight['price_final'])//10,-2))
                        fares['AdultTax'] = flight['price_final'] - flight['price_final_fare']
                        fares['AdultTotalCost'] = flight['price_final']*adultCount

                        fares['ChildBaseFare'] = flight['price_final_chd_fare']
                        fares['ChildTotalFare'] = flight['price_final_chd']
                        fares['ChildTax'] = flight['price_final_chd'] - flight['price_final_chd_fare']
                        fares['ChildTotalCost'] = flight['price_final_chd']*childCount

                        fares['InfantBaseFare'] = flight['price_final_inf_fare']
                        fares['InfantTotalFare'] = flight['price_final_inf']
                        fares['InfantTax'] = flight['price_final_inf'] - flight['price_final_inf_fare']
                        fares['InfantTotalCost'] = flight['price_final_inf']*infantCount

                        flight_is_there.append(last3char)
                        flight_is_there_time.append(flighttime)
                        Flight['Flight_Data'].append(each_flight)
                        Flight['Flight_Fare'].append(fares)
                        filterd_flights_system.append(Flight)

                elif flight['type'] == 'charter':

                    if (last3char in flight_is_there_charter) and (flighttime in flight_is_there_time_charter) :
                        index = flight_is_there_charter.index(last3char)
                        index2 = flight_is_there_time_charter.index(flighttime)

                        if index == index2:
                            if filterd_flights_charter[index]['Flight_Data'][0]['Airline'] == flight['iatA_code']:

                                fares['CabinClassName'] = class_name
                                fares['AvailableSets'] = str(flight['capacity'])
                                fares['ClassType'] = flight['type'].upper()
                                fares['FareProvider'] = 'ParseOwj Charter 724'
                                fares['IssuerCode'] = flight['ajency_online_ID']
                                fares['FlightNumberUsedbyIssuer'] = flight['number_flight']
                                fares['AirlineName'] = flight['airline']

                                fares['AdultBaseFare'] = flight['price_final_fare']
                                fares['AdultTotalPrice'] = "{:,}".format(round(int(flight['price_final'])//10,-2))
                                fares['AdultTax'] = flight['price_final'] - flight['price_final_fare']
                                fares['AdultTotalCost'] = flight['price_final']*adultCount

                                fares['ChildBaseFare'] = flight['price_final_chd_fare']
                                fares['ChildTotalFare'] = flight['price_final_chd']
                                fares['ChildTax'] = flight['price_final_chd'] - flight['price_final_chd_fare']
                                fares['ChildTotalCost'] = flight['price_final_chd']*childCount

                                fares['InfantBaseFare'] = flight['price_final_inf_fare']
                                fares['InfantTotalFare'] = flight['price_final_inf']
                                fares['InfantTax'] = flight['price_final_inf'] - flight['price_final_inf_fare']
                                fares['InfantTotalCost'] = flight['price_final_inf']*infantCount

                                filterd_flights_charter[index]['Flight_Fare'].append(fares)
                                filterd_flights_charter[index]['Flight_Data'][0]['AvailableClasse(s)'].append(class_name)

                    else:
                        Flight['Flight_NUM'] = x[0]
                        x[0] +=1


                        each_flight['Airline'] = flight['iatA_code']
                        each_flight['Type'] = flight['type'].upper()
                        each_flight['Origin'] = flight["from"].upper()
                        each_flight['Destination'] = flight["to"].upper()
                        charter724date = flight['date_flight']
                        each_flight['DepartureDate'] =charter724date
                        chrter724dateshamsi = datetime.strptime(charter724date, "%Y-%m-%d")
                        each_flight['DepartureDateShamsi'] = str(JalaliDate(chrter724dateshamsi))
                        each_flight['DepartureTime'] =flight['time_flight'][:-3]
                        each_flight['ArrivalDate'] = ''
                        each_flight['ArrivalDateShamsi'] = ''
                        each_flight['ArrivalTime'] = ''
                        each_flight['Duration'] =  ''
                        each_flight['FlightNo'] = flight["number_flight"]
                        each_flight['AvailableClasse(s)'] = [class_name]
                        each_flight['ClassType'] = flight['type_flight']
                        each_flight['AircraftTypeCode'] = ''
                        each_flight['AircraftName'] = flight['carrier']

                        fares['CabinClassName'] = class_name
                        fares['AvailableSets'] = str(flight['capacity'])
                        fares['ClassType'] = flight['type'].upper()
                        fares['FareProvider'] = 'ParseOwj Charter 724'
                        fares['IssuerCode'] = flight['ajency_online_ID']
                        fares['FlightNumberUsedbyIssuer'] = flight['number_flight']
                        fares['AirlineName'] = flight['airline']

                        fares['AdultBaseFare'] = flight['price_final_fare']
                        fares['AdultTotalPrice'] = "{:,}".format(round(int(flight['price_final'])//10,-2))
                        fares['AdultTax'] = flight['price_final'] - flight['price_final_fare']
                        fares['AdultTotalCost'] = flight['price_final']*adultCount

                        fares['ChildBaseFare'] = flight['price_final_chd_fare']
                        fares['ChildTotalFare'] = flight['price_final_chd']
                        fares['ChildTax'] = flight['price_final_chd'] - flight['price_final_chd_fare']
                        fares['ChildTotalCost'] = flight['price_final_chd']*childCount

                        fares['InfantBaseFare'] = flight['price_final_inf_fare']
                        fares['InfantTotalFare'] = flight['price_final_inf']
                        fares['InfantTax'] = flight['price_final_inf'] - flight['price_final_inf_fare']
                        fares['InfantTotalCost'] = flight['price_final_inf']*infantCount

                        flight_is_there_charter.append(last3char)
                        flight_is_there_time_charter.append(flighttime)
                        Flight['Flight_Data'].append(each_flight)
                        Flight['Flight_Fare'].append(fares)
                        filterd_flights_charter.append(Flight)


    def nira_AvailabilityJS(Airline):
        airlinename = {
            'i3':'ATA',
            'zv':'Zagros'
        }

        datefornira = departureDateShamsi.split("-")
        
        departureDateShamsiDay = datefornira[2]
        departureDateShamsiMonth = datefornira[1]

        requests_cache.install_cache('NiraFareCache', backend='sqlite', expire_after=300)
        fare_req = requests.Session()

        #GETTING URL, PASS AND USER FROM PYTHON DICT IN KEYS.PY
        airline_nira_url = nira_key(Airline,'Availability')+'/AvailabilityJS.jsp'

        airline_nira_fare_url = nira_key(Airline,'Fare')+'/FareJS.jsp'

        #print(f'Airline = {Airline} cbSource = {cbSource} cbTarget = {cbTarget} ')
        #GETTING USER AND PASSWORD
        user = nira_key(Airline,'user')
        password = nira_key(Airline,'password')
        #SETTING PRAAMS
        params = {'cbSource':originLocationCode,'cbTarget':destinationLocationCode,'cbDay1':departureDateShamsiDay,'cbMonth1':departureDateShamsiMonth,'OfficeUser':user,'OfficePass':password}
        #MAKING GET REQUEST
        print(Airline)
        t1 = time.time()
        with requests_cache.disabled():
            res = requests.get(url = airline_nira_url, params = params, timeout=3)

        #CHEACKING THE API RESPONSE
        b = time.time()
       
        if res.status_code != 200:
             
             return res.status_code

        try:
            data = res.json()
        except:
            return 400
        t2 = time.time()
        print(f"the time for {Airline} API is {t2-t1}")

        #LOOPING THROUGH THE FLIGHTS
        for flight in data['AvailableFlights']:

            Flight = {
            'Flight_Data':[],
            'Flight_Fare':[],
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
            #FOR
            flight_is_good = False

            for flight_class in all_classes:
                fares = {}
                class_is_good = False
                #last word inside the str (/WX LX MX OX RX BX DX EX SX TX GX) here would be X for all of them
                class_sets = flight_class[-1]
                if (class_sets != 'X') and (class_sets != 'C'):
                    #this gets the whole class with the number at the end
                    class_name = flight_class[:-1]
                    fares['CabinClassName'] = class_name
                    #if the last chr is 'A' in means more than 9 is available
                    if class_sets == 'A':
                        available_classes.append(class_name)
                        flight_is_good = True
                        class_is_good = True
                        fares['AvailableSets'] = '9+'
                    # else the json has a number at the end to show the available segments
                    #here we are comparing the available sets to the total sets that we need based on the user input
                    elif int(class_sets) >= adultCount + childCount + infantCount:
                                available_classes.append(class_name)
                                flight_is_good = True
                                class_is_good = True
                                fares['AvailableSets'] = class_sets

                    if class_is_good == True:

                        params_fare ={'Route':originLocationCode+'-'+destinationLocationCode,'RBD': class_name,'OfficeUser':user,'OfficePass':password}
                        fare = fare_req.get(url = airline_nira_fare_url, params = params_fare)
                        fare_data = fare.json()

                        fares['ClassType'] = 'SYSTEM'
                        fares['FareProvider'] = 'ParseOwj Nira ZV'
                        fares['IssuerCode'] = 1000
                        fares['FlightNumberUsedbyIssuer'] = flight['FlightNo']

                        fares['AdultBaseFare'] = int(fare_data['AdultFare'])
                        fares['AdultTotalPrice'] = "{:,}".format(int(all_fares[class_name])//10)
                        fares['AdultTax'] = int(all_fares[class_name]) - int(fare_data['AdultFare'])
                        fares['AdultTotalCost'] = int(all_fares[class_name])*adultCount

                        fares['ChildBaseFare'] = int(fare_data['ChildFare'])
                        fares['ChildTotalFare'] = int(fare_data['ChildTotalPrice'])
                        fares['ChildTax'] = int(fare_data['ChildTotalPrice']) - int(fare_data['ChildFare'])
                        fares['ChildTotalCost'] = int(fare_data['ChildTotalPrice'])*childCount

                        fares['InfantBaseFare'] = int(fare_data['InfantFare'])
                        fares['InfantTotalFare'] = int(fare_data['InfantTotalPrice'])
                        fares['InfantTax'] = int(fare_data['InfantTotalPrice']) - int(fare_data['InfantFare'])
                        fares['InfantTotalCost'] = int(fare_data['InfantTotalPrice'])*infantCount
                        fares['AirlineName'] = airlinename[Airline]

                        Flight['Flight_Fare'].append(fares)

            if flight_is_good == True:

                Flight['Flight_Fare'].sort(key=lambda e: e['AdultTotalCost'])

                each_flight = {}

                Flight['Flight_NUM'] = x[0]
                x[0] +=1


                each_flight['Airline'] = flight['Airline']
                each_flight['Type'] = 'SYSTEM'
                each_flight['Origin'] = flight["Origin"]
                each_flight['Destination'] = flight["Destination"]
                departureInfo = datetime.strptime(flight["DepartureDateTime"], '%Y-%m-%d %H:%M:%S')
                arrivalInfo =  datetime.strptime(flight["ArrivalDateTime"],'%Y-%m-%d %H:%M:%S' )
                each_flight['DepartureDate'] =str(departureInfo.date())
                each_flight['DepartureDateShamsi'] = str(JalaliDate(departureInfo.date()))
                each_flight['DepartureTime'] =str(departureInfo.time())[:-3]
                each_flight['ArrivalDate'] = str(arrivalInfo.date())
                each_flight['ArrivalDateShamsi'] = str(JalaliDate(arrivalInfo.date()))
                each_flight['ArrivalTime'] = str(arrivalInfo.time())[:-3]
                each_flight['Duration'] =  str(arrivalInfo - departureInfo)
                each_flight['FlightNo'] = str(flight["FlightNo"])
                each_flight['AvailableClasse(s)'] = available_classes
                each_flight['ClassType'] = 'Economy'
                planeCode = flight["AircraftTypeCode"]
                each_flight['AircraftTypeCode'] = planeCode
                each_flight['AircraftName'] = IATAAircraftTypeCodes(planeCode)
                flight_is_there.append(flight["FlightNo"])
                flight_is_there_time.append(departureInfo.date())
                Flight['Flight_Data'].append(each_flight)
                filterd_flights_system.append(Flight)



    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(nira_AvailabilityJS, 'zv')
        executor.submit(nira_AvailabilityJS, 'i3')
        executor.submit(charter724_searche)





    all = filterd_flights_system + filterd_flights_charter


    all.sort(key=lambda e: e['Flight_Fare'][0]['AdultTotalCost'])
    t3 = time.time()
    print(f" the whole thing = {t3-t1}  ")
    finalflights = {'NumberOfFlights':x[0],'Flights': all}
    return finalflights




'''
filterd_flights = iranflights('thr','mhd','2020-08-02',1)
#print(filterd_flights)

for flight in filterd_flights:
    #print(flight)
    print(f"Flight form {flight['Flight_Data'][0]['Origin']} with {flight['Flight_Data'][0]['Airline']} with cheapest {flight['Flight_Fare'][0]['AdultTotalCost']} class {flight['Flight_Fare'][0]['CabinClassName']} date {flight['Flight_Data'][0]['DepartureTime']}")
    for price in flight['Flight_Fare']:
        print(f"Class{price['CabinClassName'] }at {price['AdultTotalCost']} IssuerCode = {price['IssuerCode']} and {price['FlightNumberUsedbyIssuer']} ")


'''
