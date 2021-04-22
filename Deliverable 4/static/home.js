var url = "https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=";
fetch(url)
    .then(r => r.json())
    .then(r => {
        for(i = 0; i < r.length; i++){
            if(!(r[i].image_url.includes("default")))
            {
                var index = document.getElementById("eventFeed");
                const eventImage = document.createElement("img");
                eventImage.src = r[i].image_url;
                eventImage.setAttribute("class", "feedImage");
                id = r[i].id;
                eventImage.setAttribute("id", id);
                index.appendChild(eventImage).addEventListener('click', function(){location.href = "Eventdetails?id="+this.id;});
            }
        }
    });

<<<<<<< HEAD
// const body = {
//   id : 1,
//   url: 2,
//   title: 3,
//   time_start: 4,
//   time_finish: 5,
//   description: 6,
//   location: 7,
//   hosts: [],
//   image_url: 8,
//   categories: []
// }
// fetch('http://localhost:5000/home', {
//   method: 'POST',
//   headers: {
//     'Content-Type' : 'application/json'
//   },
//   body: JSON.stringify(body),
// }).then((response) => {
//     response.json().then(result => {
//       console.log(result.JSON);
//     })
// });

=======
>>>>>>> html_fix1
document.getElementById("Home Button").addEventListener("click", function(){location.href="/";});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="Profile"});

// document.getElementById("test-button").addEventListener("click", () => {
//   console.log('button pressed');
//   const body = {
//     test : 1
//   }
//   fetch('http://localhost:5000/test', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify(body),
//   }).then((response) => {
//       response.json().then(result => {
//         console.log(`response: ${JSON.stringify(result)}`);
//       })
//   })
// });
// Get the modal
var modal = document.getElementById("modal");

// Get the button that opens the modal
var btn = document.getElementById("Filter Button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

document.getElementById("Networking Button").addEventListener("click", function(){
    location.href="/"
});
document.getElementById("Seminar Button").addEventListener("click", function(){
  location.href="/"
});
document.getElementById("Social Button").addEventListener("click", function(){
  location.href="/"
});
document.getElementById("Workshop Button").addEventListener("click", function(){
  location.href="/"
});

