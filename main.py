# Import all required libraries and modules
import requests
from bs4 import BeautifulSoup
import datetime as dt
import ssl
import smtplib
from email.message import EmailMessage
import time
# import pprint

set_price = int
# P.S: I intermittently used camelCase for variables instead of snake_case intentionally, please excuse that.


# Define all required global scope functions
def bill_to_float(bill: str) -> float:
    """Converts bill(money i. e dollar or naira bill) to a floating point number"""
    bill = str(bill)
    float_num = ""
    for char in bill:
        # print("Char ni", char)
        if str.isdigit(char) or char == ".":
            # print("Char is", char)
            float_num += char
    print("float_num is", float_num, "and type", type(float_num))
    return float(float_num)


# Interact with User and get required information
print("Good day dear User.\nWelcome to the amazon price tracker")
print('---------\nAre you ready to track your next product?')
time.sleep(1.0)
username = input("Please start by inputting your name: ")
product_link = input("Type/Paste the product link or 'default' to use the default link and price: ")
if product_link.lower() != "default":
    set_price = input("Type your preffered price here: ")
user_email = input("Input your email address: ")
for i in range(3):
    print("Processing...")
    time.sleep(0.8)
print("Thank you, you'd receive an email from us once the price is met.")

# Set amazon product uniform Resource Locatror (URL)
if product_link.lower() == "default":
    product_link = "https://www.amazon.com/Apple-MacBook-10-core-English-Renewed/dp/B0C8GM4KKD/ref=sr_1_3?" \
          "keywords=macbook&qid=1692654666&sprefix=mac%2Caps%2C536&sr=8-3&th=1"
    set_price = 2000

# Send request to get the webpage html code
amazon_header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko"
                    ") Chrome/116.0.0.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9",
}
response = requests.get(url=product_link, headers=amazon_header, timeout=60)
html = response.text

# Make soup from the html code and retrieve the required information
soup = BeautifulSoup(html, "lxml")
productName = soup.find("span", id="productTitle").string
# print("The product being tracked is", productName)
price = soup.find("span", class_="a-offscreen").string
productPrice = bill_to_float(str(price))

# print("The product price is", productPrice, "It's a", type(price), "type object")

# Verify if price requirement is met then send mail
if productPrice < set_price:
    thisDay = dt.datetime.now()
    today = thisDay.strftime("%A, %dth of %B, %Y.")
    mail_content = f"Hi, {username}.\nToday is {today}\nThe amazon product you've been tracking has met your " \
                   f"set price requirement of ${set_price}.\n  \nProduct Name: {productName}.\n  \nProduct " \
                   f"Price: ${productPrice}.\nHere is a link to the product👇⤵:\n{product_link}" \
                   f"\n  \nThanks for writing this code and do have a great day."
    mail_sender = "opolopothings@gmail.com"
    PASSWORD = "zupsypvvrwkytdxq"
    message = EmailMessage()
    message["From"] = mail_sender
    message["To"] = user_email
    message["Subject"] = "Price Prerequisite Met"
    message.set_content(mail_content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as mail:
        mail.login(user=mail_sender, password=PASSWORD)
        mail.sendmail(from_addr=mail_sender, to_addrs="ebifredrick07@gmail.com", msg=message.as_string())
