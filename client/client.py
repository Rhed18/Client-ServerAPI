#! C:\Users\USER\Downloads\Dev\client\.venv\Scripts\python.exe
import sys
import requests

url = "http://127.0.0.1:8000"


def order(args):
    print("Create Order")

    try:
        customer = args[1]
        bw = int(args[2])
        color = int(args[3])
        photo = int(args[4])
    except:
        print("Usage: order <customer> <bw_pages> <color_pages> <photo_pages>")
        return

    data = {
        "customer": customer,
        "bw_pages": bw,
        "color_pages": color,
        "photo_pages": photo
    }

    response = requests.post(f"{url}/orders", json=data)

    if response.status_code == 200:
        res = response.json()
        print(f"Order Created! ID: {res['id']}")
        print(f"Total Cost: {res['total']}")
    else:
        print("Failed to create order.")
        print(response.text)


def search(args):
    print("Searching for order...")

    try:
        order_id = args[1]
    except:
        print("Usage: search <order_id>")
        return

    response = requests.get(f"{url}/orders/{order_id}")

    if response.status_code == 200:
        order = response.json()
        print(f"ID: {order['id']}")
        print(f"Customer: {order['customer']}")
        print(f"BW Pages: {order['bw_pages']}")
        print(f"Color Pages: {order['color_pages']}")
        print(f"Photo Pages: {order['photo_pages']}")
        print(f"Total: {order['total']}")
        print(f"Status: {order['status']}")
    else:
        print("Order not found.")


def view():
    print("All Orders")

    response = requests.get(f"{url}/orders")

    if response.status_code == 200:
        orders = response.json()
        for order in orders:
            print(f"\nID: {order['id']} | Customer: {order['customer']}")
            print(f"BW: {order['bw_pages']} | Color: {order['color_pages']} | Photo: {order['photo_pages']}")
            print(f"Total: {order['total']} | Status: {order['status']}")
    else:
        print("Failed to retrieve orders.")


def complete_order(args):
    print("Completing Order")

    try:
        order_id = args[1]
    except:
        print("Usage: complete_order <order_id>")
        return

    response = requests.put(f"{url}/orders/{order_id}/complete")

    if response.status_code == 200:
        print("Order marked as completed!")
    else:
        print("Failed to complete order.")


def main():
    if len(sys.argv) < 2:
        print("Commands: order, search, view, complete_order")
        return

    cmd = sys.argv[1]

    if cmd == "order":
        order(sys.argv[1:])

    elif cmd == "search":
        search(sys.argv[1:])

    elif cmd == "view":
        view()

    elif cmd == "complete_order":
        complete_order(sys.argv[1:])

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()