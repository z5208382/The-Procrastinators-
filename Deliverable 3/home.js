
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
                eventImage.setAttribute("class", "eventImage");
                eventImage.setAttribute("id", "eventImage");
                index.appendChild(eventImage).addEventListener('click', function(){alert("Hello World!");});
            }
        }
    });
document.getElementById("Home Button").addEventListener("click", function(){alert("Hello World!");});
document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});