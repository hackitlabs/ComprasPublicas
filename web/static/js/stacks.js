function create_tipo_procesos(container, tipo_procesos){
  Highcharts.chart(container, {
    chart: {
      type: 'bar'
    },
    title: {
      text: null
    },
    xAxis: {
      categories: ['Ministerio'],
      labels: {
        enabled: false
      }
    },
    credits:{
      enabled: false
    },
    yAxis: {
      min: 0,
      title: {
        text: null
      },
      labels:{
        enabled: false
      }
    },
    legend: {
      reversed: false
    },
    plotOptions: {
      series: {
        stacking: 'percent'
      }
    },
    series: tipo_procesos
  });
}