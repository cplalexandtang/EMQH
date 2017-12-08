var normal = chrome.contextMenus.create({
    title: "View Answer",
    contexts:["image"],
    onclick: function(info) {
        handleImageURL(info.srcUrl);
    }
});
function handleImageURL(url) {
    // now do something with the URL string in the background page
	//alert((url));
	var test = url.lastIndexOf("/");
	var query = url.substring(test);
	getAnswer(query);
}
function getAnswer(query) {
	var request = new XMLHttpRequest();
    request.open("GET", "http://35.197.88.75:5000/emans" +query);
    request.send();

    request.onreadystatechange = function() {
        // 伺服器請求完成
        if (request.readyState === 4) {
            // 伺服器回應成功
            if (request.status === 200) {
                var type = request.getResponseHeader("Content-Type");   // 取得回應類型
                // 判斷回應類型，這裡使用 JSON
                if (type.indexOf("application/json") === 0) {               
                    var data = JSON.parse(request.responseText);
					alert(data.ans);
                }
            } else {
                alert("發生錯誤: " + request.status);
            }
        }
    }
}