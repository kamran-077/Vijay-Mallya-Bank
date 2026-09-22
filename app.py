import streamlit as st
import json
import hashlib
from pathlib import Path
import random
import string

# -------------------- BANK CLASS --------------------

class VijayMallyaBank:
    database = "VijayMallyaBank.json"
    data = []

    # Load data
    if Path(database).exists():
        with open(database, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as file:
            json.dump(cls.data, file, indent=4)

    @staticmethod
    def hash_pin(pin: str) -> str:
        return hashlib.sha256(pin.encode()).hexdigest()

    @classmethod
    def generate_account_number(cls):
        existing = {user["account_no"] for user in cls.data}
        while True:
            digits = random.choices(string.digits, k=4)
            letters = random.choices(string.ascii_uppercase, k=4)
            acc = digits + letters
            random.shuffle(acc)
            acc_no = "".join(acc)
            if acc_no not in existing:
                return acc_no

    @classmethod
    def create_account(cls, user_data):
        cls.data.append(user_data)
        cls.save_data()

    @classmethod
    def find_user(cls, acc_no, pin):
        hashed = cls.hash_pin(pin)
        for user in cls.data:
            if user["account_no"] == acc_no and user["pin"] == hashed:
                return user
        return None

    @classmethod
    def delete_account(cls, user):
        cls.data.remove(user)
        cls.save_data()


# -------------------- HELPERS --------------------

def get_valid_pin(pin_input: str):
    """Return the pin string if it's exactly 4 digits, else None."""
    if pin_input.isdigit() and len(pin_input) == 4:
        return pin_input
    return None


# -------------------- STREAMLIT UI --------------------

st.set_page_config(page_title="VijayMallyaBank", page_icon="🏦")

st.title("🏦 VijayMallyaBank")
st.markdown("### Welcome to VijayMallyaBank Management System")

menu = st.sidebar.selectbox(
    "Select Service",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Update Account",
        "Delete Account",
        "View Account Details",
    ],
)

# -------------------- CREATE ACCOUNT --------------------

if menu == "Create Account":
    st.subheader("📝 Open New Account")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password", max_chars=4)
    phone = st.text_input("Phone Number (10 digits)", max_chars=10)

    if st.button("Create Account"):
        valid_pin = get_valid_pin(pin)
        errors = []

        if not name.strip():
            errors.append("Name is required")
        if age < 18:
            errors.append("Age must be 18 or older")
        if "@" not in email or "." not in email:
            errors.append("Enter a valid email")
        if valid_pin is None:
            errors.append("PIN must be exactly 4 digits")
        if not (phone.isdigit() and len(phone) == 10):
            errors.append("Phone number must be exactly 10 digits")

        if errors:
            st.error("❌ " + " | ".join(errors))
        else:
            acc_no = VijayMallyaBank.generate_account_number()
            new_user = {
                "name": name.strip(),
                "age": age,
                "email": email.strip(),
                "pin": VijayMallyaBank.hash_pin(valid_pin),
                "phone": phone,
                "account_no": acc_no,
                "balance": 0,
            }
            VijayMallyaBank.create_account(new_user)
            st.success("✅ Account Created Successfully!")
            st.info(f"Your Account Number: {acc_no}")

# -------------------- DEPOSIT --------------------

elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount", min_value=1, step=1)

    if st.button("Deposit"):
        valid_pin = get_valid_pin(pin)
        if valid_pin is None:
            st.error("❌ PIN must be exactly 4 digits")
        else:
            user = VijayMallyaBank.find_user(acc, valid_pin)
            if user:
                user["balance"] += amount
                VijayMallyaBank.save_data()
                st.success("✅ Amount Deposited Successfully")
                st.info(f"Updated Balance: ₹ {user['balance']}")
            else:
                st.error("❌ Invalid Account Number or PIN")

# -------------------- WITHDRAW --------------------

elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount", min_value=1, step=1)

    if st.button("Withdraw"):
        valid_pin = get_valid_pin(pin)
        if valid_pin is None:
            st.error("❌ PIN must be exactly 4 digits")
        else:
            user = VijayMallyaBank.find_user(acc, valid_pin)
            if user:
                if amount > user["balance"]:
                    st.error("❌ Insufficient Balance")
                elif amount > 10000:
                    st.error("❌ Withdrawal limit is 10,000 per transaction")
                else:
                    user["balance"] -= amount
                    VijayMallyaBank.save_data()
                    st.success("✅ Amount Withdrawn Successfully")
                    st.info(f"Remaining Balance: ₹ {user['balance']}")
            else:
                st.error("❌ Invalid Account Number or PIN")

# -------------------- UPDATE ACCOUNT --------------------

elif menu == "Update Account":
    st.subheader("✏ Update Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)

    if st.button("Load Account"):
        valid_pin = get_valid_pin(pin)
        if valid_pin is None:
            st.error("❌ PIN must be exactly 4 digits")
        else:
            user = VijayMallyaBank.find_user(acc, valid_pin)
            if user:
                st.session_state.user = user
            else:
                st.error("❌ Invalid Account Number or PIN")

    if "user" in st.session_state:
        user = st.session_state.user

        st.markdown("---")
        name = st.text_input("Name", user["name"])
        email = st.text_input("Email", user["email"])
        new_pin = st.text_input(
            "New PIN (leave blank to keep current)", type="password", max_chars=4
        )
        phone = st.text_input("Phone", user["phone"], max_chars=10)

        if st.button("Update Now"):
            errors = []
            if not name.strip():
                errors.append("Name is required")
            if "@" not in email or "." not in email:
                errors.append("Enter a valid email")
            if not (phone.isdigit() and len(phone) == 10):
                errors.append("Phone number must be exactly 10 digits")
            if new_pin and get_valid_pin(new_pin) is None:
                errors.append("New PIN must be exactly 4 digits")

            if errors:
                st.error("❌ " + " | ".join(errors))
            else:
                user["name"] = name.strip()
                user["email"] = email.strip()
                user["phone"] = phone
                if new_pin:
                    user["pin"] = VijayMallyaBank.hash_pin(new_pin)
                VijayMallyaBank.save_data()
                st.success("✅ Account Updated Successfully")
                del st.session_state.user

# -------------------- DELETE ACCOUNT --------------------

elif menu == "Delete Account":
    st.subheader("🗑 Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    confirm = st.checkbox("I understand this will permanently delete the account")

    if st.button("Delete Account"):
        valid_pin = get_valid_pin(pin)
        if valid_pin is None:
            st.error("❌ PIN must be exactly 4 digits")
        elif not confirm:
            st.warning("⚠ Please confirm before deleting")
        else:
            user = VijayMallyaBank.find_user(acc, valid_pin)
            if user:
                VijayMallyaBank.delete_account(user)
                st.success("✅ Account Deleted Successfully")
            else:
                st.error("❌ Invalid Account Number or PIN")

# -------------------- VIEW DETAILS --------------------

elif menu == "View Account Details":
    st.subheader("📄 Account Information")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)

    if st.button("View Details"):
        valid_pin = get_valid_pin(pin)
        if valid_pin is None:
            st.error("❌ PIN must be exactly 4 digits")
        else:
            user = VijayMallyaBank.find_user(acc, valid_pin)
            if user:
                st.success("✅ Account Found")
                safe_user = {k: v for k, v in user.items() if k != "pin"}
                st.json(safe_user)
            else:
                st.error("❌ Invalid Account Number or PIN")