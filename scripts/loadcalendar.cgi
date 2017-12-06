#!/usr/bin/env python3

#Loads the calendar for the selected section

import cgi
import pymysql
import datetime

formdata = cgi.FieldStorage()

week = formdata.getvalue("week")
year = formdata.getvalue("year")
section = formdata.getvalue("section")

print("Content-type: text/html; charset=UTF-8")
print()

searchStartpoint = datetime.datetime.strptime(str(year) + "-" + str(week) + "-1", "%Y-%W-%w")
searchEndpoint = searchStartpoint + datetime.timedelta(days = 7)

connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
cursor = connection.cursor()
sql = "SELECT * FROM posts WHERE type='event' AND startpoint > %s AND startpoint < %s AND groupname=%s ORDER BY startpoint ASC"
cursor.execute(sql, (searchStartpoint.strftime("%Y-%m-%d %H:%M:%S"), searchEndpoint.strftime("%Y-%m-%d %H:%M:%S"), section))
response = cursor.fetchall()
cursor.close()

output = ""

for event in response:
	eventId = event[0]
	eventTitle = event[1]
	eventDescription = event[2]
	eventStartpoint = event[8]
	eventEndpoint = event[9]
	
	output += "<event>"
	output += "<eventid>%s</eventid>" % (eventId)
	output += "<title>%s</title>" % (eventTitle)
	output += "<description>%s</description>" % (eventDescription)
	output += "<startpoint>%s</startpoint>" % (eventStartpoint)
	output += "<endpoint>%s</endpoint>" % (eventEndpoint)
	
	output += "</event>"

print(output)

connection.close()