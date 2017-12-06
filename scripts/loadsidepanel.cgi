#!/usr/bin/env python3

#Loads side panel information for the selected section

import cgi
import pymysql

formdata = cgi.FieldStorage()
section = formdata.getvalue('section')

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

print("Content-type: text/html; charset=UTF-8")
print()

cursor = connection.cursor()
sql = "SELECT sidepaneltitle, description, groupimage FROM groups WHERE groupname=%s"
cursor.execute(sql, (section))
response = cursor.fetchone()
if response:
	print("""
		  <title>%s</title>
		  <description>%s</description>
		  <titleimage>%s</titleimage>
		  """ % (response[0], response[1], response[2]))
cursor.close()
connection.close()