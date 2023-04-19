from sqlalchemy.orm import Session
from ..entity.transaction import Transaction
from .tampilan import show_checkout_order

def ask_item_input():
    while True:
        try:
            item_name = input("1. Masukkan nama barang: ")
            qty = int(input("2. Masukkan jumlah barang yang ingin dipesan: "))
            price = float(input("3. Masukkan harga per barang: "))
            if qty <= 0 or price < 0:
                print("Jumlah harus lebih dari 0 dan harga harus positif.  Mohon ulangi kembali")
            else:
                return item_name, qty, price
        except ValueError:
            print("Masukkan harus berupa angka.  Mohon ulangi kembali")

def add_item(order: dict):
    # Prompt for user input
    item_name, qty, price = ask_item_input()
    if item_name in order:
        print("--- PEMBERITAHUAN: barang sudah ada di keranjang, silahkan update item untuk mengubah detail barang")
    else:
        order[item_name] = {"qty": qty, "price": price}
        print("--- Order telah ditambahkan! ---")
    return order

def update_item_name(order: dict, prev_name: str, new_name: str):
    # Create new dict with the updated item name
    updated_dict = {
        new_name: {
            "qty": order[prev_name]["qty"],
            "price": order[prev_name]["price"]
        }
    }

    # Del previous item and update order with new dict
    del order[prev_name]
    order.update(updated_dict)
    return order

def update_item_qty(order: dict, item_name: str, new_name: str, new_qty: int):
    # Check if the item_name as key has been changed
    if item_name not in order:
        order[new_name]["qty"] = new_qty
    else:
        # If not update using old name
        order[item_name]["qty"] = new_qty
    return order

def update_item_price(order: dict, item_name: str, new_name: str, new_price: float):
    # Check if the item_name as key has been changed
    if item_name not in order:
        order[new_name]["price"] = new_price
    else:
        # If not update using old name
        order[item_name]["price"] = new_price
    return order

def delete_item(order: dict, item_name: str):
    del order[item_name]
    print("===== Barang telah dihapus =====")
    return order

def reset_transaction(order: dict):
    print("===== Transaksi telah dibatalkan. Keranjang Anda kosong =====")    
    return order.clear()

def calculate_total_sum(order: dict):
    for item in order.values():
        qty = item["qty"]
        price = item["price"]
        item_total = qty * price
        item["total"] = item_total
    return order

def calculate_discount(order: dict):
    for item in order.values():
        total = item["total"]
        if total > 500000:
            item["disc"] = 7
        elif total > 300000:
            item["disc"] = 6
        elif total > 200000:
            item["disc"] = 5
        else:
            item["disc"] = 0
    return order
    
def calculate_price_after_discount(order: dict):
    for item in order.values():
        total = item["total"]
        discount = item["disc"]
        price_after_discount = total * (1 - (discount / 100))
        item["after_disc"] = price_after_discount
    return order

def insert_to_database(db: Session, order: dict, user_id: int):
    try:
        for item_name, item in order.items():
            qty = item["qty"]
            price = item["price"]
            total = item["total"]
            discount = item["disc"]
            after_disc = item["after_disc"]
            transaction = Transaction(user_id, item_name, qty,price, total, discount, after_disc)
            db.add(transaction)
            db.commit()
            transaction = db.query(Transaction).filter(Transaction.item_name == item_name).first()
            
            print("============================")
            print("==== Checkout berhasil ! ====")
            print("============================")
    except Exception as e:
        db.rollback()
        raise Exception(f"Gagal melakukan checkout {str(e)}")
        
def check_transaction_checkout(db: Session, customer_id: int):
    checkout_dict = {}
    try:
        trx = db.query(Transaction).filter_by(user_id=customer_id).all()

        for item in trx:
            checkout_dict[item.item_name] = {
                "qty": item.qty,
                "price": item.price,
                "total": item.total,
                "disc": item.disc,
                "after_disc": item.after_disc
            }
    except Exception as e:
        raise e
    
    show_checkout_order(checkout_dict)
