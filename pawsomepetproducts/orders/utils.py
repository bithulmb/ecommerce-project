import datetime
from .models import OrderAddress,Order,OrderProduct,Payment


def generate_order_number(order_id):
    yr = int(datetime.date.today().strftime("%Y"))
    dt = int(datetime.date.today().strftime("%d"))
    mt = int(datetime.date.today().strftime("%m"))
    d = datetime.date(yr, mt, dt)
    current_date = d.strftime("%y%m%d")
    order_number = current_date + str(order_id)
    return order_number

def create_order_address(address):
    return OrderAddress.objects.create(
        name=address.name,
        address_line1=address.address_line1,
        address_line2=address.address_line2,
        town=address.town,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        contact_number=address.contact_number,
    )

def create_order(user, order_address, order_total, offer_amount, shipping_charge, total_amount, payment_method, coupon=None, discount=None):
    order = Order.objects.create(
        user=user,
        order_address=order_address,
        order_total=order_total,
        offer_amount=offer_amount,
        shipping_charge=shipping_charge,
        total_amount=total_amount,
        payment_method=payment_method,
        coupon=coupon,
        discount_amount=discount or 0,
    )
    order.order_number = generate_order_number(order.id)
    order.save()
    return order

def create_payment(user, payment_id, payment_method, amount_paid, status):
    return Payment.objects.create(
        user=user,
        payment_id=payment_id,
        payment_method=payment_method,
        amount_paid=amount_paid,
        status=status,
    )

def create_order_products(cart_items, order, payment):
    for item in cart_items:
        variant = item.variant
        offer_price = variant.get_offer_price() * item.quantity
        offer_discount = variant.discount_amount() * item.quantity

        # Calculate coupon discount
        if order.coupon:
            item_percentage = offer_price / (order.order_total - order.offer_amount + order.shipping_charge)
            coupon_discount = order.discount_amount * item_percentage
        else:
            coupon_discount = 0

        final_price = offer_price - coupon_discount

        OrderProduct.objects.create(
            order=order,
            payment=payment,
            product=variant,
            quantity=item.quantity,
            product_price=variant.price,
            offer_discount=offer_discount,
            offer_price=offer_price,
            coupon_discount=coupon_discount,
            final_price=final_price,
        )

        # Reduce stock
        variant.stock -= item.quantity
        variant.save()

