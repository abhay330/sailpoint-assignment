# Modules 

import argparse
import requests
import logging
import smtplib
from datetime import datetime
from datetime import timezone
from tabulate import tabulate

# Arguments 

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", type=str, help="GitHub token")
parser.add_argument("-u", "--githuburl", type=str, help="GitHub Full URL to fetch Pull Requets")
parser.add_argument("-f", "--femail", type=str, help="From Email Address")
parser.add_argument("-r", "--temail", type=str, help="Receipient Email Address")
parser.add_argument("-p", "--password", type=str, help="Gmail App Password")
args = parser.parse_args()



# Variables 

access_token = args.token 
api_url =  args.githuburl

format = '%Y-%m-%d'

today = datetime.today().strftime('%Y-%m-%d')

# Collections

open = []
closed = []

# Reuqest Headers


headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'token '+ access_token
}

# API Call

try:
    response = requests.get(api_url, headers=headers)
except Exception as exception:
    print("Error: %s!\n\n" % exception)


# Parse through response received

for content in response.json():
    if content['state'] == 'open':
        dto_create_date = datetime.fromisoformat(content['created_at'][:-1]).astimezone(timezone.utc).strftime('%Y-%m-%d')
        diff_from_create_date = datetime.strptime(today, format) - datetime.strptime(dto_create_date, format)

        if diff_from_create_date.days <= 7:
            block = {
                'ID': content['id'],
                'URL': content['url'],
                'STATE': content['state'],
                'ACTIVITY DATE': content['created_at'],
                'USER': content['user']['login'],
                'TITLE': content['title']
            }
            open.append(block)
        else:
            logging.info('Pull Request Opened more than a week ago')
    
    elif content['state'] == 'closed':
        dto_closed_date = datetime.fromisoformat(content['closed_at'][:-1]).astimezone(timezone.utc).strftime('%Y-%m-%d')
        diff_from_close_date = datetime.strptime(today, format) - datetime.strptime(dto_closed_date, format)

        if diff_from_close_date.days <= 7:
            block = {
                'ID': content['id'],
                'URL': content['url'],
                'STATE': content['state'],
                'ACTIVITY DATE': content['closed_at'],
                'USER': content['user']['login'],
                'TITLE': content['title']
            }
            closed.append(block)
        else:
            logging.info('Pull Request Closed more than a week ago')
    else:
        logging.info('No Pull request found')

#  Email Data 
total_pr = len(open)+len(closed)

total_open = len(open)
total_closed = len(closed)

gmail_user = args.femail
gmail_app_password = args.password 

to_email = args.temail

sent_from = gmail_user
sent_to = [to_email]

sent_subject = "Weekly Pull Request Summary"

sent_body = """\
Hello,

Here is the latest Pull Request Summary for the past week

Total Request : %s

Total Open : %s
Total Closed : %s 

Open PR Summary:

%s

Closed PR Summary:

%s

Regards,
Team
""" % (total_pr, total_open, total_closed, tabulate(open,headers="keys"), tabulate(closed,headers="keys"))


email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

# Sending Email over Gmail 
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(sent_from, sent_to, email_text)
    server.close()

    print('Email sent!')
except Exception as exception:
    print("Error: %s!\n\n" % exception)