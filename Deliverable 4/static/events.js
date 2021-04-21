let url = "https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=";
fetch(url)
    .then(data => data.json())
    .then(result => {
        for (let event of result) {
            // Using dummy data
            if (event.id === '2979283185636941') {
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

document.getElementById('feedback-btn').addEventListener('click', () => {
    location.href = "feedback.html";
})

document.getElementById("Home Button").addEventListener("click", function(){location.href="/";});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="Profile"});
