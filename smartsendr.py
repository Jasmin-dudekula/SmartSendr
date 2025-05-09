import smtplib
import time
import random
import csv
import os
from smtplib import SMTPAuthenticationError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pwinput
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)  # auto-reset color after each print

# Ask for user input
GMAIL_USER = input("Enter your Gmail address: ")
GMAIL_PASSWORD = pwinput.pwinput(prompt="Enter your Gmail App Password: ", mask='*')
FILENAME = input("Enter your CSV filename (default: recipients.csv): ") or "recipients.csv"

LOG_FILE = "log.txt"

# Utility: log message to file
def log_message(message):
    try:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(f"{datetime.now()} - {message}\n")
            f.flush()
    except Exception as e:
        print(Fore.RED + f"❗Log error: {e}")

# Load recipients
def load_recipients(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except Exception as e:
        print(Fore.RED + f"❗Error loading CSV: {e}")
        log_message(f"❗Error loading CSV: {e}")
        exit()

# Send email
def send_email(to_email, to_name):
    subject = f"Important Update"
    body = f"""
Dear {to_name},

I hope this message finds you well.
I'm reaching out to share some exciting updates from our team. We've recently achieved significant milestones that we believe you'll find valuable.
If you have any questions or would like more details, feel free to reach out.

Best regards,
Jasmin
"""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
        print(Fore.GREEN + f"✅ Sent to {to_name}")
        log_message(f"✅ Sent to {to_name} <{to_email}>")
        return True
    except SMTPAuthenticationError:
        print(Fore.RED + "❗Authentication failed: Incorrect Gmail App Password.")
        log_message("❗Authentication failed: Incorrect Gmail App Password.")
        exit()
    except Exception as e:
        print(Fore.RED + f"❗Failed to send to {to_email}: {e}")
        log_message(f"❗Failed to send to {to_email}: {e}")
        return False

# Dynamic countdown delay
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(Fore.YELLOW + f"⏳ Next email in {i} seconds...", end="\r")
        time.sleep(1)
    print(" " * 40, end="\r")  # Clear line

# Main function
def main():
    print(Fore.CYAN + f"📁 Log file path: {os.path.abspath(LOG_FILE)}")
    recipients = load_recipients(FILENAME)

    if not recipients:
        print(Fore.RED + "❗No recipients found.")
        return

    # Preview the first email
    print("\n📤 Email Preview:")
    print(f"To: {recipients[0]['email'][:3]}...{recipients[0]['email'][-3:]}")
    print(f"Subject: Important Update")
    print(f"""
Dear {recipients[0]['name']},

I hope this message finds you well.
I'm reaching out to share some exciting updates from our team. We've recently achieved significant milestones that we believe you'll find valuable.
If you have any questions or would like more details, feel free to reach out.

Best regards,
Jasmin
""")

    confirm = input("Proceed to send all emails? (y/n): ").lower()
    if confirm != 'y':
        print("❗Cancelled.")
        log_message("❗User cancelled email sending.")
        return

    total_sent = 0
    total_failed = 0

    for index, person in enumerate(recipients):
        if not person.get('email') or not person.get('name'):
            print(Fore.YELLOW + f"⚠️ Skipping incomplete entry: {person}")
            log_message(f"⚠️ Skipped incomplete entry: {person}")
            continue

        success = send_email(person['email'], person['name'])
        if success:
            total_sent += 1
        else:
            total_failed += 1

        if index < len(recipients) - 1:
            delay = random.randint(6, 11)
            countdown(delay)

    print(f"\n Summary: {total_sent} sent ✅, {total_failed} failed ❗")
    log_message(f"Summary: {total_sent} sent ✅, {total_failed} failed ❗")

if __name__ == '__main__':
    main()
