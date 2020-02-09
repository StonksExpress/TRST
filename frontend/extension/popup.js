var title = document.querySelector("#title");
var info = document.querySelector("#info");
var body = document.querySelector("body");

var colours = {
    "green": "#50a050",
    "gray": "#909090",
    "red": "#e04040",
    "orange": "#ef761e"
}

window.onload = function() {
    chrome.storage.local.get(['data'], function(result) {
        let data = result.data;
        title.innerHTML = data.title;
        body.style.backgroundColor = colours[data.color];
        info.innerHTML = "";
        for (let entry of data.reasons) {
            var node = document.createElement("li");
            node.appendChild(document.createTextNode(entry));                              
            info.appendChild(node);
        }
    });
}