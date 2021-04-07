const url = "https://dev-api.linkupevents.com.au/societies?uni=unsw"; 
fetch(url)
    .then(r => r.json())
    .then(r => {
        for(i = 0; i < 12; i++)
        {
            var index = document.getElementById("eventFeed"); 
            const societyImage = document.createElement("img");
            societyImage.src = r[i].image_url
            societyImage.setAttribute("class", "feedImage");
            societyImage.setAttribute("id", "feedImage");
            index.appendChild(societyImage)
        }
    });

    document.getElementById("Home Button").addEventListener("click", function(){location.href="index.html";});
    document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});