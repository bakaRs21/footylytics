<script setup>
import { computed } from "vue";

const props = defineProps({
    series: Array,
    categories: Array,
    title: String
})

const chartOptions = computed(() => ({
  ...$apexcharts,
  xaxis: {
    categories: props.categories,
  },
  stroke: { curve: "smooth" },
}))
</script>
<template>
<div>
  <ClientOnly>
    <ApexCharts id="apexchart" type="line" width="400" :series="props.series" :options="chartOptions" />
  </ClientOnly>
</div>
</template>
<style scoped>
#apexchart {
  width: 300px;
}
</style>
