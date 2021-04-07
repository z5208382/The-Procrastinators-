var url = "https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=";
fetch(url)
    .then(r => r.json())
    .then(r => {
        for(i = 25; i < 40; i++){
            if(!(r[i].image_url.includes("default")))
            {
                var index = document.getElementById("eventFeed"); 
                const eventImage = document.createElement("img");
                eventImage.src = r[i].image_url;
                eventImage.setAttribute("class", "feedImage");
                eventImage.setAttribute("id", "feedImage");
                index.appendChild(eventImage).addEventListener('click', function(){location.href='feedback.html';});
            }
        }
});

document.getElementById("Home Button").addEventListener("click", function(){location.href="index.html";});
document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});
document.getElementById("History Button").addEventListener("click", function(){location.href="history.html"});