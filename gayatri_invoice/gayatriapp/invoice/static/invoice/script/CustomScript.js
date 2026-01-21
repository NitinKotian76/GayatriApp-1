let count = 0;

// htmx.logAll();

/**
 * this function is for the searchfield in the table view
 * its meant to provde the user response on the client side
 * and send the request only if it cant find it in the current view
 *
 * @param {str} inputid - id of the searchbar element
 * @param {str} filterDiv - id of the table parent
 */
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

// document.body.addEventListener("htmx:afterSwap", function (evt) {
//   if (
//     evt.detail.target.id === "mainform" ||
//     evt.detail.target.id === "dynform"
//   ) {
//     htmx.trigger(document.body, "showNotif");
//   }
//   if (evt.detail.target.id === "notif") {
//     hideNotifAfterTimeout();
//   }
// });
//
// function hideNotifAfterTimeout() {
//   const notif = document.getElementById("notif");
//   if (notif) {
//     notif.style.display = "block";
//     setTimeout(() => {
//       notif.style.display = "none";
//     }, 5000);
//   }
// }

//
// function clearSelectedRows() {
//   const allInputs = document.querySelectorAll("#tableform input"); // Selects all input elements within the form
//   allInputs.forEach((input) => {
//     input.checked = false;
//     input.value = "";
//   });
//   console.log("cleared input ");
// }
