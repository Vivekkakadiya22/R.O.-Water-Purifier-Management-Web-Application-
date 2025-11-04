from django import template

register=template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(pro_id,cart):
    keys=cart.keys()
    for id in keys:
        if id == 'null':
            continue
        if id is not None:
            id1=int(id)
            print("cart id = ",int(id1), pro_id.id)
            # print(type(id1),type(pro_id.id))
            if id1==pro_id.id:
                return True
    return False

# @register.filter(name='cart_quantity')
# def cart_quantity(pro_id, cart):
#     for id_str, quantity in cart.items():
#         if id_str is not None and id_str != 'null':
#             id1 = int(id_str)
#             if id1 == pro_id.id:
#                 print("id=", quantity)
#                 return quantity

#     return 0

@register.filter(name='cart_quantity')
def cart_quantity(pro_id, cart):
    for id_str, quantity in cart.items():
        if id_str is not None and id_str.lower() != 'null':
            try:
                id1 = int(id_str)
            except ValueError:
                # Handle the case when id_str is not a valid integer
                continue

            if id1 == pro_id.id:
                print("id=", quantity)
                return quantity

    return 0

@register.filter(name='price_total')
def price_total(pro_id, cart):
    return pro_id.price * cart_quantity(pro_id,cart)

@register.filter(name='total_cart_price')
def total_cart_price(products,cart):
    sum=0
    for p in products:
        sum+=price_total(p,cart)
    return sum
