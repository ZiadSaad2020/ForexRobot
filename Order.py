import requests
import Config
import json
import pandas as pd

headers = {'Authorization' : 'Bearer ' + Config.api_token}

body = {
  "order": {
    "units": "100",
    "instrument": "USD_CAD",
    "timeInForce": "FOK",
    "type": "MARKET",
    "positionFill": "DEFAULT"
  }
}

send_order = requests.post(Config.order_url,headers=headers,json=body)

response = json.loads((send_order).content.decode('utf-8'))

response_df = pd.DataFrame(response['orderCreateTransaction'],index=[0])

print("Status code: {}".format(send_order.status_code))

print(response_df)