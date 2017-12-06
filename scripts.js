//Main page script file
moment.locale("nb");
var selectedSection = "all";
function selectSection(section) {
    //Called when user clicks a section title in nav bar. Will load appropriate posts, sidebar, etc.

    selectedSection = section;
    
    if (selectedSection != 'all') {
        document.getElementById("section-divider").style.opacity = "1";
    } else {
        document.getElementById("section-divider").style.opacity = "0";
    }
    
    var list = document.getElementById("navigation-list").getElementsByTagName("li");
    for (i = 0; i < list.length; i++) {
        var anchor = list[i].getElementsByTagName("a")[0];
        if (anchor.getAttribute("section") != section) {
            anchor.className = "";
        } else {
            anchor.className = "selected";
            var access = document.getElementById("loggedinastext").getAttribute("access");
            if ((access.split(",").indexOf(selectedSection) > -1 || access == "All") && selectedSection != "all") {
                document.getElementById("new-post-section").style.display = "block";
                document.getElementById("sidepanel-edit-button").style.display = "block";
            } else {
                document.getElementById("new-post-section").style.display = "";
                document.getElementById("sidepanel-edit-button").style.display = "";
            }
        }
    }
    section = encodeURIComponent(section);
    if (history.pushState) {
        var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?section=" + section;
        window.history.pushState({path:newurl},'',newurl);
    }
    document.getElementById("main-area").style.display = "";
    document.getElementById("inspect-post").style.display = "";
    document.getElementById("main-area").setAttribute("open", "true");
    document.getElementById("inspect-post").setAttribute("open", "false");
    loadSidebar();
    loadPosts();
    loadCalendar(moment().format("YYYY"), moment().format("W"));
}
function showMessage(type, message) {
    //Shows information message

    showOverlay();
    var element = document.getElementById("information-" + type);
    element.getElementsByClassName("information-message")[0].textContent = message;
    element.className = "information showinfo";
}
function hideMessage(type) {
    //Hides information message

    var element = document.getElementById("information-" + type);
    element.className = "information";
}
function toggleSidepanel() {
    //When at low window width mode, this can be called using a button. This script will toggle the sidepanel dropdown.

    if (window.innerWidth < 1700) {
        var contentblock = document.getElementById("sidepanel-content-container");
        var plustingy = document.getElementById("plus-sidepanel");
        var minustingy = document.getElementById("minus-sidepanel");
        if (contentblock.className == "showblock") {
            contentblock.className = "";
            plustingy.className = "fa fa-plus showinline";
            minustingy.className = "fa fa-minus hideinline";
        } else {
            contentblock.className = "showblock";
            plustingy.className = "fa fa-plus hideinline";
            minustingy.className = "fa fa-minus showinline";
        }
    }
}
function selectPost(postid) {
    //Called when user clicks on a post. Page will now be directed to inspecting said post (showing comment section and stuff)

    document.getElementById("main-area").setAttribute("open", "false");
    document.getElementById("inspect-post").setAttribute("open", "true");
    
    var cmtContainer = document.getElementById("post-comments");
    cmtContainer.innerHTML = "";
    if (history.pushState) {
        var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?post=" + postid;
        window.history.pushState({path:newurl},'',newurl);
    }
    document.getElementById("main-area").style.display = "none";
    document.getElementById("inspect-post").style.display = "block";
    
    var session = getCookie('session');
    if (session === "") {session = "none";}
    
    var postSection = document.getElementById("inspect-post-container");
    postSection.innerHTML = '<i class="fa fa-refresh fa-spin"></i> Laster innlegg..';
    postSection.style.textAlign = "center";
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            postSection.style.textAlign = "";
            displayPosts(xhttp.responseText, "inspect-post-container", true);
            cmtContainer.innerHTML = '<div class="fb-comments" data-href="' + [location.protocol, '//', location.host, location.search.split("&")[0]].join('') + '" data-numposts="5" data-width="100%"></div>';
            FB.XFBML.parse(cmtContainer);
        } else if (xhttp.readyState == 4) {
            postSection.innerHTML = '<i class="fa fa-frown-o"></i> Kunne ikke laste inn innlegg..';
        }
    };
    xhttp.open("GET", "/scripts/loadsinglepost.cgi?session=" + session + "&postid=" + postid,true);
    xhttp.send();
}
function checkQuery() {
    //takes the url query and shows the appropriate site content

    if (getParameterByName("section") !== null) {
        selectedSection = getParameterByName("section");
        
        if (selectedSection != 'all') {
            document.getElementById("section-divider").style.opacity = "1";
        }

        var list = document.getElementById("navigation-list").getElementsByTagName("li");
        for (i = 0; i < list.length; i++) {
            var anchor = list[i].getElementsByTagName("a")[0];
            if (anchor.getAttribute("section") != selectedSection) {
                anchor.className = "";
            } else {
                anchor.className = "selected";
            }
        }
        
        document.getElementById("main-area").style.display = "";
        document.getElementById("inspect-post").style.display = "";
        document.getElementById("main-area").setAttribute("open", "true");
        document.getElementById("inspect-post").setAttribute("open", "false");
        
        loadSidebar();
        loadPosts();
        loadCalendar(moment().format("YYYY"), moment().format("W"));
    } else if (getParameterByName("post") !== null) {
        selectPost(getParameterByName("post"));
    } else {
        loadSidebar();
        loadPosts();
        loadCalendar(moment().format("YYYY"), moment().format("W"));
    }
}
function loadSidebar() {
    //loads the relevant sidebar information for the current section

    var sidepanel = document.getElementById("sidepanel");
    if (selectedSection == "all") {
        sidepanel.style.display = "";
    } else {				
        var section = selectedSection; //determines what sidebar to get, ex: "hugin" or "skoleavisen"
        section = encodeURIComponent(section.trim());
        
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var parser = new DOMParser();
                xmlDoc = parser.parseFromString(xhttp.responseText, "text/html");
                document.getElementById("sidepanel-title").innerHTML = xmlDoc.querySelector("title").textContent;
                
                var imageSrc = xmlDoc.querySelector("titleimage").textContent;
                if (imageSrc !== "None") {
                    document.getElementById("sidepanel-image").src = "../media/titleimages/" + imageSrc;
                    document.getElementById("sidepanel-image-container").style.display = "";
                    document.getElementById("sidepanel-divider-second").style.display = "";
                } else {
                    document.getElementById("sidepanel-image").src = "";
                    document.getElementById("sidepanel-image-container").style.display = "none";
                    document.getElementById("sidepanel-divider-second").style.display = "none";
                }
                document.getElementById("sidepanel-description").innerHTML = xmlDoc.querySelector("description").innerHTML;
                sidepanel.style.display = "block";
            }
        };
        xhttp.open("GET", "/scripts/loadsidepanel.cgi?section=" + section,true);
        xhttp.send();
    }
}
function closeOverlay() {
    //Closes panel overlay (When in settings menu/creating a post/etc.)

    var overlay = document.getElementById("overlay");
    overlay.style.display = "";
    var panels = overlay.getElementsByClassName("panel");
    for (i = 0; i < panels.length; i++) {
        panels[i].style.display = "";
        panels[i].className = "panel";
    }			
}
function showOverlay() {
    //Shows the panel overlay with its' shadow overlay

    var overlay = document.getElementById("overlay");
    overlay.style.display = "block";
}
function showPanel(panelId) {
    //Shows the selected panel (Settings panel/Create post panel/Edit post panel/Etc.)

    if (panelId == "sidepanel-settings") {
        var titleInput = document.getElementById("sidepanel-input-title");
        var imagePreview = document.getElementById("sidepanel-edit-image-preview");
        
        titleInput.value = document.getElementById("sidepanel-title").innerHTML;
        tinyMCE.get("sidepanel-input-content").setContent(document.getElementById("sidepanel-description").innerHTML);
        var previewSrc = document.getElementById("sidepanel-image").getAttribute("src");
        if (previewSrc === "") {
            imagePreview.style.display = "none";
        } else {
            imagePreview.style.display = "";
        }
        imagePreview.style.backgroundImage = "url(" + document.getElementById("sidepanel-image").getAttribute("src") + ")";
    } else if (panelId == "settings-panel") {
        loaduserinformation();
        if (document.getElementById("loggedinastext").getAttribute("access") == "All") {
            document.getElementById("usertable-wrap").style.display = "";
            
            loadusertable();
        } else {
            document.getElementById("usertable-wrap").style.display = "none";
        }
    } else if (panelId == "new-user-panel") {
        document.getElementById("new-user-username").value = "";
        document.getElementById("new-user-password").value = "";
    } else if (panelId == "new-post-panel") {
        var startpoint = moment();
        document.getElementById("new-event-field-startpoint-date").value = startpoint.format("YYYY-MM-DD");
        document.getElementById("new-event-field-startpoint-time").value = startpoint.format("HH:mm");
        startpoint.add(1, "hours");
        document.getElementById("new-event-field-endpoint-date").value = startpoint.format("YYYY-MM-DD");
        document.getElementById("new-event-field-endpoint-time").value = startpoint.format("HH:mm");
        document.getElementById("new-event-field-endpoint-date").setAttribute("changed", "False");
        document.getElementById("new-event-field-location").value = "";
        var checkbox = document.getElementById("new-post-toggle-event");
        if (checkbox.checked) {
            checkbox.checked = false;
            toggleEvent();
        }
    } else if (panelId == "edit-user-panel") {
        var settingsp = document.getElementById("settings-panel");
        settingsp.style.display = "";
        settingsp.className = "panel";
        document.getElementById("edit-user-password").value = "";
        document.getElementById("edit-user-password-response").innerHTML = "";
    }
    
    var panel = document.getElementById(panelId);
    panel.style.display = "block";
    setTimeout(function(){
        panel.className += " show";
    }, 100);
}
function showEditUser(button) {
    //Will retrieve relevant user information when the user is about to edit a user's information

    var userid = button.getAttribute("userid");
    var panel = document.getElementById("edit-user-panel");
    panel.setAttribute("userid", userid);
    
    var rows = document.getElementById("usertable-body").getElementsByTagName("tr");
    for (i = 0; i < rows.length; i++) {
        if (rows[i].getAttribute("userid") == userid) {
            document.getElementById("edit-user-panel-username").textContent = rows[i].getElementsByTagName("td")[0].textContent;
            break;
        }
    }
    showPanel("edit-user-panel");
}
function setUserPassword() {
    //Sets a new password for selected user

    var panel = document.getElementById("edit-user-panel");
    var userid = panel.getAttribute("userid");
    var newpass = document.getElementById("edit-user-password").value;
    
    var responseField = document.getElementById("edit-user-password-response");
    responseField.innerHTML = "";
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{SUCCESS}") > -1) {
            responseField.innerHTML = "Nytt passord lagret.";
        } else if (xhttp.readyState == 4) {
            responseField.innerHTML = "FEIL! Nytt passord ikke lagret.";
        }
    };
    xhttp.open("GET", "/scripts/setuserpassword.cgi?session=" + getCookie('session') + "&userid=" + encodeURIComponent(userid.trim()) + "&newpass=" + encodeURIComponent(newpass.trim()),true);
    xhttp.send();
}
function setStartDate() {
    //If the endField when creating an event has not previously been set by the user, set it to the same as the now set startField

    var startField = document.getElementById("new-event-field-startpoint-date");
    var endField = document.getElementById("new-event-field-endpoint-date");

    if (endField.getAttribute("changed") == "False") endField.value = startField.value;
}
function loaduserinformation() {
    //Loads user information for settings panel. Currently only retrieves email address.

    var emailfield = document.getElementById("change-user-email");
    emailfield.value = "";
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var response = xhttp.responseText;
            emailfield.value = response;
        }
    };
    xhttp.open("GET", "/scripts/loaduserinfo.cgi?session=" + getCookie('session'),true);
    xhttp.send();
}
function loadusertable() {
    //Loads the list of users in the settings panel

    document.getElementById("usertable-response").innerHTML = "";
    
    var tablebody = document.getElementById("usertable-body");
    tablebody.innerHTML = "";
    
    
    var session = getCookie('session');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            tablebody.innerHTML = xhttp.responseText;
        } else if (xhttp.readyState == 4) {
            document.getElementById("usertable-response").innerHTML = "Fikk ikke lastet inn brukertabell.";
        }
    };
    xhttp.open("GET", "/scripts/loadusertable.cgi?session=" + session,true);
    xhttp.send();
}
function showEditPanel(postid) {
    //Shows the edit post panel

    var allPosts = document.getElementsByClassName('post');
    for (i = 0; i < allPosts.length; i++) {
        if (allPosts[i].getAttribute("postid") == postid) {
            document.getElementById("edit-post-input-title").value = allPosts[i].getElementsByClassName("post-title")[0].innerHTML;
            tinyMCE.get("edit-post-input-content").setContent(allPosts[i].getElementsByClassName("post-body")[0].innerHTML);
            document.getElementById("edit-post-panel").setAttribute("postid", postid);
            showOverlay();
            showPanel('edit-post-panel');
            break;
        }
    }
}
function toggleEvent() {
    //Toggles is new post should either be a normal post or event

    var checkbox = document.getElementById("new-post-toggle-event");
    if (checkbox.checked) {
        document.getElementById("create-event-container").style.display = "block";
    } else {
        document.getElementById("create-event-container").style.display = "";
    }
}
function submitPost() {
    //Submit new post to the server

    document.getElementById("new-post-panel").style.display = "";
    showMessage('loading', "Laster");
    
    var session = getCookie('session');
    var title = document.getElementById("new-post-input-title").value;
    //var content = document.getElementById("new-post-input-content").value;
    var content = tinyMCE.get('new-post-input-content').getContent();
    var group = document.getElementsByClassName("selected")[0].getAttribute("groupname");
    var postType = "post";
    if (document.getElementById("new-post-toggle-event").checked) {
        postType = "event";
    }
    var startpoint = document.getElementById("new-event-field-startpoint-date").value + " " + document.getElementById("new-event-field-startpoint-time").value + ":00";
    var endpoint = document.getElementById("new-event-field-endpoint-date").value + " " + document.getElementById("new-event-field-endpoint-time").value + ":00";
    var location = document.getElementById("new-event-field-location").value;
    
    session = encodeURIComponent(session.trim());
    title = encodeURIComponent(title.trim());
    content = encodeURIComponent(content.trim());
    group = encodeURIComponent(group.trim());
    postType = encodeURIComponent(postType.trim());
    startpoint = encodeURIComponent(startpoint.trim());
    endpoint = encodeURIComponent(endpoint.trim());
    location = encodeURIComponent(location.trim());
    if (location === "") location = "none";
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{SUCCESS}") != -1) {
            hideMessage('loading');
            showMessage('success', "Innlegg lagret");
            document.getElementById("new-post-input-title").value = "";
            tinyMCE.get('new-post-input-content').setContent('');
            loadPosts();
            loadCalendar(document.getElementById("calendar-year").textContent, document.getElementById("calendar-week").textContent);
            setTimeout(function(){
                hideMessage('success');
                closeOverlay();
            }, 1500);
        } else if (xhttp.readyState == 4) {
            hideMessage('loading');
            showMessage('warning', "Innlegg ble ikke lagret");
            setTimeout(function(){
                hideMessage('warning');
                document.getElementById("new-post-panel").style.display = "block";
            }, 1500);
        }
    };
    if (session !== "") {
        xhttp.open("POST", "/scripts/submitpost.cgi",true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("session=" + session + "&title=" + title + "&content=" + content + "&group=" + group + "&type=" + postType + "&startpoint=" + startpoint + "&endpoint=" + endpoint + "&location=" + location);
    }
}
function editPost() {
    //sends new content for edited post to the server

    document.getElementById("edit-post-panel").style.display = "";
    showMessage('loading', "Laster");
    
    var session = getCookie('session');
    var title = document.getElementById("edit-post-input-title").value;
    //var content = document.getElementById("edit-post-input-content").value;
    var content = tinyMCE.get('edit-post-input-content').getContent();
    var postid = document.getElementById("edit-post-panel").getAttribute("postid");
    
    session = encodeURIComponent(session.trim());
    title = encodeURIComponent(title.trim());
    content = encodeURIComponent(content.trim());
    postid = encodeURIComponent(postid.trim());
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{SUCCESS}") != -1) {
            hideMessage('loading');
            showMessage('success', "Innlegg lagret");
            if (document.getElementById("inspect-post").getAttribute("open") == "true") {
                selectPost(document.getElementById("inspect-post-container").getElementsByClassName('post')[0].getAttribute("postid"));
            } else {
                loadPosts();	
            }
            setTimeout(function(){
                hideMessage('success');
                closeOverlay();
            }, 1500);
        } else if (xhttp.readyState == 4) {
            hideMessage('loading');
            showMessage('warning', "Innlegg ble ikke lagret");
            setTimeout(function(){
                hideMessage('warning');
                document.getElementById("edit-post-panel").style.display = "block";
            }, 1500);
        }
    };
    if (session !== "") {
        xhttp.open("POST", "/scripts/editpost.cgi",true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("session=" + session + "&title=" + title + "&content=" + content + "&postid=" + postid);	
    }
}
function submitpaneledit() {
    //Changes sidepanel content for a particular section.

    document.getElementById("sidepanel-settings").style.display = "";
    showMessage('loading', "Laster");
    
    var session = getCookie('session');
    var titleInput = document.getElementById("sidepanel-input-title").value;
    var contentInput = tinyMCE.get('sidepanel-input-content').getContent();
    if (contentInput === "") {
        contentInput = "none";
    }
    session = encodeURIComponent(session.trim());
    titleInput = encodeURIComponent(titleInput.trim());
    contentInput = encodeURIComponent(contentInput.trim());
    
    var newImage = "none";
    
    var imagePreview = document.getElementById("sidepanel-edit-image-preview");
    if (imagePreview.getAttribute("newimage") == "true") {
        //portrait = "&portrait=" + encodeURIComponent(imagebox.style.backgroundImage.replace('url("',"").replace('")', ""));
        newImage = encodeURIComponent(imagePreview.style.backgroundImage.replace('url("',"").replace('")', ""));
    }
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{SUCCESS}") != -1) {
            hideMessage('loading');
            showMessage('success', "Endring lagret");
            imagePreview.setAttribute("newimage", "false");
            imagePreview.setAttribute("style", "");
            loadSidebar();
            setTimeout(function(){
                hideMessage('success');
                closeOverlay();
            }, 1500);
        } else if (xhttp.readyState == 4) {
            hideMessage('loading');
            showMessage('warning', "Endring ble ikke lagret");
            imagePreview.setAttribute("newimage", "false");
            imagePreview.setAttribute("style", "");
            setTimeout(function(){
                hideMessage('warning');
                document.getElementById("sidepanel-settings").style.display = "block";
            }, 1500);
        }
    };
    if (session !== "") {
        xhttp.open("POST", "/scripts/editsidepanel.cgi",true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("session=" + session + "&section=" + selectedSection + "&title=" + titleInput + "&content=" + contentInput + "&image=" + newImage);
    }
}
function deletePost() {
    //Deletes a post from the server

    document.getElementById("confirm-delete-panel").style.display = "";
    showMessage('loading', 'Laster');
    
    var session = getCookie('session');
    var postid = document.getElementById("confirm-delete-panel").getAttribute("postid");
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{SUCCESS}") != -1) {
            hideMessage('loading');
            showMessage('success', "Innlegg slettet");
            if (document.getElementById("inspect-post").getAttribute("open") == "true") {
                selectSection('all');
            } else {
                loadPosts();	
            }
            setTimeout(function(){
                hideMessage('success');
                closeOverlay();
            }, 1500);
        } else if (xhttp.readyState == 4) {
            hideMessage('loading');
            showMessage('warning', "Fikk ikke slettet innlegg");
            setTimeout(function(){
                hideMessage('warning');
                closeOverlay();
            }, 1500);
        }
    };
    xhttp.open("GET", "/scripts/deletepost.cgi?session=" + session + "&postid=" + postid,true);
    xhttp.send();	
}
function changepassword() {
    //Changes the password of the current user, given that correct current password information is provided.

    var responseLabel = document.getElementById("change-password-response");
    responseLabel.innerHTML = "";
    if (document.getElementById("input-new-password").value == document.getElementById("input-confirm-new-password").value) {				
        var old_pass = document.getElementById("input-old-password").value;
        old_pass = encodeURIComponent(old_pass.trim());
        var new_pass = document.getElementById("input-new-password").value;
        new_pass = encodeURIComponent(new_pass.trim());
        
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                if (xhttp.responseText.indexOf("{SUCCESS}") > -1) {
                    responseLabel.innerHTML = "Suksess! Passord endret.";
                    document.getElementById("input-old-password").value = "";
                    document.getElementById("input-new-password").value = "";
                    document.getElementById("input-confirm-new-password").value = "";
                } else {
                    responseLabel.innerHTML = "Feil ved endring av passord.";
                }
            } else if (xhttp.readyState == 4) {
                responseLabel.innerHTML = "Feil ved endring av passord.";
            }
        };
        xhttp.open("GET", "/scripts/changepass.cgi?session=" + getCookie('session') + "&old_pass=" + old_pass + "&new_pass=" + new_pass, true);
        xhttp.send();
    } else {
        responseLabel.innerHTML = "Feltene er ikke like.";
    }
}
function setEmail() {
    //Sets a new email address for the current user.

    var responseLabel = document.getElementById("change-email-response");
    responseLabel.innerHTML = "";
    
    var field = document.getElementById("change-user-email");
    var newEmail = encodeURIComponent(field.value);
    
    var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            if (xhttp.responseText.indexOf("{SUCCESS}") > -1) {
                responseLabel.innerHTML = "Suksess! E-postadresse endret.";
            } else {
                responseLabel.innerHTML = "Feil ved endring av e-postadresse.";
            }
        } else if (xhttp.readyState == 4) {
            responseLabel.innerHTML = "Feil ved endring av e-postadresse.";
        }
    };
    xhttp.open("GET", "/scripts/changeemail.cgi?session=" + getCookie('session') + "&newemail=" + newEmail, true);
    xhttp.send();
}
function navtologin() {
    //Navigates the user to the login page, keeping track of where they left off.

    window.location = "https://kattenelever.no/login?returnto=" + encodeURIComponent(location.search);
}
function checkLogin() {
    //Checkes if the user is logged into a valid account.

    var session = getCookie('session');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText.indexOf("{LOGGEDIN}") != -1) {
            document.getElementById("login").style.display = "none";
            document.getElementById("loggedinas").style.display = "block";

            var parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhttp.responseText, "text/html");

            var loggedinas = xmlDoc.querySelector("username").textContent.trim();
            var access = xmlDoc.querySelector("access").textContent.trim();

            document.getElementById("loggedinastext").textContent = loggedinas;
            document.getElementById("loggedinastext").setAttribute("access", access);
            document.getElementById("settings-button-wrap").style.display = "block";
            
            if ((access.split(",").indexOf(selectedSection) > -1 || access == "All") && selectedSection != "all") {
                document.getElementById("new-post-section").style.display = "block";
                document.getElementById("sidepanel-edit-button").style.display = "block";
            }
        }
    };
    if (session !== "") {
        xhttp.open("GET", "/scripts/checklogin.cgi?session=" + session,true);
        xhttp.send();	
    }
}
function logout() {
    //Logs the user out of the account they're signed into.

    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "../scripts/logout.cgi?session=" + getCookie('session'), true);
    xhttp.send();

    document.cookie = "session=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/";
    location.reload();
}
function loadPosts() {
    //Loads posts for the selected section.

    var session = getCookie('session');
    if (session === "") {session = "none";}
    
    var section = selectedSection; //determines which posts to get, ex: "hugin" or "skoleavisen"
    section = encodeURIComponent(section.trim());
    
    var page = getParameterByName('page');
    if (page === null) {
        page = "1";
    }
    page = encodeURIComponent(page.trim());
    
    var postSection = document.getElementById("post-section");
    postSection.innerHTML = '<i class="fa fa-refresh fa-spin"></i> Laster innlegg..';
    postSection.style.textAlign = "center";
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            postSection.style.textAlign = "";
            displayPosts(xhttp.responseText, "post-section", false);
        } else if (xhttp.readyState == 4) {
            postSection.innerHTML = '<i class="fa fa-frown-o"></i> Kunne ikke laste inn innlegg..';
        }
    };
    xhttp.open("GET", "/scripts/loadposts.cgi?session=" + session + "&section=" + section + "&page=" + page,true);
    xhttp.send();	
}
function displayPosts(postData, sectionID, inspectingPost) {
    //Takes post data and creates the relevant html for each post.

    var postSection = document.getElementById(sectionID);
    postSection.innerHTML = "";
    
    var parser = new DOMParser();
    xmlDoc = parser.parseFromString(postData, "text/html");
    
    var posts = xmlDoc.querySelectorAll('post');
    if (posts.length === 0) {
        postSection.style.textAlign = "center";
        postSection.innerHTML = '<i class="fa fa-meh-o"></i> Ingen innlegg å vise..';
    } else {
        for (i = 0; i < posts.length; i++) { //for each post
            var postContainer = document.createElement("div");
            postContainer.className = "post";
            postContainer.setAttribute("postid", posts[i].querySelector("id").textContent);
                var postHead = document.createElement("div");
                postHead.className = "post-head";
                    var postAuthor = document.createElement("div");
                    postAuthor.className = "post-author";
                    postAuthor.appendChild(document.createTextNode("Av: " + posts[i].querySelector("author").textContent));
                    if ((selectedSection == "all" || inspectingPost === true) && posts[i].querySelector("type").textContent != "event") {
                        postAuthor.innerHTML += "<br>";
                        postAuthor.appendChild(document.createTextNode("Gruppe: " + posts[i].querySelector("group").textContent));
                    }
                    var postTitle = document.createElement("div");
                    postTitle.className = "post-title";
                    postTitle.appendChild(document.createTextNode(posts[i].querySelector("title").textContent));
                    postTitle.setAttribute("onclick", "selectPost('" + posts[i].querySelector("id").textContent + "')");
                    var postTime = document.createElement("div");
                    postTime.className = "post-time";
                    var timeContent = "Postet: " + moment(posts[i].querySelector("creationtime").textContent, "YYYY-MM-DD HH:mm:ss").format('DD.MM.YYYY HH:mm');
                    postTime.appendChild(document.createTextNode(timeContent));
                    if (posts[i].querySelector("edittime").textContent != "None") {
                        var editTime = document.createElement("div");
                        editTime.className = "edit-time";
                        editTime.textContent = " (Sist endret: " + moment(posts[i].querySelector("edittime").textContent, "YYYY-MM-DD HH:mm:ss").format('DD.MM.YYYY HH:mm') + ")";
                        postTime.appendChild(editTime);
                    }
                postHead.appendChild(postAuthor);
                postHead.appendChild(postTitle);
                postHead.appendChild(postTime);
                    if (inspectingPost) {
                        if (posts[i].querySelector("type").textContent == "event") {
                            var eventInformation = document.createElement("div");
                            eventInformation.className = "event-information";
                            
                            var eventHost = document.createElement("div");
                            eventHost.className = "event-host-container";
                            eventHost.textContent = "Arrangør: ";
                            var eventHostHost = document.createElement("span");
                            eventHostHost.className = "event-host";
                            eventHostHost.textContent = posts[i].querySelector("group").textContent;
                            eventHost.appendChild(eventHostHost);
                            eventInformation.appendChild(eventHost);
                            
                            var eventStartpoint = moment(posts[i].querySelector("startpoint").textContent, "YYYY-MM-DD HH:mm:ss");
                            var eventEndpoint = moment(posts[i].querySelector("endpoint").textContent, "YYYY-MM-DD HH:mm:ss");
                            eventInformation.innerHTML += '<i class="fa fa-clock-o event-info-icon"></i> <span class="event-time">' + capitalize(eventStartpoint.format('LLLL')) + "</span> ";
                            var endpointString = "";
                            if (eventStartpoint.format("YYYY-MM-DD") == eventEndpoint.format("YYYY-MM-DD")) {
                                endpointString = "kl. " + eventEndpoint.format("HH:mm");
                            } else {
                                endpointString = capitalize(eventEndpoint.format('LLLL'));
                            }
                            eventInformation.innerHTML += 'til <span class="event-time">' + endpointString + "</span>";
                            
                            var eventLocationContainer = document.createElement("div");
                            eventLocationContainer.className = "event-location-container";
                            eventLocationContainer.innerHTML = '<i class="fa fa-map-marker event-info-icon"></i> ';
                            var eventLocation = document.createElement("span");
                            eventLocation.className = "event-location";
                            eventLocation.textContent = posts[i].querySelector("location").textContent;
                            if (eventLocation == "none") eventLocation = "Ikke angitt";
                            eventLocationContainer.appendChild(eventLocation);
                            eventInformation.appendChild(eventLocationContainer);
                            
                            postHead.appendChild(eventInformation);
                        }
                    }
            postContainer.appendChild(postHead);
                var divider = document.createElement("hr");
            postContainer.appendChild(divider);
                var postBody = document.createElement("div");
                postBody.className = "post-body";
                postBody.innerHTML = posts[i].querySelector("content").innerHTML;
                if (inspectingPost === false) {
                    postBody.className = "post-body limit-post-length";
                }
            postContainer.appendChild(postBody);
                var showMore = document.createElement("div");
                showMore.className = "show-more-container";
                var showMoreBtn = document.createElement("a");
                showMoreBtn.className = "show-more";
                showMoreBtn.setAttribute("onclick", "selectPost('" + posts[i].querySelector("id").textContent + "')");
                showMoreBtn.textContent = "Vis mer";
                showMore.appendChild(showMoreBtn);
            postContainer.appendChild(showMore);
                var divider2 = document.createElement("hr");
            postContainer.appendChild(divider2);
                var postNavigation = document.createElement("div");
                postNavigation.className = "post-navigation";
                    var commentLink = document.createElement("a");
                    commentLink.className = "linkbutton";
                    commentLink.innerHTML = "Kommenter";
                    if (inspectingPost === false) {
                        commentLink.setAttribute("onclick", "selectPost('" + posts[i].querySelector("id").textContent + "')");
                    } else {
                        commentLink.href = "#comments";
                    }
                postNavigation.appendChild(commentLink);
                    if (posts[i].querySelector("canedit").textContent == "true") {
                        var postEdit = document.createElement("div");
                        postEdit.className = "post-edit";
                            var editLink = document.createElement("a");
                            editLink.className = "linkbutton";
                            editLink.innerHTML = "Rediger";
                            editLink.setAttribute("onclick", "showEditPanel('" + posts[i].querySelector("id").textContent + "')");
                            var deleteLink = document.createElement("a");
                            deleteLink.className = "linkbutton";
                            deleteLink.innerHTML = "Slett";
                            deleteLink.setAttribute("onclick", "showDeleteConfirmation('" + posts[i].querySelector("id").textContent + "')");
                        postEdit.appendChild(editLink);
                        postEdit.appendChild(deleteLink);
                        postNavigation.appendChild(postEdit);
                    }
            postContainer.appendChild(postNavigation);
            postSection.appendChild(postContainer);
        }
        if (inspectingPost === false) {
            //show "show more" button for overflowed posts
            var allPosts = document.getElementsByClassName("post");
            for (i = 0; i < allPosts.length; i++) {
                var selPost = allPosts[i];
                var selPostBody = selPost.getElementsByClassName("post-body")[0];
                if (selPostBody.scrollHeight > selPostBody.clientHeight) {
                    //display "show more" button as the post is truncated
                    selPost.getElementsByClassName("show-more-container")[0].style.display = "block";
                }
            }				
            
            //add next/previous buttons:
            var postSectionNavigation = document.createElement('div');
            postSectionNavigation.id = "postSectionNavigation";
            
            var nextButton = document.createElement('button');
            var previousButton = document.createElement('button');
            
            nextButton.className = "postNavigationBtn";
            previousButton.className = "postNavigationBtn";
            
            nextButton.id = "nextPageBtn";
            previousButton.id = "previousPageBtn";
            
            nextButton.innerHTML = 'Tidligere innlegg <i class="fa fa-arrow-right"></i>';
            previousButton.innerHTML = '<i class="fa fa-arrow-left"></i> Senere innlegg';
            
            nextButton.setAttribute("onclick", "nextPage()");
            previousButton.setAttribute("onclick", "previousPage()");
            
            var currentPage = getParameterByName('page');
            if (currentPage === null) {currentPage = 1;}
            currentPage = parseInt(currentPage);
            if (currentPage > 1) {postSectionNavigation.appendChild(previousButton);} //only append if not first page
            
            if (parseInt(xmlDoc.querySelector('postcount').textContent) > (15 * currentPage)) {postSectionNavigation.appendChild(nextButton);} //only append if more posts after this page
            
            postSection.appendChild(postSectionNavigation);
        }
    }
}
function nextPage() {
    //Navigates to the next list of posts.

    var currentPage = getParameterByName('page');
    if (currentPage === null) {currentPage = 1;}
    currentPage = parseInt(currentPage);
    currentPage += 1;
    if (history.pushState) {
        var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?section=" + selectedSection + "&page=" + currentPage;
        window.history.pushState({path:newurl},'',newurl);
        loadPosts();
    }
}
function previousPage() {
    //Navigate to the previous list of posts.

    var currentPage = getParameterByName('page');
    if (currentPage === null) {currentPage = 1;}
    currentPage = parseInt(currentPage);
    if (currentPage > 1) {
        currentPage -= 1;
        if (history.pushState) {
            var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + "?section=" + selectedSection + "&page=" + currentPage;
            window.history.pushState({path:newurl},'',newurl);
            loadPosts();
        }
    }
}
function showDeleteConfirmation(postid) {
    //Shows a delete confirmation dialog, asking the user to confirm delete action.

    document.getElementById("confirm-delete-panel").setAttribute("postid", postid);
    showOverlay();
    showPanel('confirm-delete-panel');
}
function showDeleteUserConfirmation(button) {
    //Shows a delete selected user confirmation, asking the user to confirm delete action.

    button.innerHTML = '<i class="fa fa-trash-o fa-lg" aria-hidden="true"></i> Sikker?';
    var userid = button.getAttribute("userid");
    button.setAttribute("onclick", "deleteuser(" + userid + ")");
}
function deleteuser(userid) {
    //Deletes selected user.

    userid = encodeURIComponent(userid);
    var session = encodeURIComponent(getCookie('session'));
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            loadusertable();
        } else if (xhttp.readyState == 4) {
            document.getElementById("usertable-response").innerHTML = "Fikk ikke slettet bruker.";
        }
    };
    xhttp.open("GET", "/scripts/deleteuser.cgi?session=" + session + "&userid=" + userid,true);
    xhttp.send();	
}
function toggleUserType() {
    //Toggles the user type when creating a new user.

    var selector = document.getElementById("new-user-role");
    var checkboxes = document.getElementById("new-user-access-container").getElementsByTagName("input");
    
    var selectedUserType = selector.options[selector.selectedIndex].value;
    
    if (selectedUserType == "User") {
        for (i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
            checkboxes[i].disabled = false;
        }
    } else {
        for (i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = true;
            checkboxes[i].disabled = true;
        }
    }
}
function createuser() {
    //Takes new user form information and creates a new user.

    document.getElementById("new-user-panel").style.display = "";
    showMessage('loading', "Laster");
    
    var responseField = document.getElementById("new-user-response");
    responseField.innerHTML = "";
    var selector = document.getElementById("new-user-role");
    
    var session = encodeURIComponent(getCookie('session'));
    var username = "&username=" + encodeURIComponent(document.getElementById("new-user-username").value);
    var password = "&password=" + encodeURIComponent(document.getElementById("new-user-password").value);
    var email = "&email=" + encodeURIComponent(document.getElementById("new-user-email").value);
    var usertype = "&usertype=" + encodeURIComponent(selector.options[selector.selectedIndex].value);
    var access = "";
    var checkboxes = document.getElementById("new-user-access-container").getElementsByTagName("input");
    for (i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            if (access !== "") access += ",";
            access += checkboxes[i].value;	
        }
    }
    access = "&access=" + encodeURIComponent(access);
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            hideMessage('loading');
            closeOverlay();
            showOverlay();
            showPanel('settings-panel');
        } else if (xhttp.readyState == 4) {
            hideMessage('loading');
            document.getElementById("new-user-panel").style.display = "block";
            responseField.innerHTML = "Det skjedde noe feil..";
        }
    };
    xhttp.open("POST", "/scripts/createuser.cgi",true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("session=" + session + username + password + email + usertype + access, true);
}
var editimagefile = document.getElementById("sidepanel-edit-image-file");
if(editimagefile.addEventListener) editimagefile.addEventListener('change', handleeditimagefile, false);
function handleeditimagefile(e) {
    //Handles image data parsing for editing sidepanel image for the relevant section.
    if (window.FileReader) {
        var imagebox = document.getElementById("sidepanel-edit-image-preview");
        var file = e.target.files[0];
        var fr = new FileReader();
        fr.onload = function () {
            document.getElementById("sidepanel-edit-image-preview").style.display = "";
            imagebox.style.backgroundImage = "url(" + fr.result + ")";
            imagebox.setAttribute("newimage", "true");
        };
        fr.readAsDataURL(file);
    }
}
function loadCalendar(year, week) {
    //Loads and displays the calendar for the selected section.

    document.getElementById("calendar-week").textContent = week;
    document.getElementById("calendar-year").textContent = year;
    
    var table = document.getElementById("calendar-table");
    table.innerHTML = '<i class="fa fa-refresh fa-spin"></i> Laster kalender';
    
    var weekdays = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"];
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            table.innerHTML = "";
            
            var parser = new DOMParser();
            xmlDoc = parser.parseFromString(xhttp.responseText, "text/html");
            var events = xmlDoc.querySelectorAll("event");
            
            for (d = 0; d < 7; d++) {
                var newRow = document.createElement("tr");
                var weekDay = document.createElement("td");
                weekDay.textContent = weekdays[d];
                newRow.appendChild(weekDay);
                var weekDate = document.createElement("td");
                weekDate.textContent = moment(String(year) + "-" + String(week) + "-" + String(d + 1), "YYYY-W-E").format("DD.MM");
                newRow.appendChild(weekDate);
                var eventContainer = document.createElement("td");
                eventContainer.className = "event-block";
                eventContainer.setAttribute("empty", "yes");
                eventContainer.textContent = "Ingen arrangementer å vise";
                newRow.appendChild(eventContainer);						
                table.appendChild(newRow);
            }
            var eventContainers = table.getElementsByClassName("event-block"); //[0] = monday, [7] = sunday
            for (e = 0; e < events.length; e++) {
                var eventDay = parseInt(moment(events[e].querySelector("startpoint").textContent, "YYYY-MM-DD HH:mm:ss").format("E")) - 1; //format mon-sun = 0-6
                if (eventContainers[eventDay].getAttribute("empty") == "yes") {
                    eventContainers[eventDay].setAttribute("empty", "no");
                    eventContainers[eventDay].innerHTML = "";
                }
                var eventBlock = document.createElement("a");
                eventBlock.className = "calendar-event";
                eventBlock.setAttribute("onclick", "selectPost(" + events[e].querySelector("eventid").textContent + ")");
                
                var eventTitleContainer = document.createElement("div");
                eventTitleContainer.className = "calendar-event-title";
                eventTitleContainer.textContent = events[e].querySelector("title").textContent;
                var eventTimeContainer = document.createElement("div");
                eventTimeContainer.className = "calendar-event-time";
                eventTimeContainer.textContent = moment(events[e].querySelector("startpoint").textContent, "YYYY-MM-DD HH:mm:ss").format("HH:mm") + "-" + moment(events[e].querySelector("endpoint").textContent, "YYYY-MM-DD HH:mm:ss").format("HH:mm");
                var eventDescriptionContainer = document.createElement("div");
                eventDescriptionContainer.className = "calendar-event-description";
                eventDescriptionContainer.textContent = events[e].querySelector("description").textContent;
                
                eventBlock.appendChild(eventTitleContainer);
                eventBlock.appendChild(eventTimeContainer);
                eventBlock.appendChild(eventDescriptionContainer);
                
                eventContainers[eventDay].appendChild(eventBlock);
            }
        } else if (xhttp.readyState == 4) {
            table.innerHTML = '<i class="fa fa-frown-o"></i> Kunne ikke laste kalender';
        }
    };
    xhttp.open("GET", "/scripts/loadcalendar.cgi?week=" + week + "&year=" + year + "&section=" + document.getElementsByClassName("selected")[0].getAttribute("groupname"), true);
    xhttp.send();
}
function changeCalendarWeek(step) {
    //Called when clicking forward/backward nav button on calendar. Will change the selected week.

    var curWeek = parseInt(document.getElementById("calendar-week").textContent);
    var curYear = parseInt(document.getElementById("calendar-year").textContent);
    
    curWeek += parseInt(step);
    
    if (curWeek < 1) {
        curWeek += 52;
        curYear -= 1;
    } else if (curWeek > 52) {
        curWeek -= 52;
        curYear += 1;
    }
    
    loadCalendar(curYear, curWeek);
}
document.onkeydown = function(evt) {
    //Closes panel overlay when the user clicks the escape key
    evt = evt || window.event;
    if (evt.keyCode == 27) {
        closeOverlay();
    }
};
function getCookie(cname) {
    //Gets the cookie value of the selected cookie.
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
}
function capitalize(string) {
    //Capitalizes a word
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function getParameterByName(name, url) {
    //Gets url parameter value for given parameter name and url.
    if (!url) {
      url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
(function(DOMParser) {
//XML parser
"use strict";

    var
        proto = DOMParser.prototype
    , nativeParse = proto.parseFromString
    ;
    // Firefox/Opera/IE throw errors on unsupported types
    try {
    // WebKit returns null on unsupported types
        if ((new DOMParser()).parseFromString("", "text/html")) {
            // text/html parsing is natively supported
            return;
        }
    } catch (ex) {}
        proto.parseFromString = function(markup, type) {
        if (/^\s*text\/html\s*(?:;|$)/i.test(type)) {
            var
              doc = document.implementation.createHTMLDocument("")
            ;
                if (markup.toLowerCase().indexOf('<!doctype') > -1) {
                    doc.documentElement.innerHTML = markup;
                    }
                    else {
                        doc.body.innerHTML = markup;
                    }
                return doc;
            } else {
                return nativeParse.apply(this, arguments);
            }
        };
}(DOMParser));
window.onpopstate = function() {
    //On navigation, retrieve new relevant page content.
    checkQuery();
};