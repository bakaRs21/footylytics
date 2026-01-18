import VueApexCharts from "vue3-apexcharts"

export default defineNuxtPlugin((nuxtApp) => {
  const globalOptions = {
    theme: {
      mode: 'dark'
    },
    colors: [
      '#FF1654',
      '#4CAF50',
      '#2196F3'
    ],
    tooltip: {
      theme: 'dark'
    },
    legend: {
      labels: {
        colors: '#ffffff'
      }
    },
    dataLabels: {
      style: {
        colors: ['#ffffff']
      }
    },
    xaxis: {
      labels: {
        style: {
          colors: '#ffffff'
        }
      },
      title: {
        style: {
          color: '#ffffff'
        }
      }
    },
    yaxis: {
      labels: {
        style: {
          colors: '#ffffff'
        }
      },
      title: {
        style: {
          color: '#ffffff'
        }
      }
    },
    grid: {
      borderColor: '#444'
    }
  }
  nuxtApp.vueApp.component("ApexCharts", VueApexCharts)
  nuxtApp.vueApp.config.globalProperties.$apexcharts = globalOptions
})