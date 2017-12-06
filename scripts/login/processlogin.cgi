#!/usr/bin/env python3

#Cheks if user has provided valid login information

import cgi
import os
import http.cookies
import string
import random
import pymysql
from datetime import datetime
from urllib import parse
from argon2 import PasswordHasher

formdata = cgi.FieldStorage()
username = formdata.getvalue("username")
password = formdata.getvalue("password")

def randomValueGenerator(size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

authenticated = False

cookie = http.cookies.SimpleCookie() #Will store session token

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

cursor = connection.cursor()
sql = "SELECT userid FROM usertable WHERE BINARY username=%s"
cursor.execute(sql, (username))
response = cursor.fetchone()
cursor.close()

if response: #username/school combo exists
	userid = response[0] #account userid
	
	cursor = connection.cursor()
	sql = "SELECT passhash FROM usertable WHERE userid=%s"
	cursor.execute(sql, (userid))
	server_passhash = cursor.fetchone()[0]
	cursor.close()
	
	ph = PasswordHasher()
	try:
		if ph.verify(server_passhash, password):
			authenticated = True
	except:
		authenticated = False
	
	if authenticated:
		#generate cookie
		sessionvalue = randomValueGenerator(64)
		cookie["session"] = sessionvalue #cookie["session"] will also be stored in userdb -> session
		cursor = connection.cursor()
		sql = "UPDATE usertable SET session=%s WHERE userid=%s"
		cursor.execute(sql, (sessionvalue, userid))
		cursor.close()
		connection.commit()
		cookie["session"]["path"] = "/"
		cookie["session"]["expires"] = ""
	
connection.close()

if authenticated:
	print("Content-type: text/html; charset=UTF-8")
	print(cookie.output())
	print()
	print("{SUCCESS}")
else:
	print("Content-type: text/html; charset=UTF-8")
	print()
	print("{FAILURE}")