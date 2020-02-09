function handlePageAPIInfo(data) {
    chrome.runtime.sendMessage( {"type": "newData", "data": data} );
    chrome.storage.local.set({"data": data});
}

(() => {
    chrome.runtime.sendMessage( {"type": "reset"} );
    chrome.pageAction.show(chrome.tab.id);
    $.get(
        "http://ereshchenko.com:80/api/testSite",
        {"site": document.location.href},
        (data) => {
            if (data.trust < 0.3) {
                data.color = "red";
                data.title = "Very Low";
            } else if (data.trust < 0.5) {
                data.color = "orange";
                data.title = "Low";
            } else if (data.trust < 0.7) {
                data.color = "gray";
                data.title = "Insufficient";
            } else {
                data.color = "green";
                data.title = "Higher";
            }
            handlePageAPIInfo(data);

            title.innerHTML = data.title;
            title.style.color = colours[data.color];
            info.style.color = colours[data.color];
            info.innerHTML = "";
            for (let entry of data.reasons) {
                var node = document.createElement("li");
                node.appendChild(document.createTextNode(entry));                              
                info.appendChild(node);
            }
        }
    );
})();