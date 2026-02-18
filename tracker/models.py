from django.db import models

# Create your models here.


class Current_balance(models.Model):
    balance=models.FloatField(default=0)

    



class TrackingHistory(models.Model):
    current_balance=models.ForeignKey(Current_balance,on_delete=
                            models.CASCADE )
    amount=models.FloatField()
    expenses_type=models.CharField(choices=(('CREDIT','CREDIT'),('DEBIT','DEBIT')),max_length=100) 
    description=models.CharField(max_length=250)
    created_at=models.DateTimeField(auto_now_add=True)
    category=models.CharField(max_length=100)
