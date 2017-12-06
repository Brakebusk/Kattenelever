#!/usr/bin/env python3

#Loads post for the selected section

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')
section = formdata.getvalue('section')

try:
	page = int(formdata.getvalue('page')) - 1
except:
	page = 0
	
if page < 0:
	page = 0

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
	
	#get total count of posts within selected section (used to decide if relevant to show "next page" button):
	cursor = connection.cursor()
	if section != 'all':
		sql = "SELECT COUNT(*) FROM posts WHERE groupname=%s AND type='post'"
		cursor.execute(sql, (section))
	else:
		sql = "SELECT COUNT(*) FROM posts WHERE type='post'"
		cursor.execute(sql)
	print("<postcount>" + str(cursor.fetchone()[0]) + "</postcount>")
	cursor.close()
	
	cursor = connection.cursor()
	if section != 'all':
		sql = "SELECT * FROM posts WHERE groupname=%s AND type='post' ORDER BY creationtime DESC LIMIT 15 OFFSET %s"
		cursor.execute(sql, (section, page * 15))
	else:
		sql = "SELECT * FROM posts WHERE type='post' ORDER BY creationtime DESC limit 15 OFFSET %s"
		cursor.execute(sql, (page * 15))
	response = cursor.fetchall()
	if not response:
		print("{NONE}")
	else:
		for row in response:
			print("<post>")
			print("<id>%s</id>" % (str(row[0])))
			print("<title>%s</title>" % (str(row[1])))
			print("<content>%s</content>" % (str(row[2])))
			print("<creationtime>%s</creationtime>" % (str(row[3])))
			print("<edittime>%s</edittime>" % (str(row[4])))
			print("<author>%s</author>" % (str(row[5])))
			print("<group>%s</group>" % (str(row[6])))
			canedit = 'false'
			if str(row[6]) == str(usergroup) or usergroup == 'All':
				canedit = 'true'
			print("<canedit>%s</canedit>" % (canedit))
			print("<type>post</type>")
			print("</post>")
	cursor.close()
	connection.close()
except Exception as e:
	print("{ERROR}")