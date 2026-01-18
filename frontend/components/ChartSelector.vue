<script setup>
import { computed } from 'vue';

const props = defineProps({
    chartOptions: {
        type: Array,
        required: true,
    },
})

const selectedChart = defineModel('modelValue', {
    type: String,
    required: true,
})
const emitSelectedChart = defineEmits(['update:selectedChart']);
const selectChart = computed(() => {
    return (chart) => {
        emitSelectedChart('update:selectedChart', chart);
    }
});
</script>
<template>
<div class="input-container">
    <label v-for="option in chartOptions" :key="option" class="option" @click="() => selectChart(option)">
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