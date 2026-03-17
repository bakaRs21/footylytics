<script setup>
import { computed, ref, watch } from 'vue'
import MultiSelect from './MultiSelect.vue'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const props = defineProps({
  title: { type: String, default: 'Metrics' },
  metricOptions: { type: Array, required: true },
  metricConfigMap: { type: Object, required: true },
  entityParamName: { type: String, required: true },
  entityId: { type: [String, Number], required: true },
  seasons: { type: Array, default: () => [] },
  initialSeason: { type: [String, Number], default: 'all-seasons' },
  initialMetricKeys: { type: Array, default: () => [] },
  refetchOnSeasonChange: { type: Boolean, default: true },
})

const selectedSeason = ref(props.initialSeason)
const selectedMetricKeys = ref([...(props.initialMetricKeys ?? [])])

watch(() => props.initialSeason, v => { selectedSeason.value = v }, { immediate: true })
watch(() => props.initialMetricKeys, v => { selectedMetricKeys.value = [...(v ?? [])] }, { deep: true })

const normalizedMetricOptions = computed(() => {
  return (props.metricOptions ?? [])
    .filter(m => !!props.metricConfigMap?.[m.key])
    .map(m => ({ key: m.key, label: m.label ?? m.key }))
})

function seasonQueryParam() {
  if (!selectedSeason.value || selectedSeason.value === 'all-seasons') return ''
  return `&season_id=${encodeURIComponent(String(selectedSeason.value))}`
}

function endpointForMetricKey(metricKey) {
  const cfg = props.metricConfigMap?.[metricKey]
  return cfg?.endpoint ?? null
}

function allowedChartsForMetricKey(metricKey) {
  const cfg = props.metricConfigMap?.[metricKey]
  return cfg?.allowedCharts ?? ['Bar Chart', 'Line Chart', 'Pie Chart', 'Donut Chart']
}

function numericObjectFromResult(result) {
  const obj = Array.isArray(result) ? (result[0] ?? {}) : (result ?? {})
  const out = {}
  for (const [k, v] of Object.entries(obj)) {
    if (k.toLowerCase().includes('id')) continue
    if (typeof v === 'number' && Number.isFinite(v)) out[k] = v
  }
  return out
}

const fetched = ref({})
const loading = ref(false)
const error = ref('')

const metricCards = computed(() => {
  return (selectedMetricKeys.value ?? []).map(key => {
    const raw = fetched.value[key]
    return {
      key,
      title: normalizedMetricOptions.value.find(o => o.key === key)?.label ?? key,
      allowedCharts: allowedChartsForMetricKey(key),
      dataForChart: numericObjectFromResult(raw),
      hasData: Object.keys(numericObjectFromResult(raw)).length > 0,
    }
  })
})

async function fetchSelectedMetrics() {
  error.value = ''
  loading.value = true
  try {
    const results = await Promise.all(
      (selectedMetricKeys.value ?? []).map(async (metricKey) => {
        const endpoint = endpointForMetricKey(metricKey)
        if (!endpoint) return [metricKey, null]
        const url = new URL(endpoint, apiBase)
        url.searchParams.set(props.entityParamName, String(props.entityId))

        if (selectedSeason.value && selectedSeason.value !== 'all-seasons') {
          url.searchParams.set('season_id', String(selectedSeason.value))
        }

        const data = await $fetch(url.toString())
        return [metricKey, data]
      })
    )

    const next = {}
    for (const [key, value] of results) next[key] = value
    fetched.value = next
  } catch (e) {
    error.value = e?.data?.detail ?? e?.message ?? 'Failed to fetch metrics'
  } finally {
    loading.value = false
  }
}

async function onConfirm(keys) {
  selectedMetricKeys.value = [...(keys ?? [])]
  await fetchSelectedMetrics()
}

watch(selectedSeason, async () => {
  if (!props.refetchOnSeasonChange) return
  if (!Object.keys(fetched.value ?? {}).length) return
  await fetchSelectedMetrics()
})
</script>

<template>
  <section class="md">
    <div class="md__top">
      <div class="md__left">
        <MultiSelect
          :options="normalizedMetricOptions"
          v-model="selectedMetricKeys"
          placeholder="Select metrics…"
          confirmText="Confirm"
          @confirm="onConfirm"
        />
      </div>

      <div class="md__right">
        <div class="md__seasonLabel">filter to season</div>
        <select v-model="selectedSeason" class="md__seasonSelect">
          <option value="all-seasons">all seasons</option>
          <option v-for="s in seasons" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
    </div>

    <div class="md__body">
      <p v-if="error" class="md__error">{{ error }}</p>
      <p v-else-if="loading" class="md__loading">Fetching metrics…</p>

      <div v-else-if="!metricCards.length" class="md__empty">
        Select metrics and press <strong>Confirm</strong>.
      </div>

      <div v-else class="md__grid">
        <div v-for="card in metricCards" :key="card.key" class="md__cardWrap">
          <h4 class="md__cardTitle">{{ card.title }}</h4>

          <div v-if="!card.hasData" class="md__noData">
            Make sure to confirm your selection
          </div>

          <DashboardCard v-else
            :chartOptions="card.allowedCharts"
            :dataForChart="card.dataForChart"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.md {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.md__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  width: 100%;
}

.md__left {
  display: flex;
  align-items: flex-start;
}

.md__right {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.md__seasonLabel {
  font-size: 12px;
  color: #a0aec0;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding-top: 10px;
}

.md__seasonSelect {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #374153;
  background: #111822;
  color: white;
}

.md__body {
  min-height: 120px;
}

.md__error {
  color: #f87171;
}

.md__loading,
.md__empty {
  color: #a0aec0;
}

.md__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 14px;
}

.md__cardWrap {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.md__cardTitle {
  margin: 0;
  font-size: 14px;
  color: #cbd5e1;
}

.md__noData {
  color: #a0aec0;
  border: 1px solid #374153;
  border-radius: 10px;
  background: #111822;
  padding: 14px;
}
</style>