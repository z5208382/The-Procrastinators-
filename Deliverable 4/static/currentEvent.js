let url = "https://dev-api.linkupevents.com.au/events?uni=unsw&sort_by=time_start&query_string=";
fetch(url)
    .then(data => data.json())
    .then(result => {
        var localUrl = window.location.href;
        var url = new URL(localUrl);
        var id = url.searchParams.get("id");
        for (let event of result) {
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

document.getElementById('calendar-btn').addEventListener('click', () => {
    alert("Calendar URL Copied to Clipboard!");
})

document.getElementById("Home Button").addEventListener("click", function(){location.href="/";});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="Profile"});