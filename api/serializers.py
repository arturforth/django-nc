from rest_framework import serializers
from api.models import ServiceBill, PaymentTransaction


class ServiceBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBill
        fields = ['barcode', 'service_type', 'service_description', 'due_date', 'amount', 'payment_status']


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ['barcode', 'card_number', 'amount', 'payment_date', 'payment_method']
