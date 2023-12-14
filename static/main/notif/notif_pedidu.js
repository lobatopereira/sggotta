setInterval(function(){
    $.get('/api/notification/pedidu/distribution/foun/',function(data) {
        document.getElementById("notifpedidufoun").innerHTML = data.value;
    });
}, 5000);
