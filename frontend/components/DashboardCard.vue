<script setup>
    import { ref } from 'vue';
import DataSelector from './DataSelector.vue';
import BarChart from './Charts/BarChart.vue';
import DonutChart from './Charts/DonutChart.vue';
import LineChart from './Charts/LineChart.vue';
import PieChart from './Charts/PieChart.vue';

const props = defineProps({
    chartOptions: {
        type: Array,
        required: true,
    },
    dataForChart: {
        type: Object,
        required: true,
    },
})
const selectedChart = ref(null)
function onChartChange(chart) {
    selectedChart.value = chart;
}
const data = ref(null)
function onSelectedKeysChange(selectedKeys) {
    data.value = selectedKeys;
    processData(data.value)
}
const chartMap = {
    "Bar Chart": BarChart,
    "Donut Chart": DonutChart,
    "Line Chart": LineChart,
    "Pie Chart": PieChart,
}
const processData = computed(() => {
    if (!selectedChart.value || !data.value) return null;
    switch (selectedChart.value) {
        case "Pie Chart":
        case "Donut Chart":
            return {
                series: data.value.map(item => item.value),
                labels: data.value.map(item => formatLabel(item.key)),
            }
        case "Line Chart":
        case "Bar Chart":
            return {
                series: [{
                    name: "Stats",
                    data: data.value.map(item => item.value)
                }],
                categories: data.value.map(item => formatLabel(item.key)),
            }
        default:
            return null;
    }
})
function formatLabel(label) {
    return label.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}
</script>
<template>
    <div class="dashboard-card">
        <div class="card-header">
            <div class="header-left">
                <ChartSelector
                :chartOptions="chartOptions"
                @update:selectedChart="onChartChange"
                />
            </div>
            <div class="header-right">
                <DataSelector :options="dataForChart" @update:selectedKeys="onSelectedKeysChange"/>
            </div>
        </div>
        <div class="card-content">
            <component v-if="selectedChart"
            :is="chartMap[selectedChart]" v-bind="processData"
            />
        </div>
    </div>
</template>
<style scoped>
.dashboard-card {
  display: flex;
  flex-direction: column;
  flex: 1;
  background-color: #3a3a3a;
  overflow: hidden;
  border-radius: 12px;
  height: 320px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 10px;
  background-color: #494949;
  gap: 5px;
  border-bottom: 2px solid #141414;
  flex-wrap: wrap;
}
.card-content {
  display: flex;
  flex: 1;
  padding: 10px;
  align-items: center;
  justify-content: center;
}
.header-left,
.header-right {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    min-width: 0;
}
.header-left > *,
.header-right > * {
  flex: 1 1 160px;
}
.header-right {
    margin: auto;
}
</style>