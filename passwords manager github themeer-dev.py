import json
from cryptography.fernet import Fernet

#  Generate key (only first time run)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

#  Load key
def load_key():
    return open("secret.key", "rb").read()

#  Encrypt password
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

#  Decrypt password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

# 💾 Save password
def save_password():
    website = input("Enter website: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    key = load_key()
    encrypted = encrypt_password(password, key)

    data = {}

    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except:
        pass

    data[website] = {"username": username, "password": encrypted}

    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

    print(" Password saved successfully!")

#  View passwords
def view_passwords():
    key = load_key()

    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)

            for site, info in data.items():
                decrypted = decrypt_password(info['password'], key)
                print(f"\n🌐 Website: {site}")
                print(f"👤 Username: {info['username']}")
                print(f"🔑 Password: {decrypted}")
    except:
        print("❌ No passwords saved yet!")

# 🚀 Main menu
def main():
    if not os.path.exists("secret.key"):
        generate_key()

    while True:
        print("\n--- Password Manager ---")
        print("1. Save Password")
        print("2. View Passwords")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            save_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            break
        else:
            print("❌ Invalid option")

# Run
import os
main()
