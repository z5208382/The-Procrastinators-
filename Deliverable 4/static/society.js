const societyName = document.getElementById("societyName"); 
const localUrl = window.location.href;
let url = new URL(localUrl);
const id = url.searchParams.get("id");

const getSociety = (data) => {
  const society = data[0];
  const societyBanner = document.getElementById("societyBanner");
  const societyImage = document.createElement("img");
  societyImage.src = society.image_url; 
  societyImage.setAttribute("class", "societyImage");
  societyBanner.appendChild(societyImage);
  societyName.innerText = society.name; 
  var about = document.getElementById("aboutSociety"); 
  about.innerText = society.description; 
}

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

document.getElementById("Home Button").addEventListener("click", function(){location.href="/"});
document.getElementById("Societies").addEventListener("click", function(){location.href="Societies"});
document.getElementById("ProfileButton").addEventListener("click", function(){location.href="Profile"});