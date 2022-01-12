from zeep import Client
from datetime import datetime
def mellat (Username,Password,TerminalID,OrderID,Amount,CallBackUrl,PhoneNumber='0',SaleInfo='',CartItem=''):
    client = Client(wsdl ='https://bpm.shaparak.ir/pgwchannel/services/pgw?wsdl')
    localdate = datetime.date(datetime.now()).strftime("%Y%m%d")
    localtime = datetime.time(datetime.now()).strftime("%H%M%S")
    res = client.service.bpPayRequest(int(TerminalID),Username, Password, OrderID, Amount, localdate,  localtime, SaleInfo,  CallBackUrl,  "0")
    print(res)
    res = res.split(",")
    if int(res[0]) == 0:
        PhoneNumber = '98'+PhoneNumber[1:]
        return {"Status":0,"Token":res[1],"RedirectURL":f"https://bpm.shaparak.ir/pgwchannel/startpay.mellat","RedirectType":"POST", "RedirectData": {"RefId":str(res[1]), "MobileNo":PhoneNumber,"CartItem":CartItem}}

    
    
def mellatverify(Username,Password,TerminalID,OrderID,SaleReferenceId):
    client = Client(wsdl ='https://bpm.shaparak.ir/pgwchannel/services/pgw?wsdl')
    res = client.service.bpVerifyRequest(int(TerminalID),Username, Password, OrderID, OrderID, int(SaleReferenceId))
    return {'status':int(res)}

def mellatsettel(Username,Password,TerminalID,OrderID,saleReferenceId):
    client = Client(wsdl ='https://bpm.shaparak.ir/pgwchannel/services/pgw?wsdl')
    res = client.service.bpSettleRequest(int(TerminalID),Username, Password, OrderID, OrderID,int(saleReferenceId))
    return {'status':int(res)}










