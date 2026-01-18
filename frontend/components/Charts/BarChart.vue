<script setup>
import { computed } from 'vue';

const props = defineProps({
    series: Array,
    categories: Array,
    title: String,
})

const chartOptions = computed(() => ({
    xaxis: {
        categories: props.categories,
        labels: {
            style: {
                colors: "#fff",
            },
        },
    },
    yaxis: {
        labels: {
            style: {
                colors: "#fff",
            },
        },
    },
    tooltip: {
        theme: 'dark',
    },
    colors: ["#FF1654", "#247BA0", "#70C1B3", "#B2DBBF", "#F3FFBD"],
}))
</script>
<template>
<div>
    <ClientOnly>
        <ApexCharts width="400" type="bar" :series="series" :options="chartOptions" />
    </ClientOnly>
</div>
</template>
<style scoped>
</style>