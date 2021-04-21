var url = "https://dev-api.linkupevents.com.au/societies?uni=unsw";
fetch(url)
    .then(r => r.json())
    .then(r => {
        for(i = 0; i < r.length; i++){
            var index = document.getElementById("eventFeed"); 
            const societyImage = document.createElement("img");
            societyImage.src = r[i].image_url;
            societyImage.setAttribute("class", "feedImage");
            societyImage.setAttribute("id", r[i].id);
            index.appendChild(societyImage).addEventListener('click', function(){location.href="Society?id="+this.id;});
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
        "SELECT * from Societies",
        [],
        (error, results) => {
            if (error) {
                throw error;
            }
            res.status(200).json(results.rows);
        }
    );
});

document.getElementById("Home Button").addEventListener("click", function(){location.href="/"});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="Profile"});
