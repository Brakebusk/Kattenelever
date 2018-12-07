#!/usr/bin/env python3

#Creates and sends a password recovery email.

import cgi
import pymysql
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import random
import string

def randomValueGenerator(size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

print("Content-type: text/html; charset=UTF-8")
print()

formdata = cgi.FieldStorage()

email = formdata.getvalue("email")

if len(email) > 0:
	connection = pymysql.connect(host="localhost", user="root", port=3306, cursorclass=pymysql.cursors.SSCursor)
	
	cursor = connection.cursor()
	sql = "SELECT userid FROM bksis.usertable WHERE email=%s"
	cursor.execute(sql, (email))
	response = cursor.fetchone()
	cursor.close()
	
	if not response:
		print("{NOT REGISTERED}")
	else:
		resetcode = randomValueGenerator(32)
		
		cursor = connection.cursor()
		sql = "UPDATE bksis.usertable SET resetcode=%s WHERE email=%s"
		cursor.execute(sql, (resetcode, email))
		cursor.close()
		connection.commit()
		
		resetLink = "https://kattenelever.no/passwordreset.cgi?resetcode=%s" % (resetcode)
		
		messageBody = '''Trykk på linken under for å endre ditt passord på Kattenelever:\n%s\n\Plz remember next time.''' % (resetLink)
		
		message = MIMEText(messageBody)
		message['Subject'] = "Passordgjenopprettelse"
		message['From'] = "kattenelever@outlook.com"
		message['To'] = email
		
		try:
			server = smtplib.SMTP()
			server.connect("smtp-mail.outlook.com", 587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login('', '')
			server.send_message(message)
			server.quit()
			
			print("{SENT}")
		except:
			print("{ERROR}")
	
	connection.close()
