import requests
from keys import charter724_key
import persian
from persiantools.jdatetime import JalaliDate
from datetime import datetime, date
import time
t1 = time.time()


url = 'http://api.charter725.ir/api/Login'
data = {'userPassBase64':"XXXX"}
head = {"Content-Type": "application/json-patch+json"}
res = requests.post(url = url, headers= head, json = data)
print(res)
print(res.text)
data = res.json()
token = data['data']['access_token']
type = data['data']['token_type']
ntoken =  type+" "+token
t2 = time.time()


def charter724_searche(from_flight, to_flight, date_flight, cbAdultQty = '1', cbChildQty = '0', cbInfantQty = '0'):

    json  = { "from_flight": from_flight, "to_flight": to_flight, "date_flight": date_flight}

    header = {"Content-Type": "application/json-patch+json",'Authorization':ntoken}

    res = requests.post(url = charter724_key('Available'), headers = header, json = json)

    if res.status_code != 200:
         return res.status_code

    data = res.json()
    filterd_flights = {'Flights':[]}

    flight_is_there = []
    flight_is_there_time = []

    for flight in data['data']:

        Flight = {
        'Flight_Data':[],
        'Flight_Fare':[],
        'Flight_Rule':{},
        }


        niraflight=['W5']
        if flight['price_final'] != 0:
            if flight['iatA_code'] not in niraflight or (flight['iatA_code'] in niraflight and flight['type'] == 'charter'):
                if flight['capacity'] >= int(cbAdultQty)+int(cbChildQty)+int(cbInfantQty):

                    last3char = flight['number_flight'][-3:]
                    flighttime = flight['time_flight']
                    print(last3char)

                    if (last3char in flight_is_there) and (flighttime in flight_is_there_time) :
                        index = flight_is_there.index(last3char)
                        index2 = flight_is_there_time.index(flighttime)
                        print(index)
                        if index == index2:
                            if filterd_flights['Flights'][index]['Flight_Data'][0]['Airline'] == flight['iatA_code']:
                                fares = {}
                                class_name = flight['cabinclass']
                                if class_name == '':
                                    class_name = 'Y'
                                fares['CabinClassName'] = class_name
                                fares['ClassType'] = flight['type'].upper()
                                fares['FareProvider'] = 'ParseOwj Charter 724'
                                fares['IssuerCode'] = flight['ajency_online_ID']
                                fares['FlightNumberUsedbyIssuer'] = flight['number_flight']
                                fares['AvailableSets'] = str(flight['capacity'])
                                fares['AdultBaseFare'] = flight['price_final_fare']
                                fares['AdultTotalPrice'] = flight['price_final']
                                fares['AdultTax'] = flight['price_final'] - flight['price_final_fare']
                                fares['AdultTotalCost'] = flight['price_final']*int(cbAdultQty)

                                fares['ChildBaseFare'] = flight['price_final_chd_fare']
                                fares['ChildTotalFare'] = flight['price_final_chd']
                                fares['ChildTax'] = flight['price_final_chd'] - flight['price_final_chd_fare']
                                fares['ChildTotalCost'] = flight['price_final_chd']*int(cbChildQty)

                                fares['InfantBaseFare'] = flight['price_final_inf_fare']
                                fares['InfantTotalFare'] = flight['price_final_inf']
                                fares['InfantTax'] = flight['price_final_inf'] - flight['price_final_inf_fare']
                                fares['InfantTotalCost'] = flight['price_final_inf']*int(cbInfantQty)


                                filterd_flights['Flights'][index]['Flight_Fare'].append(fares)




                    else:
                        flight_is_there.append(last3char)
                        flight_is_there_time.append(flighttime)

                        each_flight = {}
                        fares = {}

                        each_flight['Airline'] = flight['iatA_code']
                        each_flight['Type'] = flight['type'].upper()

                        each_flight['Origin'] = flight["from"].upper()
                        each_flight['Destination'] = flight["to"].upper()

                        each_flight['DepartureDate'] =flight['date_flight']
                        tim = flight['date_flight']

                        #each_flight['DepartureDateShamsi'] = str(JalaliDate(tim))
                        each_flight['DepartureTime'] =flight['time_flight']
                        each_flight['ArrivalDate'] = ''
                        each_flight['ArrivalDateShamsi'] = ''
                        each_flight['ArrivalTime'] = ''
                        each_flight['Duration'] =  ''
                        each_flight['FlightNo'] = flight["number_flight"]
                        each_flight['ClassType'] = flight['type_flight']
                        #each_flight['AvailableClasse(s)'] = available_classes
                        each_flight['AircraftTypeCode'] = ''
                        each_flight['AircraftName'] = flight['carrier']

                        Flight['Flight_Data'].append(each_flight)

                        class_name = flight['cabinclass']

                        if class_name == '':
                            class_name = 'Y'
                        fares['CabinClassName'] = class_name
                        fares['ClassType'] = flight['type'].upper()
                        fares['FareProvider'] = 'ParseOwj Charter 724'
                        fares['IssuerCode'] = flight['ajency_online_ID']
                        fares['FlightNumberUsedbyIssuer'] = flight['number_flight']
                        fares['AvailableSets'] = str(flight['capacity'])
                        fares['AdultBaseFare'] = flight['price_final_fare']
                        fares['AdultTotalPrice'] = flight['price_final']
                        fares['AdultTax'] = flight['price_final'] - flight['price_final_fare']
                        fares['AdultTotalCost'] = flight['price_final']*int(cbAdultQty)

                        fares['ChildBaseFare'] = flight['price_final_chd_fare']
                        fares['ChildTotalFare'] = flight['price_final_chd']
                        fares['ChildTax'] = flight['price_final_chd'] - flight['price_final_chd_fare']
                        fares['ChildTotalCost'] = flight['price_final_chd']*int(cbChildQty)

                        fares['InfantBaseFare'] = flight['price_final_inf_fare']
                        fares['InfantTotalFare'] = flight['price_final_inf']
                        fares['InfantTax'] = flight['price_final_inf'] - flight['price_final_inf_fare']
                        fares['InfantTotalCost'] = flight['price_final_inf']*int(cbInfantQty)

                        Flight['Flight_Fare'].append(fares)
                        filterd_flights['Flights'].append(Flight)







        airline = flight['airline']
        time = flight["time_flight"]
        price_Markup = flight['price_Markup']
        share_Sale = flight['share_Sale']
        cla = flight['cabinclass']
        flightnum = flight['number_flight']
        type = flight['type']
        ag = flight['ajency_online_ID']
        airline_code = flight['iatA_code']

        price_final = flight['price_final']
        if flight['type'] == 'charter':
            price = flight['price_final_fare']
        else:
            price = flight["price_final"]
        print(f'Flight with = {airline} at = {time} final price for us = {price} price_Markup = {price_Markup} share_Sale = {share_Sale} site_price = {price_final} claas {cla} flight {flightnum} with {airline_code} type {type} ID {ag}')

    print('gggg')

    return filterd_flights
