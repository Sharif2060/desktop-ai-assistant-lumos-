import requests
from bs4 import BeautifulSoup
from emailAlert import alert_system
from threading import Timer

URL = "https://www.amazon.in/Gentle-Shower-SuperSaver-Glycerine-Parabens/dp/B09KHJ38HJ/ref=sr_1_5?sr=8-5"

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip',
'DNT' : '1', # Do Not Track Request Header
'Connection' : 'close'
}

set_price = 1000

def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.contewhy a Python Mein module Hai To Har kam bahut aasani se ho jata hai aap Jaise yah chatbot hi ban gaya bahut aasani se lekin ab Yahi chij aap jawab Banaya Jaaye to bahut
                         theek hai theek hai
                         matlab scrap scrapping karne ke liye
                         Roj ko track Karen price ko ki price ko track Karen aur Agar price Mere expected value Mein Hai To vah Mujhe email Karen
                         theek hai
                         none
                         none
                         theek hai main interested hun matlab bataega
                         none
                         jo bhi retirement Hai matlab Ek Bar aur Mujhe explain Karke bhej dijiyega Agar WhatsApp per To Main Usko acche se kar sakta hun
                         lumos it's time to sleep
                         none
                         matlab tracking karna hai price ke liye matlab jakar vahan per jo bhi Jaise Ham Ek banae the email karne ke liye Jaise Amazon per
                         theek hai
                         Agar kaise karna hai to main kar sakta hun web scraping karna hai price ko track karna hai
                         compare Karna Hai Bar Bar jakar
                         Achcha uska CSP file banana Hai Ek Taraf Se file banana hai
                         matlab Kuchh Din pahle hi kar raha tha jaise Koi Bhi Ek yah book to scrap Karke website uska scrap karne
                         nt, 'html.parser')

    title = soup.find(id='productTitle').get_text()
    product_title = str(title)
    product_title = product_title.strip()
    print(product_title)
    price = soup.find(id='priceblock_ourprice').get_text()
    # print(price)
    product_price = ''
    for letters in price:
        if letters.isnumeric() or letters == '.':
            product_price += letters
    print(float(product_price))
    if float(product_price) <= set_price:
        alert_system(product_title, URL)
        print('sent')
        return
    else:
        print('not sent')
    Timer(60, check_price).start()

check_price()