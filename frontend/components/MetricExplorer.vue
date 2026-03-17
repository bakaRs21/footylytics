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
  allMetrics.value.find(m => m.key === selectedMetricKey.value) ?? ""
)
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