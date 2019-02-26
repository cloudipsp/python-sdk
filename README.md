# Cloudipsp Python SDK client

<p align="center">
  <img width="200" height="200" src="https://avatars0.githubusercontent.com/u/15383021?s=200&v=4">
</p>

[![Downloads](https://pepy.tech/badge/cloudipsp)](https://pepy.tech/project/cloudipsp)
[![Downloads](https://pepy.tech/badge/cloudipsp/month)](https://pepy.tech/project/cloudipsp)
[![Downloads](https://pepy.tech/badge/cloudipsp/week)](https://pepy.tech/project/cloudipsp)

## Payment service provider
A payment service provider (PSP) offers shops online services for accepting electronic payments by a variety of payment methods including credit card, bank-based payments such as direct debit, bank transfer, and real-time bank transfer based on online banking. Typically, they use a software as a service model and form a single payment gateway for their clients (merchants) to multiple payment methods. 
[read more](https://en.wikipedia.org/wiki/Payment_service_provider)

Requirements
------------
- Python (2.4, 2.7, 3.3, 3.4, 3.5, 3.6, 3.7)

Dependencies
------------
- requests
- six

Installation
------------
```bash
pip install cloudipsp
```
### Simple start

```python
from cloudipsp import Api, Checkout
api = Api(merchant_id=1396424,
          secret_key='test')
checkout = Checkout(api=api)
data = {
    "currency": "USD",
    "amount": 10000
}
url = checkout.url(data).get('checkout_url')
```

Tests
-----------------
First, install `tox` `<http://tox.readthedocs.org/en/latest/>`

To run testing:

```bash
tox
```

This will run all tests, against all supported Python versions.