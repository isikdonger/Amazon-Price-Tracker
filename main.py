import os
from bs4 import BeautifulSoup
import requests
import smtplib

TARGET_PRICE = 6600

live_url = "https://www.amazon.com.tr/dp/B0CRNPD5P8?m=A1UNQM1SR2CHM&tag=epeyt-21&th=1&psc=1&_encoding=UTF8&aff_sub4=6"

header = {
    "User-Agent": "Edg/127.0.0.0",
    "Accept-Language": "tr,en;q=0.9,en-GB;q=0.8"
}

response = requests.get(live_url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")

# Find the HTML element that contains the price
price = soup.find(class_="a-price-whole").get_text()
price = price.split(".")[0] + price.split(".")[1]
price = int(price.split(",")[0])
#print(price)

title = soup.find(id="productTitle").get_text().strip()
#print(title)

if price < TARGET_PRICE:
    message = f"{title} is on sale for {price}!"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        mail_address = os.environ.get("EMAIL")
        result = connection.login(mail_address, os.environ.get("PASSWORD"))
        connection.sendmail(
            from_addr=mail_address,
            to_addrs=mail_address,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{live_url}".encode("utf-8")
        )
        print("Mail Send")