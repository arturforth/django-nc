# django-nc

Ejemplos de uso:

Para crear una boleta de pago mediante curl:
  
  curl -X POST -F "barcode=12" -F "service_type=Gas" -F "service_description=METROGAS" -F "due_date=2021-10-10" -F "amount=120.1" localhost:8000/api/bills/
  
Para realizar un pago de una boleta:

  curl -X POST -F "barcode=12" -F "card_number=5555444433332222" -F "amount=120.1" -F "payment_date=2021-10-11" -F "payment_method=credit_card" localhost:8000/api/payments/
  
Para listar los pagos realizados:

  curl -X GET "localhost:8000/api/payments/?start=2021-10-09&end=2021-10-12" | json_pp
  
Para listar boletas filtradas por tipo de servicio:
  
  curl "localhost:8000/api/bills/?q=Gas" | json_pp
  
Para listar boletas sin filtro:

  curl localhost:8000/api/bills/ | json_pp
 
  
