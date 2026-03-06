<script setup>
import { useMetrics } from '~/composables/useMetrics.js'

const { loadMetricOptions, mergedPlayerMetrics, mergedTeamMetrics, loading } = useMetrics()

onMounted(() => loadMetricOptions())

const domain = ref('player')
const allMetrics = computed(() =>
  domain.value === 'player' ? mergedPlayerMetrics.value : mergedTeamMetrics.value
)

const selectedMetricKey = ref(null)
const selectedMetric = computed(() =>
  allMetrics.value.find(m => m.key === selectedMetricKey.value) ?? null
)

// selectedMetric now has everything:
// .label         — from backend
// .params        — from backend (drives the filter inputs dynamically)
// .allowedCharts — from frontend config
// .toChartData   — from frontend config
</script>
<template>
    <div v-for="param in selectedMetric.params" :key="param.name" class="filter-group">
    <label>{{ param.name }} {{ param.required ? '*' : '(optional)' }}</label>
    <input
        v-model.number="filterValues[param.name]"
        type="number"
        :placeholder="param.help ?? param.name"
    />
    </div>
</template>