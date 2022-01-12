from zeep import Client

def PECsale(UserName,Amount,OrderID,CallBackUrl,SaleInfo=''):
    client = Client(wsdl ='https://pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx?WSDL')
    order_type = client.get_type('ns0:ClientSaleRequestData')
    order = order_type(LoginAccount = UserName,Amount=Amount*10,OrderId=OrderID,CallBackUrl=CallBackUrl,AdditionalData=SaleInfo)
    res = client.service.SalePaymentRequest(requestData=order)
    print(res)
    Token= res['Token']
    Status = res['Status']
    if (Token <= 0) and Status == 0:
        Status = -1111
    
    data = {'Status':Status,'Token':str(Token),'RedirectURL':f'https://pec.shaparak.ir/NewIPG/','RedirectType':'GET', 'RedirectData': {'Token':Token}}
    return data

def PECconfirm(UserName,Token, OrderId,Amount):
    client = Client(wsdl ='https://pec.shaparak.ir/NewIPGServices/Confirm/ConfirmService.asmx?WSDL')
    order_type = client.get_type('ns0:ClientConfirmWithAmountRequestData')
    order = order_type(LoginAccount = UserName, Token = Token, OrderId=OrderId,Amount=2)
    res = client.service.ConfirmPaymentWithAmount(requestData=order)
    print(res)
    Token= res['Token']
    Status = res['Status']
    if (Token <= 0) and Status == 0:
        Status = -1111
    data = {'Status':Status,'Token':str(Token),'ConfirmationNUM':res['RRN'],'CardNumber':res['CardNumberMasked']}
    return data

def PECrefund(UserName, Token):
    client = Client(wsdl ='https://pec.shaparak.ir/NewIPGServices/Reverse/ReversalService.asmx?WSDL')
    order_type = client.get_type('ns0:ClientReversalRequestData')
    order = order_type(LoginAccount = UserName, Token = Token)
    res = client.service.ReversalRequest(requestData=order)
    print(res)
    Token= res['Token']
    Status = res['Status']
    if (Token <= 0) and Status == 0:
        Status = -1111
    data = {'Status':Status,'Token':str(Token)}
    return data

