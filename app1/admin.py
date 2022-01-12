from django.contrib import admin
from .models import sale, flightdata,passenger,passengerprice,transaction,ipginfo,irantrainstations,tokens

admin.site.register(sale)
admin.site.register(flightdata)
admin.site.register(passenger)
admin.site.register(passengerprice)
admin.site.register(transaction)
admin.site.register(ipginfo)
admin.site.register(irantrainstations)
admin.site.register(tokens)