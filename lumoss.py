import pyttsx3
import speech_recognition as sr
import datetime
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import cv2
import pyaudio
import random
from bs4 import BeautifulSoup
import smtplib
 
from requests import get
import wikipedia
import pyautogui
import time
import subprocess
import webbrowser
import pywhatkit as kit
import pyautogui
import psutil
import requests
from transformers import pipeline
TF_ENABLE_ONEDNN_OPTS=0
import openai
import google.generativeai as genai
import threading





# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 170 ) # Correct the 'voice' property


# Text to speech
def speak(audio):

    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=8, phrase_time_limit=8)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')  # Recognize the command
        print(f"User said: {query}")
    except Exception as e:
        print("Could not understand the audio. Please say that again...")
        return "none"
    return query



# Initialize OpenAI API
openai.api_key = ''


def chat_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPT-3.5 engine
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()








# to wish
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >=0 and hour<=12:
        speak('good morning')
    elif hour >12 and hour<18:
        speak('good afternoon ')
    else:
        speak('good evening')
    speak('i am Lumos.')
    speak('a desktop ai assistant.')
    speak('developed by Sharif Alam.')


# API_KEY = ""
# # Initialize the Hugging Face pipeline (optional if you prefer local inference)
# generator = pipeline('text-generation', model='gpt2')

# def chat_with_huggingface(prompt):
#     """Function to generate text using Hugging Face API"""
#     API_URL = "https://api-inference.huggingface.co/models/gpt2"
#     headers = {"Authorization": f"Bearer {API_KEY}"}
#     payload = {"inputs": prompt}

#     response = requests.post(API_URL, headers=headers, json=payload)
#     if response.status_code == 200:
#         return response.json()[0]['generated_text']
#     else:
#         return "Sorry, I couldn't process the request."



# Define the Gemini function with chat history
def query_gemini(input_text):
    global chat_history

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Add the user query to chat history
        chat_history.append({"role": "user", "content": input_text})

        # Start the chat session with history
        chat_session = model.start_chat(history=chat_history)

        # Send the query to Google Gemini
        response = chat_session.send_message(input_text)

        # Add the Gemini response to chat history
        chat_history.append({"role": "assistant", "content": response.text})

        return response.text
    except Exception as e:
        return f"Error occurred: {str(e)}"






# Configure Google Gemini API
genai.configure(api_key="")

# Create model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define the Gemini function
def query_gemini(input_text):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        
        # Start the chat session
        chat_session = model.start_chat(history=[])
        
        # Send the query to Google Gemini
        response = chat_session.send_message(input_text)
        
        return response.text
    except Exception as e:
        return f"Error occurred: {str(e)}"



# # Function to handle Gemini interaction
# def google_gemini_interaction():
#     speak("What do you want to search on Gemini, Sir?")
#     user_query = takecommand().lower()
#     if user_query != "none":
#         speak(f"Searching Gemini for {user_query}")
#         gemini_response = ask_google_gemini(user_query)
#         speak(gemini_response)

def price_notifier():
    # Step 1: Speak and ask for user input (URL and expected price)
    speak("Please give the URL")
    url = input("Please give the URL: ")
    
    speak("Please give the expected price")
    expected_price = float(input("Please give the expected price: "))

    # Step 2: Scrape the price from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the price (assuming similar HTML structure as before)
    price = float(soup.find('p', class_='price_color').text[1:])
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
                                 'sharifalam9667@gmail.com', msg)
            
            speak("Email sent successfully!")
            print("Email sent successfully!")
            smtp_server.quit()
        
        except Exception as e:
            speak(f"Error sending email: {e}")
            print(f"Error sending email: {e}")
    else:
        speak(f"The price is still above {expected_price}. No email sent.")
        print(f"The price is still above {expected_price}. No email sent.")





#  Function to calculate shared expenses and speak inputs and outputs
def calculate_expenses():
    speak("Enter your hostel or flat rent")
    rent = int(input("Enter your hostel/flat rent = "))
    
    speak("Enter the amount of food ordered")
    food = int(input("Enter the amount of food ordered = "))
    
    speak("Enter the total electricity spend")
    electricity_spend = int(input("Enter the total of electricity spend = "))
    
    speak("Enter the charge per unit of electricity")
    charge_per_unit = int(input("Enter the charge per unit = "))
    
    speak("Enter the number of persons living in the room or flat")
    persons = int(input("Enter the number of persons living in room/flat = "))
    
    total_bill = electricity_spend * charge_per_unit
    output = (food + rent + total_bill) // persons
    
    result_text = f"Each person will pay {output} rupees."
    print(result_text)
    speak(result_text)















# Set up your OpenWeatherMap API key here
API_KEY = ""

# Function to get weather data
def get_weather(city_name):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    # Make the API request
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]

        # Extracting temperature and weather description
        temperature = main["temp"]
        weather_description = weather["description"]

        # Return the formatted weather details
        return temperature, weather_description
    else:
        return None, None


