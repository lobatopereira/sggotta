setInterval(function(){
    $.get('/api/notification/badge/distribution/request/',function(data) {
        document.getElementById("notifbadge").innerHTML = data.value;
    });
}, 5000);
