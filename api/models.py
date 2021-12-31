from django.db import models


class ServiceBill(models.Model):
    barcode = models.IntegerField(primary_key=True)
    service_type = models.CharField(max_length=255)
    service_description = models.CharField(max_length=255)
    due_date = models.DateField()
    amount = models.FloatField()
    payment_status = models.CharField(max_length=10, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ], default='pending')

    class Meta:
        ordering = ['barcode']


class PaymentTransaction(models.Model):
    barcode = models.IntegerField()
    card_number = models.IntegerField(blank=True, null=True)
    amount = models.FloatField()
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=15, choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('cash', 'Cash'),
    ], default='credit_card')