# Function to get temperature and type of day
def tell_weather(city_name):
    temperature, weather_description = get_weather(city_name)

    if temperature and weather_description:
        message = (f"The current temperature in {city_name} is {temperature} degrees Celsius "
                   f"with {weather_description}.")
        #  print(message)  # Print to console
        speak(message)  # Jarvis will speak this
    else:
        speak(f"Sorry, I couldn't fetch the weather for {city_name}.")


 




# Function to open Notepad and write into it
def open_notepad_and_write():
   # Open Notepad
    npath = "C:\\Windows\\System32\\notepad.exe"
    os.startfile(npath)
    time.sleep(2)  # Wait for Notepad to open

    # Keep taking input from the user
    speak("What would you like me to write? Say 'stop' when you are done.")
    while True:
        command = takecommand()

        if 'stop' in command:
            speak("Okay, I have finished writing.")
            break

        if 'close it' in command or 'close notepad' in command:
            speak("Closing Notepad.")
            close_notepad()
            break

        # Write to Notepad using pyautogui
        pyautogui.typewrite(command)
        pyautogui.press("enter")  # To simulate hitting 'Enter' after each input

# Function to close Notepad
def close_notepad():
    # Iterate over all running processes
    for proc in psutil.process_iter():
        if proc.name().lower() == "notepad.exe":
            proc.kill()  # Kill the Notepad process
            speak("Notepad has been closed.")
            return
    speak("Notepad is not open.")

# Function to search YouTube
def search_youtube():
    # Ask the user what they want to search
    speak("What would you like to search for on YouTube?")
    search_query = takecommand()

    if search_query != "none":
        speak(f"Searching for {search_query} on YouTube.")
        kit.playonyt(search_query)  # Directly search the query on YouTube
        time.sleep(5 )  # Wait for the browser to load

    speak("YouTube is now playing. Say 'close YouTube' when you're done.")

    while True:
        command = takecommand()

        # Only check for the 'close' command, avoid continuously asking for commands
        if 'close youtube' in command.lower() or 'close it' in command.lower():
            speak("Closing YouTube.")
            os.system("taskkill /im brave.exe /f")  # Adjust browser process name if needed
            break


if __name__ == "__main__":
    speak('Hello Sir')

    city = "New Delhi"  # Replace with your location
    tell_weather(city)
    wish()
    # takecommand()
    # AIzaSyBTKd90AenyioEZEpCd_LpWBFw5PNK3Dp8


    # print(sr.Microphone.list_microphone_names())

    while True:
        query = takecommand().lower()

        # logic building for task
        if "open camera" in query:
           cap =cv2.VideoCapture(0)
           while True:
               ret,img =cap.read()
               cv2.imshow('webcam' , img)
               k = cv2.waitKey(50)
               if k==27:
                   break
           cap.release()
           cv2()
        

        
        elif "notepad" in query:
          open_notepad_and_write()

        elif "product" in query:
            price_notifier()

        elif "youtube" in query:
          search_youtube()

        elif "command prompt" in query:
           os.system("start cmd")
           speak('command prompt opened sir ')

       


        elif "rent " in query:
            calculate_expenses()




 

        elif "play music" in query:
           music_dir="C:\\Users\\Rais Ahamed\\OneDrive\\Pictures"
           songs=os.listdir(music_dir)
           rd=random.choice(songs)
           os.startfile(os.path.join(music_dir,rd))



        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f" Sir your IP adress is{ip}")


        elif "wikipedia" in query:
            speak("searching wikipedia")
            query = query.replace("wikipedia" ,"")
            results = wikipedia.summary(query,sentences=2)
            speak("according to wikipedia")
            speak(results)
            print(results)

        # elif "open youtube" in query:
        #     webbrowser.open("www.youtube.com")

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")


        elif "open github" in query:
            webbrowser.open("www.github.com")

        elif "deadline

        elif "open google" in query:
            speak("Sir, what should i search on google")
            cm=takecommand().lower()
            webbrowser.open(f"{cm}")


        elif "send message" in query:
            kit.sendwhatmsg_instantly("+919540718858", "this is testing protocol", 17, 56)

    

      


        # elif "face" in query:
        #     speak("What would you like to ask Hugging Face GPT?")
        #     hf_query = takecommand().lower()
        #     response = chat_with_huggingface(hf_query)
        #     speak(response)


         # OpenAI Integration: Use hot word 'openai' for OpenAI-related queries
        elif "open" in query:
            speak("What would you like to ask OpenAI?")
            openai_query = takecommand().lower()
            response = chat_with_openai(openai_query)
            speak(response)




        # Listen for the sleep time command to exit the loop;
        elif "sleep" in query:
            speak("Okay Sir, going to sleep. Have a good day!")
            break  # Break the loop and exit the program

           

        else:
            # If the query doesn't match any predefined commands, send it to Google Gemini
            # speak("Let me check that for you.")
            response = query_gemini(query)
            # print(f"Response says: {response}")
            speak(response)
