# SmartSendr – Python Email Automation Tool

SmartSendr is a Python-based command-line application that automates sending personalized emails using Gmail's SMTP server. It is designed to simulate natural human behavior with dynamic delays, customizable messages, and UTF-8 logging — all to help improve deliverability and reduce the chances of your emails going to spam.


#  Features

-  Send emails to multiple recipients from a CSV file.
-  Compose a custom subject and message body with `{name}` placeholders for personalization.
-  Dynamic countdown delay between emails to mimic human-like sending behavior.
-  Color-coded terminal output for success, failure, and status.
-  Logs all email activity (sent/failed) with timestamps in `log.txt`.
-  Secure login using Gmail App Password.


# CSV Format

Ensure your recipient CSV file (e.g., `recipients.csv`) is formatted like this:
name,email
abc,abc430@gmail.com


# Prerequisites

- Python 3.6 or higher.
- Gmail account with App Password enabled.


# Setup
1. Clone the repository:
   git clone https://github.com/yourusername/foldername.git
   cd folderpath

2. Create a virtual environment:
   python -m venv env

3. Activate the virtual environment:
   .\env\Scripts\activate

4. Install the required packages:
   pip install -r requirements.txt

