<script setup>
import { watch, onMounted } from 'vue';
const props = defineProps({
    chartOptions: {
        type: Array,
        required: true,
    },
})
const emitSelectedChart = defineEmits(['update:selectedChart']);
const selectedChart = defineModel('modelValue', {
    type: String,
    required: true,
})

watch(selectedChart, (newChart) => {
    emitSelectedChart('update:selectedChart', newChart);
});
onMounted(() => {
    if (props.chartOptions.length > 0 && !selectedChart.value) {
    selectedChart.value = props.chartOptions[0];
}
})
</script>
<template>
<div class="input-container">
    <label v-for="option in chartOptions" :key="option" class="option">
        <input type="radio" :value="option" v-model="selectedChart"/>
        {{ option }}
    </label>
</div>
</template>
<style scoped>
div, label, input {
    cursor: pointer;
}
</style>