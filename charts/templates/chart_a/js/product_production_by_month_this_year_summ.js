
var endpoint = '/api/c/g/product/report/summury/by-month/this-year'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        var ajaxdata = []
        for (let i in data.labels) {
            var totData = []
            for (let j in data.obj) {
                totData.push(data.obj[j][i])
            }
            ajaxdata.push(totData)
        }
        var backgroundColor = ['#8ed8a7','#ff3','#bebada','#fb8072','#80b1d3','#10f1d3','#89d1a3','#fdb462']
        var plotdata = []
        for (let i in ajaxdata) {
            plotdata.push({
                label: data.labels[i],
                data: ajaxdata[i],
                backgroundColor: backgroundColor[i],
                borderColor: backgroundColor[i],
                borderWidth: 1
            },)
        }
        const dt = {
            labels: data.label,
            datasets: plotdata
        };
        
        const config_gclubfedassoc = {
            type: 'bar',
            data: dt,
            options: groupoption
        };
        const gProductProdusaunChart_data = new Chart(
            document.getElementById('gProductProdusaunChart_data'),
            config_gclubfedassoc
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
