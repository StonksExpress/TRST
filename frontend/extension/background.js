chrome.runtime.onMessage.addListener((request, sender, _) => {
    if (request.type == "newData") {
        chrome.pageAction.setIcon({
            "path": "rsc/img/" + request.data.color + ".png",
            tabId: sender.tab.id
        })
    } else if (request.type == "reset") {
        chrome.pageAction.setIcon({
            path: "rsc/img/logo.png",
            tabId: sender.tab.id
        })
    }
});