import shopify
import json
from datetime import datetime 
from datetime import timedelta, timezone
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

email = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")

shopify_api_key = os.getenv("SHOPIFY_API_KEY")
shopify_shared_secret = os.getenv("SHOPIFY_SHARED_SECRET")
TOKEN = os.getenv("SHOPIFY_TOKEN")
shopify_password = os.getenv("SHOPIFY_PASSWORD")
shop_name = os.getenv("SHOPIFY_SHOP_NAME")
API_VERSION = os.getenv("SHOPIFY_API_VERSION")
SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
test_email = os.getenv("TEST_EMAIL")
google_forms = os.getenv("GOOGLE_FORM")

print(f"Connecting to {shop_name}.myshopify.com with API version {API_VERSION}...")


with open('mail_room/MandyMooLogo.png', 'rb') as img_file:
    img = MIMEImage(img_file.read())
    img.add_header('Content-ID', '<image1>')
    img.add_header('Content-Disposition', 'inline', filename="MandyMooLogo.png")


def create_email_template(name): 
    # HTML Template
    email_content = f"""\
<html>
    <body style="color: black;">
        <p>Hi <b>{name}<b>,</p>
        <p>Thank you for your purchase with <b>MandyMoo</b>! 💕</p>
        <p>
            We're excited to help you create a unique, one-of-a-kind blind box. Let's start customising! 
            Please take a moment to fill out this Google Form with your customisation details: 
            <a href="{google_forms}" target='_blank'>Valentine's Edition Blind Box Template 🌹</a>
            (You may use any email that works with Google Form, but preferably the same email you used for your purchase).
        </p>
        <p>
            Once we receive your form, we'll get started on creating your customised 
            <b><i>Valentine's Edition Blind Box Template</i></b> 
            and send it to you via email within 1-3 business days.
        </p>
        <br><br>
        <h4>⭐️ NEXT STEPS:</h4>
        <ol>
            <li><b>How-to-Make Guide</b> 
            <br>
            <br>
            Along with your customised PDF template, you’ll also receive a detailed <b>How-to-Make Guide</b>  in the email. This guide will walk you through the process of assembling your blind box, step by step, making it as easy as possible to create your beautiful, personalised gift. It also comes with a Printing Guide and Gift-Giving Guide.</li>
            <br>
            <li><b>Print Your Template!</b> 
            <br>
            <br>
            After reading the How-to-Make Guide, it’s time to print! You can print it at home or take it to your local Officeworks on a USB for high-quality results. Here are the best A4 paper options for printing:
                <ul>
                    <li>210gsm+ Uncoated</li>
                    <li>140gsm Gloss</li>
                    <li>210gsm Gloss (this is the paper we personally recommend!)</li>
                </ul>
            </li>
        </ol>
        <br><br>
        <p>If you have any questions along the way, don't hesitate to reach out - we're here to help! 💌</p>
        <p>Thank you again for choosing <b>MandyMoo</b>, where <i>Love is in the details</i>. ❤️</p>
        <br>
        <br>
        <p>Warm Regards,</p>
        <p><b>Amanda 💕</b></p>
        <p>
            Instagram: <a href='https://instagram.com/mandymoo.official' target='_blank'>@mandymoo.official</a><br>
            TikTok: <a href='https://tiktok.com/@mandymoo.official' target='_blank'>@mandymoo.official</a>
        </p>
        <img src="cid:image1" alt="MandyMooLogo" style="width:20%; max-width:300px;">
    </body>
</html>
    """
    
    return email_content

def get_orders():
    with shopify.Session.temp(SHOP_URL, API_VERSION, TOKEN):
        # Fetch all orders with 'any' status
        orders = shopify.Order.find(status="any")
        return orders

def get_customer(customer_id):

    query = '''{
    customer(id: "gid://shopify/Customer/'''+customer_id +'''") {
        id
        firstName
        email
    }
    }'''

    with shopify.Session.temp(SHOP_URL, API_VERSION, TOKEN):
        customer = shopify.GraphQL().execute(query)
        return customer

def work():
    print("MOO MOO HAS WOKEN UP TO WORK")
    orders = get_orders()
    orders_last_thirty_minutes = [order for order in orders if datetime.fromisoformat(order.created_at) > datetime.now(timezone(timedelta(seconds=39600))) - timedelta(minutes=30)]
    customers_order_number = [[order.customer.id, order.order_number] for order in orders_last_thirty_minutes]
    customer_details = {customer[1]:json.loads(get_customer(str(customer[0])))['data']['customer'] for customer in customers_order_number}
    email_details = [[order_number, customer['firstName'], customer['email']] for order_number, customer in customer_details.items()]
    
    print(f"MOO MOO HAS SEEN {len(email_details)} NEW EMAILS TO SEND")
    
    for order in email_details:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = order[2]
        subject = str(f"ORDER #{order[0]} - Let's Customise Your Blind Box!")
        msg['Subject'] = subject

        html_content = create_email_template(order[1])
        msg.attach(MIMEText(html_content, 'html'))
        msg.attach(img)

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() # Upgrade the connection to secure
            server.login(email, email_password)
            server.send_message(msg)
        
    print(f"MOO MOO HAS SENT {len(email_details)} NEW EMAILS TO SEND")
    print("MOO MOO BRB 5 MINS SLEEP")


def test():
    print("TESTING MOO MOO EMAIL")
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = test_email
    subject = str(f"ORDER #TEST - Let's Customise Your Blind Box!")
    msg['Subject'] = subject

    html_content = create_email_template("Gary")
    msg.attach(MIMEText(html_content, 'html'))
    msg.attach(img)

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls() # Upgrade the connection to secure
        server.login(email, email_password)
        server.send_message(msg)
    print("EMAIL SENT")