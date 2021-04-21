const societyName = document.getElementById("societyName"); 
var localUrl = window.location.href;
var url = new URL(localUrl);
var id = url.searchParams.get("id");
fetch("https://dev-api.linkupevents.com.au/societies?uni=unsw")
    .then(r => r.json())
    .then(r => {
        for(i = 0; i < r.length; i++){
            if(r[i].id == id)
            {
                const societyBanner = document.getElementById("societyBanner");
                const societyImage = document.createElement("img");
                societyImage.src = r[i].image_url; 
                societyImage.setAttribute("class", "societyImage");
                societyBanner.appendChild(societyImage);
                societyName.innerText = r[i].name; 
                var about = document.getElementById("aboutSociety"); 
                about.innerText = r[i].description; 
            }
        }
    });

// connect to the PostgreSQL database    
const { Client } = require('pg');
const client = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'seng2021',
    password: '',
    port: 5432,
});    
client.connect();

// queries and grabs from data from api
app.get("https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=", (req, res) => {
    client.query(
        "SELECT name from Societies",
        [],
        (error, results) => {
            if (error) {
                throw error;
            }
            res.status(200).json(results.rows);
        }
    );
});

document.getElementById("Events Button").addEventListener("click", function(){
    var about = document.getElementById("aboutSociety");
    about.style.display = "none";
    fetch("https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=")
        .then(r => r.json())
        .then(r => {
            for(i = 0; i < r.length; i++){
                if(r[i].hosts[0]){
                    if(r[i].hosts[0].id == id){
                        var index = document.getElementById("societyEvents"); 
                        const societyImage = document.createElement("img");
                        societyImage.src = r[i].image_url;
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