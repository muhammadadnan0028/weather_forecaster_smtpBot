import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

weather_url = "https://www.google.com/search?q=my+location+weather"

Fake_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

sender_email = "probot.pakistan@gmail.com"
sender_password = "zvcoblrlimaeruvt"
receiver_email = ["muhammadadnan0028@gmail.com"]

def send_notification(subject, message, receiver_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"Notification email sent successfully to {receiver_email}.")
    except Exception as e:
        print(f"Error sending email to {receiver_email}: {str(e)}")

def scrape_weather_data(url):
    response = requests.get(url, headers=Fake_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        location_element = soup.find(class_='BBwThe')
        conditions_element = soup.find(class_='wob_dcp')

        if location_element and conditions_element:
            location = location_element.get_text()
            conditions = conditions_element.get_text()
            return location,conditions
        else:
            print("Location or conditions element not found.")
            return None, None
    else:
        print("Error fetching weather data.")
        return None, None

location, conditions = scrape_weather_data(weather_url)

if conditions and ("rain" in conditions.lower() or "stormy" in conditions.lower()):
    notification_subject = f"Weather Alert: {location}"
    notification_message = f"Current weather conditions in {location}: {conditions}"
    
    for recipient in receiver_email:
        send_notification(notification_subject, notification_message, recipient)
else:
    print("No weather alert needed.")