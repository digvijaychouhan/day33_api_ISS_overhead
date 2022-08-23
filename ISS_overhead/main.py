import time
import requests
import datetime as dt
import smtplib

MY_LAT = 13.022505
MY_LNG = 12.571365
EMAIL_USR = "xyz@gmail.com"
EMAIL_PWD = "xyz"
EMAIL_SMTP = "smtp.gmail.com"
RECEIVER = "xyz@yahoo.com"
EMAIL_MSG = "Subject: Satellite\n\nDear,\nGo out the as the ISS is overhead :)"


def iss_is_overhead():
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5:
        return True
    return False


def is_night():
    parameters = {"lat": MY_LAT, "lng": MY_LNG, "formatted": 0}
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
    return False


while True:
    if iss_is_overhead() and is_night():
        with smtplib.SMTP(EMAIL_SMTP, 587) as connection:
            connection.starttls()
            connection.login(EMAIL_USR, EMAIL_PWD)
            connection.sendmail(from_addr=EMAIL_USR, to_addrs=RECEIVER, msg=EMAIL_MSG)
            print("Mail sent successfully.")

    time.sleep(60)
