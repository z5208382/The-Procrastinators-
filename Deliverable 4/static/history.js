var url = "https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=";
fetch(url)
    .then(r => r.json())
    .then(r => {
        for(i = 0; i < 15; i++){
            if(!(r[i].image_url.includes("default")))
            {
                var index = document.getElementById("eventFeed"); 
                const eventImage = document.createElement("img");
                eventImage.src = r[i].image_url;
                eventImage.setAttribute("class", "feedImage");
                eventImage.setAttribute("id", "feedImage");
                index.appendChild(eventImage).addEventListener('click', function(){location.href='event_details.html';});
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
        "SELECT prevAttended from Profiles",
        [],
        (error, results) => {
            if (error) {
                throw error;
            }
            res.status(200).json(results.rows);
        }
    );
});

document.getElementById("Home Button").addEventListener("click", function(){location.href="index.html";});
document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});
document.getElementById("History Button").addEventListener("click", function(){location.href="history.html"});