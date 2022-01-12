from keys import charter724_key,nira_key
from tokens import charter724_Token
import requests
def captcha724(originLocationCode,destinationLocationCode,departureDate,departureTime,flightNum,source,airlineName,airlineIATAcode):

    if int(source) == 1000:
        flightNum = airlineIATAcode.upper()+flightNum
        source = 446

    charter724token = charter724_Token()


    json  = { "from_flight": originLocationCode, "to_flight": destinationLocationCode, "date_flight": departureDate, 'time_flight':departureTime, 'number_flight':flightNum,'ajency_online_ID':int(source),'airline':airlineName}
    header = {"Content-Type": "application/json-patch+json",'Authorization':charter724token}


    res = requests.post(url = charter724_key('GetCaptcha'), headers = header, json = json)
    print(res.text)
    if res.status_code != 200:
        captchajsonfake = {
        'captchacode':'1234',
        'captchaurl':'pt.ca'
        }
        #return res.status_code
        return captchajsonfake

    print(res.text)

    data = res.json()
    captchajson = {
        'captchacode':data['data']['id_request'],
        'captchaurl':data['data']['link_captcha']
    }

    return captchajson


