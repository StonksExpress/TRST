chrome.runtime.onMessage.addListener((request, sender, _) => {
    if (request.type == "newData") {
        chrome.pageAction.setIcon(({
            "path": "rsc/img/" + request.data.color + ".png",
            tabId: sender.tab.id
        }))
    }
});