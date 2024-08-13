$(document).ready( function() {
	function getCSRFToken() {
	       //this function gets the csrftoken 
		let name = "csrftoken=";
		let decodedCookie = decodeURIComponent(document.cookie);
		let ca = decodedCookie.split(';');
		for(let i = 0; i <ca.length; i++) {
			let c = ca[i];
			while (c.charAt(0) == ' ') {
				c = c.substring(1);
			}
			if (c.indexOf(name) == 0) {
				return c.substring(name.length, c.length);
			}
		}
		return "";
	}
	   //this event is triggered by htmx requests     
    console.log(getCSRFToken());
    document.body.addEventListener('htmx:configRequest', (event) => {
		event.detail.headers['X-CSRFToken'] = getCSRFToken();
	}); 
    document.body.addEventListener('htmx:configRequest', (event) => {
        console.log(event.detail.headers); // Check if the CSRF token is included
    });
    document.getElementById('modal').style.display='block';// this triggers the login Modal
});


