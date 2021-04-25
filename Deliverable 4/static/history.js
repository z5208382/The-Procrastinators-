const url = "http://localhost:5000/Eventdetails";
fetch(url, {
  method: 'POST'
})
  .then(r => r.json())
  .then(r => {
    for(i = 0; i < 15; i++){
      if(!(r[i].image_url.includes("default"))) {
        var index = document.getElementById("eventFeed"); 
        const eventImage = document.createElement("img");
        eventImage.src = r[i].image_url;
        eventImage.setAttribute("class", "feedImage");
        eventImage.setAttribute("id", "feedImage");
        index.appendChild(eventImage).addEventListener('click', function(){location.href='Eventdetails';});
      }
    }
});

document.getElementById("Home Button").addEventListener("click", function(){location.href="/";});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("History Button").addEventListener("click", function(){location.href="History"});