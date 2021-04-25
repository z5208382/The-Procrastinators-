const url = "http://localhost:5000/Eventdetails"
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

document.getElementById('feedback-btn').addEventListener('click', () => {
    location.href = "feedback.html";
})

document.getElementById("Home Button").addEventListener("click", function(){location.href="/";});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="Profile"});
