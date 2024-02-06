
import json
import os

data = {
            "transactions": [
                {
                    "customerId": "fbbe0690-0cd1-48eb-aece-f2744db6f895",
                    "customerName": "Gregory Downs",
                    "transactionId": "7b3c8eee-3689-4cf8-b874-dfbe515d2eb7",
                    "transactionDate": "2022-02-21",
                    "sourceDate": "2022-02-22T21:20:48",
                    "merchantId": 36,
                    "categoryId": 10,
                    "currency": "GBP",
                    "amount": "-1841.11",
                    "description": "Blair-White | Travel"
                },
                {
                    "customerId": "fbbe0690-0cd1-48eb-aece-f2744db6f895",
                    "customerName": "Gregory Downs",
                    "transactionId": "3a05ea6b-acb8-4dfe-847e-470b6502bd54",
                    "transactionDate": "2022-04-03",
                    "sourceDate": "2022-04-03T19:00:23",
                    "merchantId": 64,
                    "categoryId": 3,
                    "currency": "GBP",
                    "amount": "594.59",
                    "description": "Sherman-Love | Shopping"
                },
                {
                    "customerId": "fbbe0690-0cd1-48eb-aece-f2744db6f895",
                    "customerName": "Gregory Downs",
                    "transactionId": "b14a9ac9-c541-4ba9-8bf1-efbaab61d76f",
                    "transactionDate": "2023-11-11",
                    "sourceDate": "2023-11-13T04:00:20",
                    "merchantId": 61,
                    "categoryId": 4,
                    "currency": "GBP",
                    "amount": "-656.25",
                    "description": "Anderson, Thomas and Jimenez | Eating Out"
                }
            ]
       }

# data_test = json.loads(json.dumps(data))

# for x in data_test['transactions']:
#     print(x)