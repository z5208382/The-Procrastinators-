<<<<<<< HEAD

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
                eventImage.setAttribute("id", "feedImage");
                index.appendChild(eventImage).addEventListener('click', function(){alert("Hello World!");});
            }
        }
    });
document.getElementById("Home Button").addEventListener("click", function(){alert("index.html");});
document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});

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
    location.href="index.html"
});
=======
var index = document.getElementById("eventFeed"); 
const test = document.createElement("img");
test.src = "./test.jpg";
test.setAttribute("class", "eventImage");
index.appendChild(test);
>>>>>>> login
