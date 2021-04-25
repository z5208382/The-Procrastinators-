const url = "http://localhost:5000/Home";
fetch(url, {
  method: 'POST'
})
  .then(r => r.json())
  .then(r => {
    for(i = 0; i < r.length; i++) {
      if(!(r[i].image_url.includes("default"))) {
        var index = document.getElementById("eventFeed");
        const eventImage = document.createElement("img");
        eventImage.src = r[i].image_url;
        eventImage.setAttribute("class", "feedImage");
        id = r[i].id;
        eventImage.setAttribute("id", id);
        index.appendChild(eventImage).addEventListener('click', function(){location.href = "Eventdetails?id="+this.id;});
      }
    }
  })
  
const getSociety = (data) => {
  if (data !== null) {
    for(i = 0; i < r.length; i++) {
      if(!(r[i].image_url.includes("default"))) {
        var index = document.getElementById("eventFeed");
        const eventImage = document.createElement("img");
        eventImage.src = r[i].image_url;
        eventImage.setAttribute("class", "feedImage");
        id = r[i].id;
        eventImage.setAttribute("id", id);
        index.appendChild(eventImage).addEventListener('click', function(){location.href = "Eventdetails?id="+this.id;});
      }
    }
  }
}

document.getElementById("Home Button").addEventListener("click", function(){location.href="/";});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="Profile"});

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
  location.href="/Category?category=networking"
});
document.getElementById("Seminar Button").addEventListener("click", function(){
  location.href="/Category?category=seminar"
});
document.getElementById("Social Button").addEventListener("click", function(){
  location.href="/Category?category=social"
});
document.getElementById("Workshop Button").addEventListener("click", function(){
  location.href="/Category?category=workshop"
});

