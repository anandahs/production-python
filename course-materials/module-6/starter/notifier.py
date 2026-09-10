from email_service import send_confirmation_email


def process_orders(orders: list[dict]) -> None:
    for order in orders:
        print("Sending confirmation email...")
        try:
            send_confirmation_email(order["order_id"], order["customer_email"], order["total"])
            print("Email sent.")
        except Exception as e:
            print(f"Failed to send email: {e}")
