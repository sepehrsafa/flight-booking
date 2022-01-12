
def amadeus_key(type, method):
    url = None
    key = None
    secret = None
    if type == "test":
        url = "https://test.api.amadeus.com"
        key = "XXXX"
        secret = "XXXX"
        if method == 'Flight_Offers_Search':
            url = url+'/v2/shopping/flight-offers'
        elif method == 'auth':
            url = url+'/v1/security/oauth2/token'

    elif type == "production":
        Url = "api.amadeus.com"
        Key = "XXX"
        secret = "XXX"

    return url, key, secret
def nira_key(airline, method):
    #zagrous airline(ZV)
    zv = {
    'Availability': 'http://zv.nirasoft.ir:882',
    'Fare': 'http://zv.nirasoft.ir:880',
    'Reserve': 'http://book.zagrosairlines.com/cgi-bin/NRSWeb.cgi/ReservJS',
    'ETISSUE': 'http://Book.zagrosairlines.com/cgi-bin/NRSWeb.cgi',
    'CancelPNR': 'http://zv.nirasoft.ir/cgi-bin/NRSWeb.cgi',
    'CancelSeat': 'http://Book.zagrosairlines.com/cgi-bin/NRSWeb.cgi',
    'ETRefund': 'http://Book.zagrosairlines.com/cgi-bin/NRSWeb.cgi',
    'RT': 'http://zv.nirasoft.ir:880/NRSRT.jsp',
    'ETR': 'http://Zv.nirasoftware.com:880',
    'Command': 'http://Book.zagrosairlines.com/cgi-bin/NRSWeb.cgi',
    'user': 'XXX',
    'password': 'XXX'
    }
    i3 = {
    'Availability' : 'http://api.ataair.ir/ws1',
    'Availability Fare': 'http://api.ataair.ir/ws1',
    'Fare': 'http://api.ataair.ir/ws1',
    'Reserve': 'http://api.ataair.ir/ws2/cgi-bin/NRSWeb.cgi/ReservJS',
    'ETISSUE': 'http://api.ataair.ir/ws2/cgi-bin/NRSWEB.cgi',
    'CancelPNR': 'http://api.ataair.ir/ws2/cgi-bin/NRSWEB.cgi',
    'CancelSeat': 'http://api.ataair.ir/ws2/cgi-bin/NRSWEB.cgi',
    'ETRefund': 'http://api.ataair.ir/ws2/cgi-bin/NRSWEB.cgi',
    'RT': 'http://api.ataair.ir/ws1/NRSRT.jsp',
    'ETR': 'http://api.ataair.ir/ws1',
    'Command': 'http://api.ataair.ir/ws2/cgi-bin/NRSWEB.cgi',
    'Penalty': 'http://api.ataair.ir/ws1',
    'penaltyNow': 'http://api.ataair.ir/ws1',
    'user' : 'XXX',
    'password': 'XXX'
    }
    #kish airline (Y9)
    y9 = {
    'Availability' : 'Api.kishair.aero/ws1',
    'Availability Fare': 'Api.kishair.aero/ws1',
    'Fare': 'Api.kishair.aero/ws1',
    'Reserve': 'Api.kishair.aero/ws2/cgi-bin/NRSWEB.cgi',
    'ETISSUE': 'Api.kishair.aero/ws2/cgi-bin/NRSWEB.cgi',
    'CancelPNR': 'Api.kishair.aero/ws2/cgi-bin/NRSWEB.cgi',
    'CancelSeat': 'Api.kishair.aero/ws2/cgi-bin/NRSWEB.cgi',
    'ETRefund': 'Api.kishair.aero/ws2/cgi-bin/NRSWEB.cgi',
    'RT': 'Api.kishair.aero/ws1',
    'ETR': 'Api.kishair.aero/ws1',
    'Command': 'Api.kishair.aero/ws2/cgi-bin/NRSWEB.cgi',
    'Penalty': 'Api.kishair.aero/ws1',
    'penaltyNow': 'Api.kishair.aero/ws1',
    'user' : 'XXX',
    'password': 'XXX'
    }


    if (airline == 'ZV') or (airline == 'zv') :
        return zv[method]
    elif airline == 'y9' :
        return y9[method]
    elif (airline == 'i3') or (airline == 'I3'):
        return i3[method]


def charter724_key(key):
    charter724_base_url = 'http://api.charter725.ir'
    charter724 = {
    'userPassBase64' : '/api/userPassBase64',
    'Login': '/api/Login',
    'showmyip': '/api/showmyip',
    'Airportlist' : '/api/WebService/Airportlist',
    'Available15Days' : '/api/WebService/Available15Days',
    'Available' : '/api/WebService/Available',
    'GetCharge' : '/api/WebService/GetCharge',
    'GetCaptcha' : '/api/WebService/GetCaptcha',
    'Reservation' : '/api/WebService/Reservation',
    'BuyTicket' : '/api/WebService/BuyTicket',
    'PayAndBuyTicket' : '/api/WebService/PayAndBuyTicket',
    'CheckTransaction' : '/api/WebService/CheckTransaction',
    'userPassBase64answer' : "Basic XXX",
    'user' : 'XXX',
    'password' : 'XXX'
    }
    return (charter724_base_url+charter724[key])
