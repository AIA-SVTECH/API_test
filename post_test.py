import requests

url = "http://140.83.86.79:8000/create_payer"


def merchant():
    data = {"merchant_name": "VNPAY"}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Response data:", response.json())
    else:
        print(f"Failed to get response. Status code: {response.status_code}")
        print("Response content:", response.text)


def create_account(
    name: str,
    email: str,
    phone_number: str,
    account_balance: float = 0,
):
    data = {
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "account_balance": account_balance,
    }

    response = requests.post(url, params=data)
    if response.status_code == 200:
        print("Account created:", response.json())
    else:
        print(f"Failed to create account. Status code: {response.status_code}")
        print("Response content:", response.text)


if __name__ == "__main__":
    name = ("John Doe",)
    email = ("john.doe@example.com",)
    phone_number = ("1234567890",)
    account_balance = (1000.0,)
    create_account(name, email, phone_number, account_balance)
