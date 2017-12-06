#!/usr/bin/env python3

#Loads list of users

import cgi
import pymysql

formdata = cgi.FieldStorage()
session = formdata.getvalue('session')

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)

cursor = connection.cursor()
sql = "SELECT userid, username, role, groupname, email FROM usertable WHERE role='Administrator' AND session=%s"
cursor.execute(sql, (session))
response = cursor.fetchone()
cursor.close()

if response:
	role = response[3]
	useremail = "" + str(response[4]).replace("None", "")
	if role == "All":
		role = "Administrator"
	output = '''<tr userid="%s">
		<td>%s</td>
		<td>%s</td>
		<td>%s</td>
		<td></td>
		<td></td>
		</tr>
	''' % (response[0], response[1], useremail, role)
	cursor = connection.cursor()
	sql = "SELECT userid, username, role, groupname, email FROM usertable WHERE NOT userid=%s ORDER BY groupname, username"
	cursor.execute(sql, (response[0]))
	otherUsers = cursor.fetchall()
	cursor.close()
	
	if otherUsers:
		for user in otherUsers:
			useremail = "" + str(user[4]).replace("None", "")
			role = user[3]
			if role == "All":
				role = "Administrator"
			else:
				roleString = ""
				rolesplit = role.split(",")
				for eachrole in rolesplit:
					if len(roleString) > 0:
						roleString += ", "
					roleString += eachrole.capitalize()
				role = roleString
			output += '''<tr userid="%s">
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td style="width: 100px;text-align:center;"><button onclick="showEditUser(this);" userid="%s" class="btn cyan-btn"><i class="fa fa-pencil-square-o"></i> Rediger</button></td>
				<td style="width: 110px;text-align:center;"><button onclick="showDeleteUserConfirmation(this);" userid="%s" class="btn red-btn" style="width: 100px;"><i class="fa fa-trash-o fa-lg" aria-hidden="true"></i> Slett</button></td>
				</tr>
			''' % (user[0], user[1], useremail, role, user[0], user[0])
	
	print("Content-type: text/html; charset=UTF-8")
	print()
	print(output)

connection.close()