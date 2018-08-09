import logging

import smtplib

import re

#from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_mail():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("AMAZON.YesIntent")

def ac():

    round_msg = render_template('ac_name')

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'accountName': str, 'applicationName': str})

def answer(accountName, applicationName):

    try:
        #SERVER = "mail.ap.amdocs.com"
        SERVER = "smtp.gmail.com:587"
        #FROM = "Saurabh.Agrawal@amdocs.com"
        FROM = "saurabhag1010@gmail.com"
        TO = ["Saurabh.Agrawal@amdocs.com"] # must be a list

        Urgency = 'Medium'
        
        if re.search('(?i)csm',applicationName):
        	if re.search('(?i)att',accountName):
        		mail_sender = 'CMICSMOGSAT&TZIG@int.amdocs.com'
        	elif re.search('(?i)metro',accountName):
        		mail_sender = 'CMICOMMetro@amdocs.com'
        	elif re.search('(?i)sprint',accountName):
        		mail_sender = 'CMICOMSprint@amdocs.com'
        	else:
        		mail_sender = ''
        		
        elif re.search('(?i)aam',applicationName):
        	if re.search('(?i)sprint',accountName):
        		mail_sender = 'cmiscdev@amdocs.com'
        	elif re.search('(?i)metro',accountName):
        		mail_sender = 'cmiscdev@amdocs.com'
        	else:
        		mail_sender = ''
        
        else:
        	mail_sender = ''
        		
        Description = 'Account Name is ' + accountName + ' and Application Name is ' + applicationName + ' and Mail is send to ' + mail_sender

        SUBJECT = "Test"
        TEXT = "Urgency : " + Urgency + "\nDescription : " + Description

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT) 

        # Send the mail
        server = smtplib.SMTP(SERVER)
        server.ehlo()
        server.starttls()
        server.login("saurabhag1010@gmail.com", "deepadinesh")
        server.sendmail(FROM, TO, message)
        server.close()

        msg = render_template('success')
    
    except:
        msg = render_template('failure')
    
    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)