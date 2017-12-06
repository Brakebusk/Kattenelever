#!/usr/bin/env python3

#Loads the information for a selected post (Used when inspecting a single post)

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
postid = formdata.getvalue('postid')

print("Content-type: text/html; charset=UTF-8")
print()

try:
	connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
	usergroup = None
	if session != 'none':
		cursor = connection.cursor()
		sql = "SELECT groupname FROM usertable WHERE session=%s"
		cursor.execute(sql, (session))
		checkresp = cursor.fetchone()
		if checkresp:
			usergroup = checkresp[0]
		cursor.close()
	
	cursor = connection.cursor()
	sql = "SELECT * FROM posts WHERE postid=%s"
	cursor.execute(sql, (postid))
	response = cursor.fetchone()
	if not response:
		print("{NONE}")
	else:
		print("<post>")
		print("<id>%s</id>" % (str(response[0])))
		print("<title>%s</title>" % (str(response[1])))
		print("<content>%s</content>" % (str(response[2])))
		print("<creationtime>%s</creationtime>" % (str(response[3])))
		print("<edittime>%s</edittime>" % (str(response[4])))
		print("<author>%s</author>" % (str(response[5])))
		print("<group>%s</group>" % (str(response[6])))
		canedit = 'false'
		if str(response[6]) == str(usergroup) or usergroup == 'All':
			canedit = 'true'
		print("<canedit>%s</canedit>" % (canedit))
		print("<type>%s</type>" % (response[7]))
		print("<startpoint>%s</startpoint>" % (response[8]))
		print("<endpoint>%s</endpoint>" % (response[9]))
		print("<location>%s</location>" % (response[10]))
		print("</post>")		
	cursor.close()
	connection.close()
except Exception as e:
	print("{ERROR}")