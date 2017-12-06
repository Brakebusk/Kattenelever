#!/usr/bin/env python3

import cgi
import pymysql
from html.parser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

formdata = cgi.FieldStorage()
postid =  formdata.getvalue("post")

title = "Kattenelever"
description = "En uoffisiell nettside for Kattens elever."
url = "https://kattenelever.no/"
ogtype = "website"
articleinfo = ""

if postid != None:
	connection = pymysql.connect(host="localhost", user="root", db="bksis", port=3306, cursorclass=pymysql.cursors.SSCursor)
	cursor = connection.cursor()
	sql = "SELECT title, content, creationtime, edittime, author, groupname FROM posts WHERE postid=%s"
	cursor.execute(sql, (postid))
	response = cursor.fetchone()
	cursor.close()
	connection.close()
	if response:
		title += " - " + response[0]
		description = strip_tags(response[1])[0:500]
		url += "?post=" + postid
		ogtype = "article"
		
		creationtime = response[2]
		if creationtime != None:
			creationtime = str(creationtime).replace(" ", "T") + "+01:00"
		
		edittime = response[3]
		if edittime != None:
			edittime = str(edittime).replace(" ", "T") + "+01:00"
			
		articleinfo = '''<meta property="article:published_time" content="%s">
		<meta property="article:author" content="%s">
		<meta property="article:section" content="%s">''' % (creationtime, response[4], response[5])
		if edittime != None:
			articleinfo += '<meta property="article:modified_time" content="%s">' % (edittime)

print("Content-type: text/html; charset=UTF-8")
print()

