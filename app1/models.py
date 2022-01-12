from django.db import models
from django.utils import timezone

class sale(models.Model):
    OrderNumber = models.AutoField(primary_key=True)
    OrderTime = models.DateTimeField(auto_now_add=True)
    NumberofTickets = models.IntegerField()
    TotalPrice = models.IntegerField()
    TotalReturnPrice = models.IntegerField(default=0)
    PNR = models.CharField(max_length=25,blank=True)
    RequestID = models.CharField(max_length=25, blank=True)
    FaktorID = models.CharField(max_length=25, blank=True)
    

class flightdata(models.Model):
    FlightNumber  = models.CharField(max_length=10)
    FlightDepartureDataTime = models.DateTimeField()
    FlightProvider = models.CharField(max_length=10)
    FlightType = models.CharField(max_length=7)
    FlightAirline = models.CharField(max_length=10)
    FlightOriginAirport= models.CharField(max_length=3)
    FlightOriginTerminal= models.CharField(max_length=3,blank=True)
    FlightDestinationAirport= models.CharField(max_length=3)
    FlightDestinationTerminal= models.CharField(max_length=3,blank=True)
    OrderNumber = models.ForeignKey(sale, on_delete=models.CASCADE, related_name="flightdata",db_column="OrderNumber")

class passenger(models.Model):
    PassengerID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Type = models.CharField(max_length=7)
    IDNumber = models.CharField(max_length=50)
    IDEXP = models.DateField(null=True,blank=True)
    Status = models.CharField(max_length=10)
    TicketNumber = models.CharField(max_length=200)
    OrderNumber = models.ForeignKey(sale, on_delete=models.CASCADE, related_name="passenger",db_column="OrderNumber")

class passengerprice(models.Model):

    TicketBaseFare = models.BigIntegerField()
    TicketCommison = models.BigIntegerField()
    TicketTotalPrice = models.BigIntegerField()
    passenger = models.ForeignKey(passenger, on_delete=models.CASCADE, related_name="passengerprice",db_column="PassengerID")

class ipginfo(models.Model):
    IPGID = models.AutoField(primary_key=True)
    IPGName = models.CharField(max_length=50)
    Provider = models.CharField(max_length=5)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50,blank=True)
    TerminalID = models.CharField(max_length=50)
    AccountNumber = models.CharField(max_length=50)
    AccountBank =  models.CharField(max_length=50)
    AccountName = models.CharField(max_length=50)
    CallBackURL = models.CharField(max_length=50)
    def __str__(self):
        return f'ID: {self.IPGID} - Provider: {self.Provider} - Name: {self.IPGName} - BankInfo: {self.AccountBank} ({self.AccountNumber})'
    
class transaction(models.Model):
    OrderTime = models.DateTimeField(auto_now_add=True)
    TransactionID = models.AutoField(primary_key=True)
    Token = models.CharField(max_length=30,blank=True)
    IPGTransactionReferenceID = models.CharField(max_length=30, blank=True)
    CardNumber =models.CharField(max_length=20, blank=True)
    GatewayInfo = models.ForeignKey(ipginfo, on_delete=models.CASCADE, related_name="transaction",db_column="IPGID")
    AmountRecived = models.IntegerField(default=0)
    AmountReturned = models.IntegerField(default=0)
    OrderNumber = models.ForeignKey(sale, on_delete=models.CASCADE, related_name="transaction",db_column="OrderNumber")


class irantrainstations(models.Model):
    StationCode = models.IntegerField(blank=True)
    StationNameFarsi2 = models.CharField(max_length=50,blank=True)
    StationNameFarsi = models.CharField(max_length=50,blank=True)
    StationNameEnglish = models.CharField(max_length=50,blank=True)
    TelephoneCode = models.CharField(max_length=15,blank=True)
    def __str__(self):
        return f'ID: {self.pk} Station ID: {self.StationCode} - Farsi Name: {self.StationNameFarsi} - English Name: {self.StationNameEnglish}'
    

class tokens(models.Model):
    Name = models.CharField(max_length=30)
    Token = models.CharField(max_length=1000)
    TimeRecived = models.DateTimeField(auto_now=True)
    ValidTo = models.DateTimeField()




    










