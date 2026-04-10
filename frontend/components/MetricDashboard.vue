<script setup>
import { computed, ref, watch } from 'vue'
import MultiSelect from './MultiSelect.vue'
import { Icon } from '@iconify/vue'

const { t } = useI18n()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const showMetrics = ref(false)
const dashboard = ref(null)

const props = defineProps({
  title: { type: String },
  metricOptions: { 
    type: Array, 
    required: true 
  },
  metricConfigMap: { 
    type: Object, 
    required: true 
  },
  itemParamName: { 
    type: String, 
    required: true 
  },
  itemId: { type: [String, Number], required: true },
  seasons: { type: Array, default: () => [] },
  initialSeason: { type: [String, Number], default: 'all-seasons' },
  initialMetricKeys: { type: Array, default: () => [] },
  refetchOnSeasonChange: { type: Boolean, default: true },
})

const title = computed(() => props.title ?? t('components.metricDashboard.selectMetrics'))
const selectedSeason = ref(props.initialSeason)
const selectedMetricKeys = ref([...(props.initialMetricKeys ?? [])])

watch(() => props.initialSeason, (newVal) => { 
  selectedSeason.value = newVal 
}, { immediate: true })
watch(() => props.initialMetricKeys, (newVal) => { 
  selectedMetricKeys.value = [...(newVal ?? [])] 
}, { deep: true })

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

function flattenResultToChartData(result) {
  const obj = Array.isArray(result) ? (result[0] ?? {}) : (result ?? {})
  const out = {}
  const ignoreKeys = ['player_id', 'team_id', 'season_id', 'id']

  for (const [key, value] of Object.entries(obj)) {
    if (ignoreKeys.includes(key.toLowerCase())) continue

    if (typeof value === "number" && Number.isFinite(value)) {
      out[key] = value

    } else if (value !== null && typeof value === "object" && !Array.isArray(value)) {
      for (const [subKey, subValue] of Object.entries(value)) {
        if (subKey.toLowerCase().includes("id")) continue
        if (typeof subValue === "number" && Number.isFinite(subValue)) {
          out[`${key}_${subKey}`] = subValue
        }
      }
    }
  }

  return out;
}

function extractMetricValue(raw, metricKey) {
  const conf = props.metricConfigMap?.[metricKey]
  const flat = flattenResultToChartData(raw)

  if (conf?.metricValue) {
    return flat[conf?.metricValue] ?? 0
  }
  return flat
}

const fetched = ref({})
const loading = ref(false)
const error = ref('')


