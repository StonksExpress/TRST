var title = document.querySelector("#title");
var info = document.querySelector("#info");

var colours = {
    "green": "#20e040",
    "gray": "#cccccc",
    "red": "#e04040",
    "orange": "#ffb62e"
}

window.onload = function() {
    chrome.storage.local.get(['data'], function(result) {
        let data = result.data;
        title.innerHTML = data.title;
        title.style.color = colours[data.color];
        info.style.color = colours[data.color];
        info.innerHTML = ""
        for (let entry of data.info) {
            var node = document.createElement("li");
            node.appendChild(document.createTextNode(entry));                              
            info.appendChild(node);
        }
    });
}