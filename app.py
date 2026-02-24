import streamlit as st
import json
from pathlib import Path
import random
import string

# -------------------- BANK CLASS --------------------

class LenaDenaBank:
    database = "lena_dena_data.json"
    data = []

    # Load data
    if Path(database).exists():
        with open(database, "r") as file:
            data = json.load(file)
    else:
        data = []

    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as file:
            json.dump(cls.data, file, indent=4)

    @staticmethod
    def generate_account_number():
        digits = random.choices(string.digits, k=4)
        letters = random.choices(string.ascii_uppercase, k=4)
        acc = digits + letters
        random.shuffle(acc)
        return "".join(acc)

    @classmethod
    def create_account(cls, user_data):
        cls.data.append(user_data)
        cls.save_data()

    @classmethod
    def find_user(cls, acc_no, pin):
        for user in cls.data:
            if user["account_no"] == acc_no and user["pin"] == pin:
                return user
        return None

    @classmethod
    def delete_account(cls, user):
        cls.data.remove(user)
        cls.save_data()


# -------------------- STREAMLIT UI --------------------

st.set_page_config(page_title="Lena Dena Bank", page_icon="🏦")

st.title("🏦 LENA DENA BANK")
st.markdown("### Welcome to Lena Dena Bank Management System")

menu = st.sidebar.selectbox(
    "Select Service",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Update Account",
        "Delete Account",
        "View Account Details"
    ]
)

# -------------------- CREATE ACCOUNT --------------------

if menu == "Create Account":
    st.subheader("📝 Open New Account")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")
    phone = st.text_input("Phone Number (10 digits)")

    if st.button("Create Account"):
        if age > 18 and len(pin) == 4 and len(phone) == 10:
            acc_no = LenaDenaBank.generate_account_number()
            new_user = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "phone": phone,
                "account_no": acc_no,
                "balance": 0
            }
            LenaDenaBank.create_account(new_user)
            st.success(f"✅ Account Created Successfully!")
            st.info(f"Your Account Number: {acc_no}")
        else:
            st.error("❌ Invalid Details (Age must be >18, PIN=4 digits, Phone=10 digits)")

# -------------------- DEPOSIT --------------------

elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        user = LenaDenaBank.find_user(acc, int(pin))
        if user:
            user["balance"] += amount
            LenaDenaBank.save_data()
            st.success("✅ Amount Deposited Successfully")
            st.info(f"Updated Balance: ₹ {user['balance']}")
        else:
            st.error("❌ Invalid Account Number or PIN")

# -------------------- WITHDRAW --------------------

elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        user = LenaDenaBank.find_user(acc, int(pin))
        if user:
            if amount > user["balance"]:
                st.error("❌ Insufficient Balance")
            elif amount > 10000:
                st.error("❌ Withdrawal limit is 10,000 per transaction")
            else:
                user["balance"] -= amount
                LenaDenaBank.save_data()
                st.success("✅ Amount Withdrawn Successfully")
                st.info(f"Remaining Balance: ₹ {user['balance']}")
        else:
            st.error("❌ Invalid Account Number or PIN")

# -------------------- UPDATE ACCOUNT --------------------

elif menu == "Update Account":
    st.subheader("✏ Update Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Load Account"):
        user = LenaDenaBank.find_user(acc, int(pin))
        if user:
            st.session_state.user = user
        else:
            st.error("❌ Invalid Account Number or PIN")

    if "user" in st.session_state:
        user = st.session_state.user

        name = st.text_input("Name", user["name"])
        email = st.text_input("Email", user["email"])
        new_pin = st.text_input("PIN", value=str(user["pin"]), type="password")
        phone = st.text_input("Phone", user["phone"])

        if st.button("Update Now"):
            user["name"] = name
            user["email"] = email
            user["pin"] = int(new_pin)
            user["phone"] = phone
            LenaDenaBank.save_data()
            st.success("✅ Account Updated Successfully")
            del st.session_state.user

# -------------------- DELETE ACCOUNT --------------------

elif menu == "Delete Account":
    st.subheader("🗑 Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete Account"):
        user = LenaDenaBank.find_user(acc, int(pin))
        if user:
            LenaDenaBank.delete_account(user)
            st.success("✅ Account Deleted Successfully")
        else:
            st.error("❌ Invalid Account Number or PIN")

# -------------------- VIEW DETAILS --------------------

elif menu == "View Account Details":
    st.subheader("📄 Account Information")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("View Details"):
        user = LenaDenaBank.find_user(acc, int(pin))
        if user:
            st.success("✅ Account Found")
            st.json(user)
        else:
            st.error("❌ Invalid Account Number or PIN")