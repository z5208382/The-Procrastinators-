const societyName = document.getElementById("societyName"); 
societyName.innerText = "UNSW Education Society";
const societyBanner = document.getElementById("societyBanner");
const societyImage = document.createElement("img");
societyImage.src = 'https://cdn.linkupevents.com.au/society/UNSWEDSOC.jpg'
societyImage.setAttribute("class", "societyImage");
societyBanner.appendChild(societyImage);

const url = "https://dev-api.linkupevents.com.au/societies?uni=unsw"; 
fetch(url)
    .then(r => r.json())
    .then(r => {
        for(i = 0; i < r.length; i++){
            if(r[i].name == "UNSW Education Society")
            {
                var about = document.getElementById("aboutSociety"); 
                about.innerText = r[i].description; 
            }
        }
    });

document.getElementById("Events Button").addEventListener("click", function(){
    var about = document.getElementById("aboutSociety");
    about.style.display = "none";
    fetch("https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=")
        .then(r => r.json())
        .then(r => {
            for(i = 0; i < r.length; i++){
                if(r[i].hosts[0]){
                    if(r[i].hosts[0].name == "UNSW Education Society"){
                        var index = document.getElementById("societyEvents"); 
                        const societyImage = document.createElement("img");
                        societyImage.src = r[i].hosts[0].image;
                        societyImage.setAttribute("class", "feedImage");
                        societyImage.setAttribute("id", "feedImage");
                        index.appendChild(societyImage);
                    }
                }
            }
        });
    });

document.getElementById("Home Button").addEventListener("click", function(){location.href="index.html"});
document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="profile.html"});