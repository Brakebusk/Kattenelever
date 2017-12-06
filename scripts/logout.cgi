#!/usr/bin/env python3

#Remove session token from account at logout

import cgi
import pymysql

response = cgi.FieldStorage()
session = response.getvalue("session")

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
with connection.cursor() as cursor:
	sql = "UPDATE usertable SET session='' WHERE session=%s"
	cursor.execute(sql, (session))
	connection.commit()
	cursor.close()
connection.close()