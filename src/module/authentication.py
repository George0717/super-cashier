from sqlalchemy.orm import Session
from typing import Optional
from ..entity.user import User

def register(db: Session):
  
      # Validate user input
    is_input_valid = False
    while not is_input_valid:
        # Take user input
        name = input("Siapa nama Anda? ")
        email = input("Masukkan email: ")
        password = input("Masukkan password (Min.6 Karakter):  ")

        # Call function to validate input
        is_input_valid = validate_input(email, password, name, input_ctx="register")

    user = User(email, name, password)
    db.add(user)
    db.commit()

    print("Anda telah berhasil terdaftar.  Silahkan masuk")
    login(db)
    

def login(db: Session):

    # Validate user input
    is_input_valid = False
    while not is_input_valid:
        # Take user input
        email = input("Masukkan email: ")
        password = input("Masukkan password (min 6 karakter): ")        

        # Call function to validate input
        is_input_valid = validate_input(email, password, input_ctx="login")
    
    # Check if user in database
    user = db.query(User).filter(User.email == email, User.password == password).first()
    if user:
        print("======================================================")
        print(f"{user.welcome_user()}")
        return user
    else:
        print("Email atau Password Anda salah. Silahkan coba lagi")
        login(db)  # recursive call if login fails

        
def validate_input(email: str, password: str, name: Optional[str] = None, input_ctx: Optional[str] = None) -> bool:

    if input_ctx == "register":
        if not email or not name or not password:
            print("Semua data harus diisi. Mohon ulangi")
            return False
        if len(name) > 30:
            print("Nama tidak boleh lebih dari 30 karakter")
            return False
    else:
        if not email or not password:
            print("Semua data harus diisi. Mohon ulangi")
            return False

    if len(email) > 50:
        print("Email tidak boleh lebih dari 50 karakter")
        return False
    
    if not "@" in email or not "." in email:
        print("Format e-mail tidak valid")
        return False
    
    if len(password) < 6 or len(password) > 25:
        print("RROR: Password minimal 6 karakter dan maksimal 25 karakter")
        return False

    return True