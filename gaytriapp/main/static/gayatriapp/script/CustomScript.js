$(document).ready(function() {
	let count = 0;
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
	/** the count is not updated immideately it updates after two requests */
	console.log(getCSRFToken());
	document.body.addEventListener('htmx:configRequest', (event) => {
		event.detail.headers['X-CSRFToken'] = getCSRFToken();
	}); 
});
