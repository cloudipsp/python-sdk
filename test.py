from cloudipsp import Api, Checkout

api = Api(merchant_id=1396424,
          secret_key='test',
          request_type='xml',
          api_protocol='1.0',
          api_domain='api.fondy.eu')  # json - is default
checkout = Checkout(api=api)
data = {
    "preauth": 'Y',
    "currency": "RUB",
    "amount": 10000,
    "reservation_data": {
        'test': 1,
        'test2': 2
    }
}
response = checkout.url(data)
