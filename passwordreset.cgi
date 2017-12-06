#!/usr/bin/env python3

import cgi
import pymysql

print("Content-type: text/html; charset=UTF-8")
print()

print('''<!DOCTYPE html>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Kattenelever - Reset passord</title>
		<link rel="shortcut icon" href="../media/favicon.png">
		<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
		<style>
			body {
				text-align: center;
				font-family: 'Open Sans';
			}
			input {
				margin-bottom: 10px;
			}
			#selectUserid {
				height: 30px;
			}
		</style>
	</head>
	<body>
	''')
try:
	formdata = cgi.FieldStorage()
	resetcode = formdata.getvalue("resetcode")
except:
	print("Ugyldig kode...")

if len(resetcode) > 10:
	connection = pymysql.connect(host="localhost", user="root", port=3306, cursorclass=pymysql.cursors.SSCursor)
	cursor = connection.cursor()
	sql = "SELECT username, userid FROM bksis.usertable WHERE resetcode=%s"
	cursor.execute(sql, (resetcode))
	response = cursor.fetchall()
	cursor.close()
	connection.close()
	
	if response:
		useridlist = ""
		for user in response:
			useridlist += "<option userid='%s'>%s</option>" % (user[1], user[0])
			
		print("<h1>Sett nytt passord for: <select id='selectUserid'>" + useridlist + "</select></h1>")
		print('''
			Nytt passord: <input type="password" id="newpassword"><br>
			Bekreft nytt passord: <input type="password" id="newpassconfirm"><br>
			<button onclick="setNew()">Endre passord</button>
			<h3 id="response"></h3>
			<script>
				function setNew() {
					var newpass = document.getElementById("newpassword").value;
					var newpassConfirm = document.getElementById("newpassconfirm").value;
					
					var selector = document.getElementById("selectUserid");
					var userid = selector.options[selector.selectedIndex].getAttribute("userid");
					
					var responseField = document.getElementById("response");
					if (newpass == newpassConfirm && newpass != "") {
						var xhttp = new XMLHttpRequest();
						xhttp.onreadystatechange = function() {
						if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{SUCCESS}") > -1) {
							responseField.textContent = "Passord endret";
						} else if (xhttp.readyState == 4) {
							responseField.textContent = "Det skjedde en feil...";
						}
						};
						xhttp.open("POST", "/scripts/changepasswordreset.cgi", true);
						xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
						xhttp.send("userid=" + userid + "&resetcode=%s&newpass=" + newpass);	
					} else {
						responseField.textContent = "De to feltene matcher ikke.";
					}	
				}
			</script>
			''' % (resetcode))
	else:
		print("Ugyldig kode...")
else:
	print("Ugyldig kode...")


print("</body></html>")