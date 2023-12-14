
var endpoint = '/api/c/g/product/summury/chart/all/time/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Produtu',
                data: data.obj,
                backgroundColor: [
                    '#007bff','#242555','#5fa638','#fb8072','#80b1d3','#fdb462'
                ],
                borderWidth: 1
            }]
        };
        
        const config_product_summ_all = {
            type: 'pie',
            data: dt,
            // options: myoption
        };
        const product_summ_allChart_data = new Chart(
            document.getElementById('product_summ_allChart_data'),
            config_product_summ_all
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
