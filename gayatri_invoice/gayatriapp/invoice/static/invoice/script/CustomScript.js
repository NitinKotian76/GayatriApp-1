let count = 0;
function getCSRFToken() {
  //this function gets the csrftoken
  let name = "csrftoken=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function filter(inputid, filterDiv) {
  var input, filter, ul, li, a, i;
  input = document.getElementById("inputid");
  filter = input.value.toUpperCase();
  div = document.getElementById(filterDiv);
  a = div.getElementsByTagName("td");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

setTimeout(() => {
  document.getElementById("notif")?.remove();
}, 5000);

function visible(id) {
  var x = document.getElementById(id);
  if (x.style.display == "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
}
// htmx.logAll();
