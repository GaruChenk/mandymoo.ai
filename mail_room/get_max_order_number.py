from mail_room.email_moogent import get_orders

def get_max_order_number():
    orders = get_orders()
    order_numbers = [order.order_number for order in orders]
    max_order_number = max(order_numbers)
    return max_order_number

if __name__ == "__main__":
    max_order_number = get_max_order_number()
    with open('mail_room/last_order_number.txt', 'w') as file:
        file.write(str(max_order_number))
    print(f"The maximum order number is: {max_order_number}")