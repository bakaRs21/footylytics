<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
    series: {
        type: Array,
        required: true,
    },
    labels: {
        type: Array,
        required: true,
    },
})

const chartOptions = computed(() => ({
    labels: props.labels,
        style: {
            colors: "#fff",
        },
        legend: {
            labels: {
                colors: "#fff",
            },
        },
    tooltip: {
        theme: 'dark',
    },
    colors: ['#4CAF50', '#FFC107', '#F44336', '#2196F3', '#9C27B0', '#FF5722'],
}))
</script>

<template>
<div>
    <ClientOnly>
        <ApexCharts width="400" type="pie" :options="chartOptions" :series="props.series"></ApexCharts>
    </ClientOnly>
</div>
</template>