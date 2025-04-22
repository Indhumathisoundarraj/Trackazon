from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import datetime
import schedule
import time as t
import os
import csv


def send_email_alert(title, price):
    sender_email = "SENDER_EMAIL_ID"
    sender_password = "APP_PASSWORD" #visit google security for app password[ex: 16 digit without space
    recipient_email = "RECEIVER_EMAIL_ID"

    subject = "💰 Trackazon Alert - Price Dropped!"
    body = f"Product: {title}\nCurrent Price: ₹{price}\nLink: https://www.amazon.in/iQOO-Snapdragon-Processor-Slimmest-Smartphone/dp/B0DW48MM7C?ref=dlx_deals_dg_dcl_B0DW48MM7C_dt_sl10_61_pi&pf_rd_r=0TWY4WG3X4GGTWQHBJXZ&pf_rd_p=1ce42f93-7595-413b-b263-9a38e0c62f61"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            print("📧 Alert email sent successfully!")
    except Exception as e:
        print("Email sending failed:", e)
    
def job():
    print("Running Trackazon...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # show browser
        page = browser.new_page()
    
        page.goto("https://www.amazon.in/iQOO-Snapdragon-Processor-Slimmest-Smartphone/dp/B0DW48MM7C?ref=dlx_deals_dg_dcl_B0DW48MM7C_dt_sl10_61_pi&pf_rd_r=0TWY4WG3X4GGTWQHBJXZ&pf_rd_p=1ce42f93-7595-413b-b263-9a38e0c62f61")#you can change the product link
        page.wait_for_selector("#productTitle")

        title = page.query_selector("#productTitle").inner_text().strip()
        price = page.query_selector(".a-price-whole").inner_text().strip()

        print("Title:", title)
        print("Price:", price)

        browser.close()

# 🕒 Add timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 📝 Save to CSV
    filename = 'product_data.csv'
    file_exists = os.path.isfile(filename)

    last_price = None
    if os.path.exists("product_data.csv"):
        with open("product_data.csv", "r", encoding='utf-8') as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                last_price = rows[-1][2]  # No need to clean yet
# 🧠 Clean price strings
    clean_current = int(price.replace(",", "").replace(".", "").strip())

# If price dropped, send email
    if last_price:
        clean_previous = int(last_price.replace(",", "").replace(".", "").strip())
        # Compare and send alert if price dropped
        if clean_current < clean_previous:
            send_email_alert(title, price)

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
    
        if not file_exists:
            writer.writerow(["Time", "Title", "Price"])  # Header
    
        writer.writerow([now, title, price])
    print(f"{now} | Scraped: {title} | ₹{price}")
    
#🔁 Run every hour (you can change to daily etc.)
schedule.every(1).hours.do(job)#you can change the hours to seconds or minutes.

print("Scheduler started... Ctrl+C to stop")

while True:
    schedule.run_pending()
    t.sleep(1)
