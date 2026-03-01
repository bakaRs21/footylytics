const availableCharts = computed(() => {
  switch (spec.value.kind) {
    case 'minuteBuckets':
    case 'bar':
      return ['Bar Chart', 'Line Chart']  // both work perfectly
    case 'donut':
      return ['Donut Chart', 'Pie Chart']
    case 'pie':
      return ['Pie Chart', 'Donut Chart']
    default:
      return ['Bar Chart']
  }
})