import Config
import requests


class listAllOrders:
    
    endpoint = 'openPositions'
    
    def __init__(self):
        pass
    
    @staticmethod
    def listOrders():
        get_orders = requests.get(Config.url+listAllOrders.endpoint,
                                  headers=Config.headers)
        print("Status Code: "+ str(get_orders.status_code))
        print('\nOrders: {}'.format(get_orders.content))

listAllOrders.listOrders()