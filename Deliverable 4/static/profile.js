const url = "https://dev-api.linkupevents.com.au/societies?uni=unsw"; 
fetch(url)
    .then(r => r.json())
    .then(r => {
        for(i = 120; i < 135; i++)
        {
            var index = document.getElementById("eventFeed"); 
            const societyImage = document.createElement("img");
            societyImage.src = r[i].image_url
            societyImage.setAttribute("class", "feedImage");
            societyImage.setAttribute("id", r[i].id);
            index.appendChild(societyImage).addEventListener('click', function(){location.href="Society?id="+this.id;});
        }
    });

document.getElementById("Home Button").addEventListener("click", function(){location.href="/home";});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("History Button").addEventListener("click", function(){location.href="History"});
