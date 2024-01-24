from cart.models import *

def generateOrderIds():
    ORDER_ID = 10000000
    TRACKING_NO = 99999999
    n = Orders.objects.first()
    return f'ORD{ORDER_ID + n.id + 1}', f'DRB{TRACKING_NO + n.id + 1}'

def getDiscounValue(user):
    discount_value = 0
    try:
        userCoupon = UserCoupons.objects.get(user=user, is_active=True)
        userCoupon.is_used = True
        userCoupon.is_active = False
        userCoupon.save()
        discount_value = userCoupon.coupon.coupon_value
        return discount_value
    except:
        return discount_value