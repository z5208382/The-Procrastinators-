var url = "https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=";
fetch(url)
    .then(r => r.json())
    .then(r => {
        var societies = [];
        for(i = 15; i < 80; i++){
            if(r[i].hosts[0]){
                var society = r[i].hosts[0].name;
                if(societies.indexOf(society) == -1) {
                    societies.push(society); 
                    var index = document.getElementById("eventFeed"); 
                    const societyImage = document.createElement("img");
                    societyImage.src = r[i].hosts[0].image;
                    societyImage.setAttribute("class", "feedImage");
                    societyImage.setAttribute("id", "feedImage");
                    index.appendChild(societyImage).addEventListener('click', function(){location.href="society.html"});
                }
            }
        }
    });

document.getElementById("Home Button").addEventListener("click", function(){location.href="index.html"});
document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="profile.html"});
