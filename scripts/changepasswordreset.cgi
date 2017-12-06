#!/usr/bin/env python3

#Changes password of user that has given resetcode (Reset codes will have been sent by email to that user by request.)

import cgi
import pymysql
import random
import string
from argon2 import PasswordHasher

def randomValueGenerator(size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

formdata = cgi.FieldStorage()

resetcode = formdata.getvalue("resetcode")
newpass = formdata.getvalue("newpass")
userid = formdata.getvalue("userid")

print("Content-type: text/html; charset=UTF-8")
print()

if len(resetcode) > 10:
	connection = pymysql.connect(host="localhost", user="root", port=3306, cursorclass=pymysql.cursors.SSCursor)
	
	ph = PasswordHasher()
	newpasshash = ph.hash(newpass)
	
	cursor = connection.cursor()
	sql = "UPDATE bksis.usertable SET passhash=%s, salt='' WHERE resetcode=%s AND userid=%s"
	cursor.execute(sql, (newpasshash, resetcode, userid))
	cursor.close()
	
	cursor = connection.cursor()
	sql = "UPDATE bksis.usertable SET resetcode='' WHERE resetcode=%s"
	cursor.execute(sql, (resetcode))
	cursor.close()
	
	connection.commit()
	
	print("{SUCCESS}")
	
	connection.close()