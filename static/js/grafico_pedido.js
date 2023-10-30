var colors = ['#AEA7DC', '#A2C7E5', '#FF99C9','#58FCEC'];
                
Highcharts.chart('pedidos-chart', {
    chart: {
    type: 'column'
    },
    title: {
    text: 'Total de Pedidos por Tipo'
    },
    xAxis: {
    categories: []
    },
    yAxis: {
    title: {
        text: 'Total'
    }
    },
    labels: {
    format: '{value:.0f}' 
    },
    series: [{
    name: 'Pedidos',
    data: [],
    colorByPoint: true, 
    colors: colors 
    }]
});

fetch("http://localhost:5000/get-pedido-data")
    .then((response) => response.json())
    .then((data) => {
    let pedidos = data;

    console.log(pedidos);

    var ped_cont = {};
            
    pedidos.forEach(function (categoria) {
        ped_cont[categoria] = (ped_cont[categoria] || 0) + 1;
    });
    
    var pedData = Object.keys(ped_cont).map(function (categoria) {
        return {
        name: categoria,
        y: ped_cont[categoria]
        };
    });
    // Get the chart by ID
    const chart = Highcharts.charts.find(
    (chart) => chart && chart.renderTo.id === "pedidos-chart"
    );

    // Update the chart with new data
    chart.update({
        xAxis: {
            categories: Object.keys(ped_cont)
            },
        series: [
            {
            data: pedData,
            },
        ],
    });
    })
    .catch((error) => console.error("Error:", error));