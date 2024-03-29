import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def get_weather():
    api_key = "5ae120b0e854caf22f609c46800e97a9"
    city = "{replace}"
    url = "http://api.openweathermap.org/data/2.5/weather?"
    url_final = url + "appid=" + api_key + "&id=" + city + "&units=metric"
    response = requests.get(url_final)
    data = response.json()
    return data

def get_forecast():
    api_key = "5ae120b0e854caf22f609c46800e97a9"
    city = "{replace}"
    url = "http://api.openweathermap.org/data/2.5/forecast?"
    url_final = url + "appid=" + api_key + "&id=" + city + "&units=metric"
    response = requests.get(url_final)
    data = response.json()
    return data

def check_rain_forecast(hourly_forecast):
    for forecast in hourly_forecast['list']:
        if 'rain' in forecast.get('weather', [])[0].get('main', '').lower():
            return True
    return False

def send_warning_email(temperature, rain_forecast):
    temp = str(temperature)
    sender_email = "{replace}"
    sender_password = "{replace}"
    receiver_email = "{replace}"
    msg = MIMEMultipart()
    msg['Subject'] = "WARNING! COLD WEATHER "+temp+" degree TODAY!"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    message = f"Hey, it is going to be very cold today, you must wear more when you go out!"

    if rain_forecast:
        message += " It might rain later, remember to bring an umbrella!"

    with open(r'C:\Users\wawac\Downloads\coldbeans.jpg', "rb") as f:
        image_data = f.read()

    html_msg = f"""
    <html>
        <body style="color: blue; font-family: Arial, sans-serif;">
            <p style="font-size: 38px;"><b>{msg['Subject']}</b></p>
            <img src="cid:image" style="width: 180px; height: auto;">
            <p style="font-size: 22px; color: black;">{message}</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_msg, 'html'))

    img = MIMEImage(image_data, name='coldbeans.jpg')
    img.add_header('Content-ID', '<image>')
    msg.attach(img)
    
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("EMAIL sent successfully")

def send_reminder_email(temperature, rain_forecast=True):
    temp = str(temperature)
    sender_email = "{replace}"
    sender_password = "{replace}"
    receiver_email = "{replace}"
    msg = MIMEMultipart()
    msg['Subject'] = "WARNING! COLD WEATHER "+temp+" degree TODAY!"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    message = f"Hey, it is going to be quite cold today, would recommend you wear a bit more when you go out!"

    if rain_forecast:
        message += " It might rain later, remember to bring an umbrella!"
    
    with open(r'C:\Users\wawac\Downloads\coldbeans.jpg', "rb") as f:
        image_data = f.read()

    html_msg = f"""
    <html>
        <body style="color: blue; font-family: Arial, sans-serif;">
            <p style="font-size: 38px;"><b>{msg['Subject']}</b></p>
            <img src="cid:image" style="width: 180px; height: auto;">
            <p style="font-size: 22px; color: black;">{message}</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(html_msg, 'html'))

    img = MIMEImage(image_data, name='coldbeans.jpg')
    img.add_header('Content-ID', '<image>')
    msg.attach(img)
    
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("EMAIL sent successfully")


def send_telegram_message_reminder(temperature, rain_forecast):
    token='{replace}'
    chat_id='{replace}'
    temp = str(temperature)
    message='['+temp+'度] 少心凍親！ 記得著多啲！Becareful it is getting cold! Do not forget to wear a couple more layers when you are going out!'
    if rain_forecast:
        message = '['+temp+'度][有雨] 少心凍親！ 記得著多啲！带遮啊！ Becareful it is getting cold! Do not forget to wear a couple more layers when you are going out! Remember to bring an umbrella as well!'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, json=params)
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except:
        send_telegram_message_reminder()

def send_telegram_message_warning(temperature, rain_forecast):
    token='{replace}'
    chat_id='{replace}'
    temp = str(temperature)
    message= '['+temp+'度] 好L凍！要包到成隻粽咁先可以出去！带遮啊！ Becareful it is getting cold! Do not forget to wear a couple more layers when you are going out!'
    if rain_forecast:
        message = '['+temp+'度][有雨】 好L凍！要包到成隻粽咁先可以出去！带遮啊！ OMG SOOOOO COLD! WEAR UNTIL YOU LOOK LIKE A TURTLE!'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, json=params)
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except:
        send_telegram_message_warning()
        
def main():
    weather_data = get_weather()
    hourly_forecast = get_forecast()
    rain_forecast = check_rain_forecast(hourly_forecast)
    if weather_data["cod"] != "404":
        temperature = weather_data["main"]["temp"]
        if temperature < 10:
            print("COLD WEATHER! MUST WEAR MORE LAYERS!")
            send_telegram_message_warning(temperature, rain_forecast)
            send_warning_email(temperature, rain_forecast)
        elif temperature < 15:
            print("COLD WEATHER! RECOMMEND WEAR MORE LAYERS!")
            send_telegram_message_reminder(temperature, rain_forecast)
            send_reminder_email(temperature, rain_forecast)
        elif temperature < 20:
            print("BIT CHILLI!")
        else:
            print("NICE WARM AND COLD!")
    else:
        print("City does not exist!")

if __name__ == "__main__":
    main()
