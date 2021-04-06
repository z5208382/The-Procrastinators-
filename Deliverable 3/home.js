var i = 0; 
while(i < 20){
    var index = document.getElementById("eventFeed"); 
    const test = document.createElement("img");
    test.src = "./test.jpg";
    test.setAttribute("class", "eventImage");
    index.appendChild(test);
    i++; 
}

document.getElementById("Home Button").addEventListener("click", function(){alert("Hello World!");});

