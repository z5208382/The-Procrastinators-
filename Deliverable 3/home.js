var i = 0; 
while(i < 20){
    var index = document.getElementById("eventFeed"); 
    const test = document.createElement("img");
    test.src = "./test.jpg";
    test.setAttribute("class", "eventImage");
    test.setAttribute("id", "eventImage");
    index.appendChild(test);
    i++; 
}

document.getElementById("Home Button").addEventListener("click", function(){alert("Hello World!");});

var elements = document.getElementsByClassName("eventImage");

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', function(){alert("Hello World!");});
}