async function fetchSelectedMetrics() {
  error.value = ''
  loading.value = true
  try {
    const results = await Promise.all(
      (selectedMetricKeys.value ?? []).map(async (metricKey) => {
        const endpoint = endpointForMetricKey(metricKey)
        if (!endpoint) return [metricKey, null]
        const url = new URL(endpoint, apiBase)
        url.searchParams.set(props.itemParamName, String(props.itemId))

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

// Metric Card Control
const metricCardsControl = computed (() => {
  const standAloneCards = []
  const sharedCards = {}
  for (const key of (selectedMetricKeys.value ?? [])) {
    const conf = props.metricConfigMap?.[key]
    const raw = fetched.value[key]
    const dataForChart = flattenResultToChartData(raw)
    if (!conf) continue
    standAloneCards.push({
      key,
      title: normalizedMetricOptions.value.find(o => o.key === key)?.label ?? key,
      allowedCharts: allowedChartsForMetricKey(key),
      dataForChart,
      hasData: Object.keys(dataForChart).length > 0,
      isPct: key.toLowerCase().includes('pct'),
      isShared: false,
    })
    
    if (!conf.sharedGraph) continue

    const groupSharedGraph = conf.sharedGraph.bar
    if (!groupSharedGraph) continue
    const sharedGraphId = groupSharedGraph.name
    if (!sharedCards[sharedGraphId]) {
      sharedCards[sharedGraphId] = {
        key: sharedGraphId,
        title: sharedGraphId.replace(/_bar$|_pie$/, '').replace(/_/g, ' '),
        allowedCharts: conf.allowedCharts,
        dataForChart: {},
        hasData: false,
        isPct: false,
        isShared: true,
      }
    }

    if (raw && Object.keys(dataForChart).length > 0) {
      sharedCards[sharedGraphId].dataForChart[key] = (extractMetricValue(raw, key))
      sharedCards[sharedGraphId].hasData = true

    }
  }

  return [...standAloneCards, ...Object.values(sharedCards)]
})
// Row Control
const rows = computed(() => {
  const cards = metricCardsControl.value
  const result = []
  let currentRow = []
  let pctCount = 0
  const maxPerRow = 3

  for (const card of cards) {
    if (card.isPct && pctCount >= 2) {
      if (currentRow.length > 0) result.push(currentRow)
      currentRow = [card]
      pctCount = 1
    } else {
      currentRow.push(card)
      if (card.isPct) pctCount++
    }

    if (currentRow.length >= maxPerRow) {
      result.push(currentRow)
      currentRow = []
      pctCount = 0
    }
  }

  if (currentRow.length > 0) result.push(currentRow)
  return result
})


watch(() => showMetrics.value, async (newVal) => {
  if (!newVal) return;
  await scrollToDashboard()
})
async function scrollToDashboard() {
  if (showMetrics.value) {
        await nextTick();
        const offset = 200
        const top = dashboard.value.getBoundingClientRect().top + window.scrollY - offset
        window.scrollTo({ top, behavior: 'smooth' })
    }
}
</script>

<template>
  <div @click="showMetrics = !showMetrics" class="title-with-arrows tooltip" :data-tooltip="$t('statistics.tooltips.showMetricOptions')" >
    <Icon icon="mdi:chevron-down" />
      <h2 class="stats-h2" id="metrics"> {{ $t('components.metricDashboard.selectMetrics') }} </h2>
    <Icon icon="mdi:chevron-down" />
  </div>
  <div v-if="showMetrics">
    <section class="md" ref="dashboard">
      <div class="md__top">
        <div class="md__left">
          <MultiSelect
            :options="normalizedMetricOptions"
            v-model="selectedMetricKeys"
            :placeholder="$t('components.metricDashboard.selectMetrics')"
            :confirmText="$t('common.select')"
            @confirm="onConfirm"
          />
        </div>

        <div class="md__right">
          <div class="md__seasonLabel">{{ $t('pages.teams.sections.seasonSelection') }}</div>
          <select v-model="selectedSeason" class="md__seasonSelect">
            <option value="all-seasons">{{ $t('pages.documentation.title') }}</option>
            <option v-for="s in seasons" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>
      </div>

      <div class="md__body">
        <p v-if="error" class="md__error">{{ error }}</p>
        <p v-else-if="loading" class="md__loading">{{ $t('common.loading') }}</p>

        <div v-else-if="!rows.length" class="md__empty">
          {{ $t('components.metricDashboard.selectMetrics') }} {{ $t('common.select') }} <strong>{{ $t('common.select') }}</strong>.
        </div>

        <div v-else class="md__grid">
          <div v-for="(row, rowIndex) in rows" :key="rowIndex" class="md__row">
            <div v-for="card in row" 
            :key="card.key" class="md__cardWrap" 
            :class="{ 'md__cardWrap--pct' : card.isPct}"
            >
              <h4 class="md__cardTitle">{{ card.title }}</h4>
              <div v-if="!card.hasData" class="md__noData">
                {{ $t('common.noData') }}
              </div>
              <DashboardCard v-else
                :chartOptions="card.allowedCharts"
                :dataForChart="card.dataForChart"
              />
            </div>
            <div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
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
  flex-direction: column;
  gap: 14px;
}

.md__row {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.md__cardWrap {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1 1 360px;
}

.md__cardWrap--pct {
  flex: 2 1 360px;
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