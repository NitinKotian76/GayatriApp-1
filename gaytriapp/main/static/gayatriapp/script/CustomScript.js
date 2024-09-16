$(document).ready( function() {
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
	console.log(getCSRFToken());
    document.body.addEventListener('htmx:beforeRequest', (event)=>{
        //if(event.target.className == "fieldlist"){
            count++;
            console.log(event.target);
            let value= JSON.parse(event.target.getAttribute("hx-vals"));
            value["count"] = count;
            event.target.setAttribute("hx-vals",JSON.stringify(value));
        //}
    });
	document.body.addEventListener('htmx:configRequest', (event) => {
		event.detail.headers['X-CSRFToken'] = getCSRFToken();
	}); 


});


