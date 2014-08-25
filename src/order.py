import json
import httphandler

class Order:
    def __init__(self, conID, isAsk, quantity, price):
        self.conID = conID
        self.isAsk = isAsk
        self.quantity = quantity
        self.price = price
    def __repr__(self):
        return order2str(self)
        

# Orders[] -> Str
def order2str(listOfOrders):
    listOfjson = []
    for order in listOfOrders:
        json_obj = {'ContractId': order.conID,
                    'isAsk': order.isAsk,
                    'Quantity': order.quantity,
                    'Price': order.price}
        listOfjson.append(json_obj)
    json_str = json.dumps(listOfjson, indent=1, separators=(',',':'))
    return json_str


# implement multi cancel orders (how? should order ID be in order?

# Strings[] -> Str
def cancel2str(listOfCancels):
    listOfjson = []
    for string in listOfCancels:
        json_obj = {'Id': string}
        listOfjson.append(json_obj)
    json_str = json.dumps(listOfjson, indent=1, separators=(',',':'))
    return json_str
