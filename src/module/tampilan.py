from tabulate import tabulate

def show_welcome_menu():
    print("========== Selamat Datang Di Toko Si Paling Modern ==========")
    print("=====            SELF CASHIER SYSTEM            =====")
    print("\n Main Menu")
    print("------------")
    print("Sudah memiliki akun?")
    print("1. Login \n2. Register")
    print("======================================================")

def show_transaction_menu():
    print("======================================================")
    print("Silahkan pilih menu dibawah ini")
    print("1. Masukkan barang yang ingin dibeli")
    print("2. Perbarui daftar barang")
    print("3. Hapus barang dari keranjang")
    print("4. Batalkan transaksi")
    print("5. Lihat pesanan")
    print("6. Check out pesanan")
    print("7. Lihat pesanan yang telah di-check out")
    print("8. Keluar dari program")
    print("\n")

def show_order(order: dict):
    table = []
    for item_name, item_info in order.items():
        qty = int(item_info["qty"])
        price = float(item_info["price"])
        total = qty * price
        table.append([item_name, qty, price, total])

    headers = ["Item Name", "Qty", "Price", "Total"]
    print("Order Anda saat ini: ")
    print(tabulate(table, headers = headers, tablefmt="grid"))

def show_checkout_order(order: dict):
    table = []
    for item_name, item_info in order.items():
        qty = int(item_info["qty"])
        price = float(item_info["price"])
        total = float(item_info["total"])
        discount = int(item_info["disc"])
        after_disc = float(item_info["after_disc"])
        table.append([item_name, qty, price, total, discount, after_disc])

    headers = ["Item Name", "Qty", "Price", "Total", "Discount (%)", "Price After Disc"]
    print(tabulate(table, headers = headers, tablefmt="grid"))