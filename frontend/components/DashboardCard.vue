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
    <div class="dashboard-card card-dashboard">
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
  height: 320px;
}
.card-content {
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
