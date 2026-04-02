<script setup>
    import { ref, computed } from 'vue';
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

const data = ref(null)
function onSelectedKeysChange(selectedKeys) {
    data.value = selectedKeys;
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
                <ChartSelector  :chartOptions="chartOptions"
                v-model:selectedChart="selectedChart"
                />
            </div>
            <div class="header-right">
                <DataSelector :options="dataForChart" @update:selectedKeys="onSelectedKeysChange"/>
            </div>
        </div>
        <div class="card-content">
            <component v-if="selectedChart && data"
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
  background-color: #0f1923;
  overflow: hidden;
  border-radius: 16px;
  height: 320px;
  border: 1px solid #1e3a5f;
  box-shadow: 0 8px 22px 0 rgba(12, 41, 95, 0.5);
  transition:
    box-shadow 0.3s ease,
    transform 0.3s ease,
    border-color 0.3s ease;
}
.dashboard-card:hover {
  border-color: #2d5a8e;
  box-shadow: 0 12px 32px 0 rgba(12, 41, 95, 0.7);
  transform: translateY(-3px);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background-color: #1a2332;
  gap: 12px;
  border-bottom: 2px solid #2d3a4a;
  flex-wrap: wrap;
}
.card-content {
  display: flex;
  flex: 1;
  padding: 16px;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #0f1923 0%, #111822 100%);
  min-height: 295.5px;
}
.header-left {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    min-width: 0;
    flex-shrink: 0;
}
.header-right {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    min-width: 0;
    margin-left: auto;
}
</style>