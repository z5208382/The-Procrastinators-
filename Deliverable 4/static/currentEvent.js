let url = "https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=";
fetch(url)
    .then(data => data.json())
    .then(result => {
        var localUrl = window.location.href;
        var url = new URL(localUrl);
        var id = url.searchParams.get("id");
        for (let event of result) {
            // Using dummy data
            if (event.id === id) {
                const imgHeader = event.image_url;
                const eventName = event.title;
                const eventLoc = event.location;
                const time = event.time_start + ' - ' + event.time_finish;
                const description = event.description;

                document.getElementById('event-image').src = imgHeader;
                document.getElementById('event-name').innerText = eventName;
                document.getElementById('event-location').innerText = eventLoc;
                document.getElementById('event-time').innerText = 'Time: \n' + time;
                document.getElementById('event-description').innerText = 'Description: \n' + description;
            }
        }
    })

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
        "SELECT * from Events ORDER BY startDate",
        [],
        (error, results) => {
            if (error) {
                throw error;
            }
            res.status(200).json(results.rows);
        }
    );
});

document.getElementById('calendar-btn').addEventListener('click', () => {
    alert("Calendar URL Copied to Clipboard!");
})

document.getElementById("Home Button").addEventListener("click", function(){location.href="index.html";});
document.getElementById("Societies").addEventListener("click", function(){location.href="societies.html"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="profile.html"});