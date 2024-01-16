from cart.models import *

def generateOrderIds():
    ORDER_ID = 10000000
    TRACKING_NO = 99999999
    n = Orders.objects.count()
    return f'ORD{ORDER_ID + n + 1}', f'DRB{TRACKING_NO + n +1}'