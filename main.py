# import requests
#
# response = requests.get(url="http://api.open-notify.org/iss-now.json")
#
# response.raise_for_status()
#
# longitude = response.json()["iss_position"]["longitude"]
# latitude = response.json()["iss_position"]["latitude"]
#
# iss_position = (longitude, latitude)
#
# print(iss_position)


#####################################################


# from tkinter import *
# import requests
#
# def get_quote():
#     response = requests.get(url="https://api.kanye.rest/")
#     response.raise_for_status()
#     quote = response.json()["quote"]
#     canvas.itemconfig(quote_text, text=quote)
#
#
#
# window = Tk()
# window.title("Kanye Says...")
# window.config(padx=50, pady=50)
#
# canvas = Canvas(width=300, height=414)
# background_img = PhotoImage(file="background.png")
# canvas.create_image(150, 207, image=background_img)
# quote_text = canvas.create_text(150, 207, text="", width=250, font=("Arial", 30, "bold"), fill="white")
# canvas.grid(row=0, column=0)
#
# kanye_img = PhotoImage(file="kanye.png")
# kanye_button = Button(image=kanye_img, highlightthickness=0, command=get_quote)
# kanye_button.grid(row=1, column=0)
#
# window.mainloop()

#####################################################

import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL= ""
MY_PASSWORD= ""
MY_LAT = 40.712776
MY_LONG = -74.005974


# print(sunrise)
# print(sunset)
# print(time_now.hour)

def iss_nearby():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if  abs(abs(iss_latitude) - abs(MY_LAT)) < 5.0 and abs(abs(iss_longitude) - abs(MY_LONG)) < 5.0:
        return True
    else:
        return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response_sun = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_sun.raise_for_status()
    data_sun = response_sun.json()
    sunrise = int(data_sun["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_sun["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if iss_nearby() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
           from_addr=MY_EMAIL,
           to_addrs=MY_EMAIL,
           msg="Subject:Look Up\n\nThe ISS is above you in the sky!"
        )

