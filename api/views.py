from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from api.models import ServiceBill, PaymentTransaction
from api.serializers import ServiceBillSerializer, PaymentTransactionSerializer


@api_view(['GET', 'POST'])
def list_bills(request, format=None):
    if request.method == 'GET':
        query = request.GET.get('q', None)
        queryset = ServiceBill.objects.filter(payment_status='pending')
        if query is not None:
            queryset = queryset.filter(service_type__icontains=query).order_by('barcode')
            serializer = ServiceBillSerializer(queryset, many=True)
            for item in serializer.data:
                item.pop('service_type')
        else:
            serializer = ServiceBillSerializer(queryset, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ServiceBillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_bill(request, pk, format=None):
    try:
        bill = ServiceBill.objects.get(pk=pk)
    except ServiceBill.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceBillSerializer(bill)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = ServiceBillSerializer(bill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        bill.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_payment(request, id, format=None):
    try:
        payment = PaymentTransaction.objects.get(barcode=id)
    except PaymentTransaction.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentTransactionSerializer(payment)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = PaymentTransactionSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        payment.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def list_payments(request, format=None):
    if request.method == 'GET':
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        payments = PaymentTransaction.objects.filter(payment_date__range=[start, end])
        serializer = PaymentTransactionSerializer(payments, many=True)

        days = {}
        for payment in serializer.data:
            date = payment['payment_date']
            amount = payment['amount']
            if date in days:
                days[date] += amount
            else:
                days[date] = amount
        return Response(days)

    elif request.method == 'POST':
        serializer = PaymentTransactionSerializer(data=request.data)
        if serializer.is_valid():
            barcode = request.data['barcode']
            bill = ServiceBill.objects.filter(barcode=barcode)
            bill_status = ServiceBill.objects.get(barcode=barcode).payment_status
            if bill is not None and bill_status != 'paid':
                bill.update(payment_status='paid')
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