print('''
<!DOCTYPE html>
<html>
<head>
	<title>Kattenelever</title>
	<meta property="og:title" content="''' + title + '''">
	<meta name="description" content="''' + description + '''">
	<meta property="og:description" content="''' + description + '''">
	<meta property="og:url" content="''' + url + '''">
	<meta property="og:type" content="''' + ogtype + '''">
	''' + articleinfo + '''
	<meta charset="UTF-8">
	<link rel="stylesheet" href="../stylesheets/general_style.css" type="text/css">
	<link rel="stylesheet" href="../stylesheets/windowsizeadaptation.css" type="text/css">
	<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
	<link rel="shortcut icon" href="../media/favicon.png">
	<link rel="stylesheet" href="../stylesheets/font-awesome/css/font-awesome.min.css">
	<meta name="viewport" content="initial-scale=1.0, user-scalable=1">
	<meta property="fb:app_id" content="1189710891076496">
	<!--[if lt IE 9]>
		<script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.min.js"></script>
	<![endif]-->
	<script>
		if (window.location.protocol != "https:" && window.location.hostname != "localhost") {
			window.location.href = "https:" + window.location.href.substring(window.location.protocol.length);
		}
	</script>
</head>
<body onload="checkQuery();checkLogin();">
	<div id="fb-root"></div>
	<script>(function(d, s, id) {
	  var js, fjs = d.getElementsByTagName(s)[0];
	  if (d.getElementById(id)) return;
	  js = d.createElement(s); js.id = id;
	  js.src = "//connect.facebook.net/nb_NO/sdk.js#xfbml=1&version=v2.8";
	  fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));</script>
	<div id="overlay">
		<div id="shade"></div>
		<button id="close-overlay" onclick="closeOverlay();"><i class="fa fa-times"></i></button>
		<div class="information" id="information-success"><p><i class="fa fa-check fa-lg"></i> <span class="information-message"></span></p></div>
		<div class="information" id="information-warning"><p><i class="fa fa-exclamation-triangle fa-lg"></i> <span class="information-message"></span></p></div>
		<div class="information" id="information-loading"><p><i class="fa fa-refresh fa-spin fa-lg"></i> <span class="information-message"></span></p></div>
		<div class="panel" id="new-post-panel">
			<form action="javascript:submitPost()">
				<div id="new-post-panel-title">Nytt innlegg</div>
				<hr>
				<span>Tittel:</span><input id="new-post-input-title" type="text" required="required">
				<div style="margin-top: 10px;">
					<label><input type="checkbox" onchange="toggleEvent();" id="new-post-toggle-event">Lag et arrangement</label>
					<div style="margin-top: 5px;" id="create-event-container">
						<div class="new-input-group" style="display: inline-table;">
							<span class="new-input-group-title" style="width: 80px;">Start</span>
							<input type="date" id="new-event-field-startpoint-date" class="new-input-group-input" required="required" onchange="setStartDate();">
						</div>
						<input type="text" id="new-event-field-startpoint-time" class="time-input" required="required"><br>
						<div class="new-input-group" style="display: inline-table;">
							<span class="new-input-group-title" style="width: 80px;">Slutt</span>
							<input type="date" id="new-event-field-endpoint-date" class="new-input-group-input" required="required" onchange="this.setAttribute('changed', 'True');">
						</div>
						<input type="text" id="new-event-field-endpoint-time" class="time-input" required="required"><br>
						<div class="new-input-group" style="display: inline-table;margin-top: 5px;">
							<span class="new-input-group-title" style="width: 80px;">Sted</span>
							<input type="text" id="new-event-field-location" class="new-input-group-input">
						</div>
					</div>
				</div>
				<div id="new-post-content-container">
					<span>Innhold:</span>
					<textarea id="new-post-input-content"></textarea>
					<input type="file" style="display: none;" id="new-post-input-image">
				</div>
				<div style="text-align: right;margin-top: 10px;"><button id="new-post-submit" type="submit"><i class="fa fa-floppy-o"></i> Lagre</button></div>
			</form>
		</div>
		<div class="panel" id="edit-post-panel" postid="">
			<form action="javascript:editPost()">
				<div id="edit-post-panel-title">Rediger innlegg</div>
				<hr>
				<span>Tittel:</span><input id="edit-post-input-title" type="text" required="required">
				<div id="edit-post-content-container">
					<span>Innhold:</span>
					<textarea id="edit-post-input-content"></textarea>
				</div>
				<div style="text-align: right;margin-top: 10px;"><button id="edit-post-submit" type="submit"><i class="fa fa-floppy-o"></i> Lagre</button></div>
			</form>
		</div>
		<div class="panel" id="settings-panel">
			<form action="javascript:changepassword()">
				<div style="margin-bottom: 10px;">Endre bruker-passord:</div>
				<div class="new-input-group">
					<span class="new-input-group-title">Ditt gamle passord</span>
					<input id="input-old-password" type="password" required="required" class="new-input-group-input">
				</div>
				<div class="new-input-group">
					<span class="new-input-group-title">Nytt passord</span>
					<input id="input-new-password" type="password" required="required" class="new-input-group-input">
				</div>
				<div class="new-input-group">
					<span class="new-input-group-title">Bekreft nytt passord</span>
					<input id="input-confirm-new-password" type="password" required="required" class="new-input-group-input">
				</div>
				<button type="submit" class="confirm-btn"><i class="fa fa-floppy-o" aria-hidden="true"></i> Lagre</button>
				<span id="change-password-response"></span>
			</form>
			<form action="javascript:setEmail()" style="margin-top: 20px;">
				<div style="margin-bottom: 10px;">
					Endre E-postadresse:<br>
					<span style="font-size: 0.8em;">Brukes til passordgjenopprettelse ved glemt passord.</span>
				</div>
				<div class="new-input-group">
					<span class="new-input-group-title">E-postadresse</span>
					<input id="change-user-email" type="email" required="required" class="new-input-group-input">
				</div>
				<button type="submit" class="confirm-btn"><i class="fa fa-floppy-o" aria-hidden="true"></i> Lagre</button>
				<span id="change-email-response"></span>
			</form>
			<div id="usertable-wrap">
				<hr>
				<div style="margin-bottom: 10px;">Brukere:</div>
				<table id="usertable" style="width: 700px;">
					<tbody>
						<tr style="background-color: #bebebe;">
							<th>Brukernavn</th>
							<th>E-postadresse</th>
							<th>Tilgang</th>
							<th>Rediger</th>
							<th>Slett</th>
						</tr>
					</tbody>
					<tbody id="usertable-body"></tbody>
				</table>
				<div id="usertable-response"></div>
				<button onclick="closeOverlay();showOverlay();showPanel('new-user-panel');" class="confirm-btn" style="margin-top: 10px;"><i class="fa fa-plus-square" aria-hidden="true"></i> Ny bruker</button>
			</div>
		</div>
		<div class="panel" id="new-user-panel">
			<form action="javascript:createuser();">
				<div style="margin-bottom: 10px;">Ny bruker:</div>
				<div class="new-input-group">
					<span class="new-input-group-title" style="width: 90px;">Brukernavn</span>
					<input id="new-user-username" type="text" required="required" class="new-input-group-input" mplete="off">
				</div>
				<div class="new-input-group">
					<span class="new-input-group-title" style="width: 90px;">Passord</span>
					<input id="new-user-password" type="password" required="required" class="new-input-group-input">
				</div>
				<div class="new-input-group">
					<span class="new-input-group-title" style="width: 90px;">E-postadresse</span>
					<input id="new-user-email" type="email" class="new-input-group-input">
				</div>
				Brukertype:
				<select id="new-user-role" class="nice-select" style="margin-bottom: 10px;" onchange="toggleUserType();">
					<option value="User">Bruker</option>
					<option value="Administrator">Administrator</option>
				</select>
				<div id="new-user-access-container">
					Tilgang:<br>
					<input value="elevrådet" type="checkbox" id="new-user-check-elevrådet"><label for="new-user-check-elevrådet">Elevrådet</label><br>
					<input value="hugin" type="checkbox" id="new-user-check-hugin"><label for="new-user-check-hugin">Hugin</label><br>
					<input value="skoleavisen" type="checkbox" id="new-user-check-skoleavisen"><label for="new-user-check-skoleavisen">Skoleavisen</label><br>
					<input value="revyen" type="checkbox" id="new-user-check-revyen"><label for="new-user-check-revyen">Revyen</label><br>
					<input value="sos" type="checkbox" id="new-user-check-sos"><label for="new-user-check-sos">SOS Barnebyer</label><br>
					<input value="nu" type="checkbox"id="new-user-check-nu"><label for="new-user-check-nu">Natur og Ungdom</label>
				</div>
				<li class="small-divider" style="margin-bottom: 10px;"></li>
				<button class="btn green-btn"><i class="fa fa-floppy-o" aria-hidden="true"></i> Lagre</button>
				<button type="button" class="btn red-btn" onclick="closeOverlay();showOverlay();showPanel('settings-panel');"><i class="fa fa-times" aria-hidden="true"></i> Avbryt</button>
				<div id="new-user-response"></div>
			</form>
		</div>
		<div class="panel" id="sidepanel-settings">
			<form action="javascript:submitpaneledit()" id="sidepanel-edit-form">
				<div id="sidepanel-edit-title">Rediger info-panelet:</div>
				<hr>
				<span>Tittel:</span><input id="sidepanel-input-title" type="text" required="required">
				<div id="sidepanel-edit-image-container">
					Tittelbilde: <input type="file" id="sidepanel-edit-image-file" accept="image/*"><br>
					<img id="sidepanel-edit-image-preview" newimage="false">
				</div>
				<div id="sidepanel-edit-content-container">
					<span>Innhold:</span>
					<textarea id="sidepanel-input-content"></textarea>
				</div>
				<div style="text-align: right;margin-top: 10px;"><button id="sidepanel-edit-submit" type="submit">Rediger</button></div>
			</form>
		</div>
		<div class="panel" id="confirm-delete-panel" postid="">
			Er du sikker på at du vil slette dette inlegget?
			<hr>
			<button class="btn red-btn" onclick="deletePost()"><i class="fa fa-trash-o fa-lg" aria-hidden="true"></i> Slett</button>
			<button class="btn green-btn" onclick="closeOverlay();"><i class="fa fa-times" aria-hidden="true"></i> Avbryt</button>
		</div>
		<div class="panel" id="edit-user-panel" userid="">
			<div id="edit-user-panel-title">Rediger bruker: <span id="edit-user-panel-username"></span></div>
			<hr>
			<form action="javascript:setUserPassword()">
				<div style="margin-bottom: 10px;">Sett nytt brukerpassord:</div>
				<div class="new-input-group">
					<span class="new-input-group-title" style="width: 90px;">Nytt passord</span>
					<input id="edit-user-password" type="password" class="new-input-group-input" required="required">
				</div>
				<button type="submit" class="confirm-btn"><i class="fa fa-floppy-o" aria-hidden="true"></i> Lagre</button>
				<span id="edit-user-password-response"></span>
			</form>
		</div>
	</div>
	<header>
		<div id="login-wrap">
			<span id="loggedinas">
				<span id="loginastext-container">Logget inn som: <span id="loggedinastext" access=""></span></span>
				<button id="logout" onclick="logout();"><i class="fa fa-sign-out"></i> Logg ut</button>
			</span>
			<button id="login" onclick="navtologin();"><i class="fa fa-sign-in"></i> Logg inn</button>
			<div id="settings-button-wrap"><button id="show-settings" onclick="showOverlay();showPanel('settings-panel');"><i class="fa fa-cog"></i> Instillinger</button></div>
		</div>
		<h1>Kattenelever</h1>
		<h2>En uoffisiell nettside for Kattens elever</h2>
		<hr id="navigation-separator">
		<div id="navigation">
			<ul id="navigation-list">
				<li><a class="selected" onclick="selectSection('all');" section="all" groupname="None">Forsiden</a></li>
				<li><a class="" onclick="selectSection('elevrådet');" section="elevrådet" groupname="Elevrådet">Elevrådet</a></li>
				<li><a class="" onclick="selectSection('hugin');" section="hugin" groupname="Hugin">Hugin</a></li>
				<li><a class="" onclick="selectSection('skoleavisen');" section="skoleavisen" groupname="Skoleavisen">Skoleavisen</a></li>
				<li><a class="" onclick="selectSection('revyen');" section="revyen" groupname="Revyen">Revyen</a></li>
				<li><a class="" onclick="selectSection('sos');" section="sos" groupname="SOS">SOS Barnebyer</a></li>
				<li><a class="" onclick="selectSection('nu');" section="nu" groupname="nu">Natur og Ungdom</a></li>
			</ul>
		</div>
	</header>
	<div id="main-area" open="true">
		<div id="new-post-section">
			<button id="new-post-button" onclick="showOverlay();showPanel('new-post-panel');"><i class="fa fa-pencil-square-o"></i> Nytt innlegg</button><br id="new-post-section-newline">
		</div>
		<div id="sidepanel">
			<div id="sidepanel-container" onclick="toggleSidepanel();">
				<div id="sidepanel-title-container">
					<i id="plus-sidepanel" class="fa fa-plus" title="Vis informasjon"></i>
					<i id="minus-sidepanel" class="fa fa-minus" title="Skjul informasjon"></i>
					<span id="sidepanel-title"></span>
					<a id="sidepanel-edit-button" onclick="showOverlay();showPanel('sidepanel-settings');">Rediger</a>
				</div>
				<div id="sidepanel-content-container" class="">
					<hr>
					<div id="sidepanel-image-container">
						<img id="sidepanel-image" src="">
					</div>
					<hr id="sidepanel-divider-second">
					<div id="sidepanel-description"></div>
				</div>
			</div>
			<div id="calendar">
				<span id="calendar-title">Kalender</span>
				<hr>
				<span style="font-size: 1.1em;">Uke <span id="calendar-week"></span> <span id="calendar-year"></span>:</span><span id="calendar-week-select-container"><button class="calendar-week-select" onclick="changeCalendarWeek(-1);">&lt;</button><button class="calendar-week-select" onclick="changeCalendarWeek(1);">&gt;</button></span>
				<div id="calendar-container">
					<table id="calendar-table"></table>
				</div>
			</div>
		</div>
		<hr id="section-divider" style="opacity: 0">
		<div id="post-section"></div>
	</div>
	<div id="inspect-post" open="false">
		<div id="inspect-post-container"></div>
		<div id="post-comment-container">
			<a name="comments"></a>
			<div id="post-comments">
			</div>
		</div>
	</div>
	<footer>
		<a href="https://github.com/Brakebusk/Kattenelever">Source code</a>
	</footer>
	<script src="../scripts/moment-with-locales.min.js"></script>
	<script src="//cdn.tinymce.com/4/tinymce.min.js"></script>
	<script src="scripts.js"></script>
	<script>
		tinymce.init({
			selector: "textarea",  // change this value according to your HTML
			plugins: "autolink image link",
			file_picker_callback: function(callback, value, meta) {
				if (meta.filetype == 'image') {
					document.getElementById("new-post-input-image").click();
					document.getElementById("new-post-input-image").onchange = function() {
						var file = this.files[0];
						var reader = new FileReader();
						reader.onload = function(e) {
							var session = getCookie('session');
							var datastring = e.target.result;
							
							session = encodeURIComponent(session.trim());
							datastring = encodeURIComponent(datastring.trim());
							
							callback('Laster...', {
										alt: ''
									});	
							var xhttp = new XMLHttpRequest();
							xhttp.onreadystatechange = function() {
								if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{SUCCESS}") != -1) {
									callback("/media/postimages/" + xhttp.responseText.split("§")[1], {
										alt: ''
									});	
								} else if (xhttp.readyState == 4) {
									callback("Upload Error", {
										alt: ''
									});	
								}
							};
							xhttp.open("POST", "/scripts/uploadimage.cgi",true);
							xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
							xhttp.send("session=" + session + "&datastring=" + datastring);
						};
						reader.readAsDataURL(file);
					};
				}
			},
			file_picker_types: 'image',
			height: "440"
		});
	</script>
</body>
</html>''')