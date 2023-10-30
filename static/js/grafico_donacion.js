var colors = ['#AEA7DC', '#A2C7E5', '#FF99C9','#58FCEC'];
                
Highcharts.chart('donacion-chart', {
    chart: {
    type: 'column'
    },
    title: {
    text: 'Total de Donaciones por Tipo'
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
    name: 'Donaciones',
    data: [],
    colorByPoint: true, 
    colors: colors 
    }]
});

fetch("http://localhost:5000/get-donacion-data")
    .then((response) => response.json())
    .then((data) => {
    let donaciones = data;

    console.log(donaciones);

    var don_cont = {};
            
    donaciones.forEach(function (categoria) {
        don_cont[categoria] = (don_cont[categoria] || 0) + 1;
    });
    
    var donData = Object.keys(don_cont).map(function (categoria) {
        return {
        name: categoria,
        y: don_cont[categoria]
        };
    });
    // Get the chart by ID
    const chart = Highcharts.charts.find(
    (chart) => chart && chart.renderTo.id === "donacion-chart"
    );

    // Update the chart with new data
    chart.update({
        xAxis: {
            categories: Object.keys(don_cont)
            },
        series: [
            {
            data: donData,
            },
        ],
    });
    })
    .catch((error) => console.error("Error:", error));