function handlePageAPIInfo(data) {
    chrome.runtime.sendMessage( {"type": "newData", "data": data} );
    chrome.storage.local.set({"data": data});
}

(() => {
    // $.get(
    //     "localhost",
    //     {"url": document.location.href},
    //     (data) => handlePageAPIInfo(JSON.parse(data))
    // );

    if (document.location.host == "developer.chrome.com") {
        handlePageAPIInfo({
            color: "green",
            title: "Trusted",
            info: ["Guardian blah", "trust matrix 52.1%"]
        })
    }
})()