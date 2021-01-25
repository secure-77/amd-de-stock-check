from bs4 import BeautifulSoup
from urllib.error import URLError, HTTPError
from urllib import request
import socket
import urllib
import gzip
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# config here
url = 'https://www.amd.com/de/direct-buy/de'
desiredProducts = ['5900X' , '5600X', '6800 XT']
sender_email = "mail@from.de"
receiver_email = "mail@to.de"
password = "your smtp pass"
smtp_server = "your.smtp.server"

# init
availableProducts = []
notavailableProducts = []


def checkStock():
    try:
        
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        cache = 'max-age=0'
        headers={'Connection':'close',
            'Cache-Control':cache,
            'User-Agent':user_agent,
            'Accept':accept,
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Length': '2'}

        # get content of website
        request=urllib.request.Request(url,headers=headers)
        response = urllib.request.urlopen(request)
        
        # unzip
        gzipFile = gzip.GzipFile(fileobj=response)
        data = gzipFile.read()
        
        # Beatiful it
        soup_mysite = BeautifulSoup(data, "lxml")
        
        # search for products
        products = soup_mysite.find_all("div",class_="direct-buy")

        for product in products:
            productName = product.find("div",class_="shop-title").contents
            availibility = product.find("div",class_="shop-links").contents
            availibility = str(availibility).replace("[\'\\n","").replace("\']","").strip().replace("\\n","")
                                  
            for desiredProduct in desiredProducts:
                if desiredProduct in str(productName):

                   # check if available
                   if 'Out of Stock' not in str(availibility):
                       availableProducts.append(desiredProduct + ' (' + availibility.replace("\',","").replace(", \'","") + ')')
                   else:
                       notavailableProducts.append(desiredProduct  + ' (' + availibility + ')')
    
    # error handling
    except urllib.error.HTTPError as e:
            return (e.code)
    except urllib.error.URLError as e:
            return ('URL_Error')
    except socket.timeout as e:
            return ('Connection timeout')


def sendMail(error):

    message = MIMEMultipart("alternative")  
    if error != 'None':
        message["Subject"] = "Fehler beim Abfragen des status!"
        error = 'Fehler: ' + error
    else:
        message["Subject"] = "AMD Produkt verfügbar!"
        error = ""
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Products availible: {productsAV}
    Products still not not availible: {productsNotAV}
    {url}
    {error}
    """

    html = f"""\
    <html>
    <body>
    <p>Products available: {productsAV}<br>
    Products still not not available: {productsNotAV}<br>
    <br>
    Shop Link: <a href=\"{url}\">{url}</a>
    </p>
    <p>{error}</p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

error = checkStock()
productsAV = ',  '.join(availableProducts)
productsNotAV = ',  '.join(notavailableProducts)

# if error on request or products available -> send mail
if error or len(availableProducts) > 0:
    sendMail(str(error))

