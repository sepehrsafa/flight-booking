from keys import amadeus_key,charter724_key
import requests
from app1.models import tokens
from datetime import datetime, timedelta
import pytz  

def amadeus_Token(type):
    if type == 'test':
        urlInfo = amadeus_key(type,'auth')
    elif type == 'production':
        urlInfo = amadeus_key(type, 'auth')
    url = urlInfo[0]
    key = urlInfo[1]
    secret = urlInfo[2]
    data = {"grant_type":"client_credentials","client_id":key,"client_secret":secret}
    res = requests.post(url = url ,data=data)
    if res.status_code != 200:
         return status_code
    else:
        res = res.json()
        token = "Bearer " +res['access_token']
        return token

def charter724_Token():
    tokenobject = tokens.objects.filter(pk=2)
    now = datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc) 
    if tokenobject.first().ValidTo < now:
        url = charter724_key('Login')
        userPassBase64 = charter724_key('userPassBase64answer')
        data = {'userPassBase64': userPassBase64}
        head = {"Content-Type": "application/json-patch+json"}
        res = requests.post(url = url, headers= head, json = data)
        data = res.json()
        token = data['data']['access_token']
        tokentype = data['data']['token_type']
        finaltoken =  tokentype+" "+token
        now = datetime.utcnow()
        now = now.replace(tzinfo=pytz.utc) 
        onehour = now + timedelta(hours=1)
        tokenobject.update(ValidTo=onehour,Token=finaltoken,TimeRecived=now)
        return finaltoken
    else:
        return tokenobject.first().Token


    
if __name__ == '__main__':

    charter724_Token()
