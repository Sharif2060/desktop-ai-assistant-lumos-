import requests
from bs4 import BeautifulSoup
import smtplib
import pyttsx3

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_price_from_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the price using various Amazon price tags
    price = None
    try:
        price = soup.find('span', id='priceblock_ourprice')
        if price is None:
            price = soup.find('span', id='priceblock_dealprice')
        if price:
            price = float(price.text.replace('₹', '').replace(',', '').strip())
    except Exception as e:
        print(f"Error scraping Amazon price: {e}")
        return None
    return price

def get_price_from_flipkart(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the price using Flipkart price tags
    price = None
    try:
        price = soup.find('div', class_='_30jeq3 _16Jk6d')
        if price:
            price = float(price.text.replace('₹', '').replace(',', '').strip())
    except Exception as e:
        print(f"Error scraping Flipkart price: {e}")
        return None
    return price

def price_notifier():
    # Step 1: Speak and ask for user input (URL and expected price)
    speak("Please give the URL")
    url = input("Please give the URL: ")

    headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip',
'DNT' : '1', # Do Not Track Request Header
'Connection' : 'close'
}
    
    speak("Please give the expected price")
    expected_price = float(input("Please give the expected price: "))

    # Step 2: Check if the URL is Amazon or Flipkart, and scrape accordingly
    price = None
    if "amazon" in url:
        price = get_price_from_amazon(url)
    elif "flipkart" in url:
        price = get_price_from_flipkart(url)
    else:
        speak("Sorry, I can only scrape Amazon and Flipkart at the moment.")
        return
    
    if price is None:
        speak("Unable to retrieve the price. Please check the URL or try again later.")
        print("Unable to retrieve the price.")
        return

    print(f"Current price is: {price}")
    speak(f"The current price is {price}")

    # Step 3: If the price is below the expected value, send an email
    if price < expected_price:
        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.ehlo()
            smtp_server.starttls()

            # Login to the Gmail account
            smtp_server.login('sharifalam206@gmail.com', 'sobh zrdt tqhg iuxn')

            # Create and send the email
            subject = "Price Drop Alert!"
            body = f"The price has dropped to {price}. Buy it now!"
            msg = f"Subject: {subject}\n\n{body}"
            smtp_server.sendmail('sharifalam206@gmail.com', 
                                 'dalaiamrendra@gmail.com', msg)
            
            speak("Email sent successfully!")
            print("Email sent successfully!")
            smtp_server.quit()
        
        except Exception as e:
            speak(f"Error sending email: {e}")
            print(f"Error sending email: {e}")
    else:
        speak(f"The price is still above {expected_price}. No email sent.")
        print(f"The price is still above {expected_price}. No email sent.")

# Example of how this function can be called in your Jarvis project
# price_notifier()




if __name__ == "__main__":
    price_notifier()
# Example of how this function can be called in your Jarvis project
# price_notifier()
# genai.configure(api_key="AIzaSyBKOBfL00t3XttgXTut53vh01Z2MV6jXPI")
