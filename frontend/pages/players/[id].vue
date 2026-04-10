<script setup>
  import { Icon } from '@iconify/vue';
  import { ref, onMounted, watch } from 'vue';
  import { PLAYER_METRIC_CONFIGS } from '~/composables/useMetricConfig.js';
  const { t } = useI18n()
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id || "")
const pageParam = 'player_id'
const onMountedMsg = ref("")
const selectedSeason = ref("")
const seasonParam = ref("")
const stats = ref({})
const statsStatus = ref("")
const statsError = ref("")
const pageSections = [
  { label: t("pages.players.sections.playerInfo"), anchor: "top-section" },
  { label: t("pages.players.sections.seasonSelection"), anchor: "seasons" },
  { label: t("pages.players.sections.playerStats"), anchor: "stats" },
  { label: t("pages.players.sections.playerMetrics"), anchor: "metrics" },
]

watch(() => stats.value, (newVal) => {
  if (newVal === null) {
    selectedSeason.value = ""
  }
})

const { data: playerInfo, error: playerInfoError } = await useFetch(`${config.public.apiBase}players/${id.value}`)
const { data: playerSeasons, error: playerSeasonsError } = await useFetch(`${config.public.apiBase}players/${id.value}/seasons`)
const { data: playerMetricOptions, error: playerMetricOptionsError } = await useFetch(`${config.public.apiBase}player-metrics/options`)


function filterKyes(obj) {
  const flat = {}
  for (const [key, value] of Object.entries(obj ?? {})) {
    if (typeof value === 'object' && value !== null) {
      Object.assign(flat, value)
    } else {
      flat[key] = value
    }
  }
  return Object.fromEntries(Object.entries(flat).filter(([key, value]) =>
      !key.toLowerCase().includes('id') && value !== null)
  )
}
function formatKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase())
}

async function selectSeason(season) {
  selectedSeason.value = season
}
watch(() => selectedSeason.value, async (newVal) => {
  seasonParam.value = ""
  if (newVal === 0) {
    await router.replace({ query: { ...route.query, season: "all-seasons" } })
  } else if (newVal || !newVal) {
    await router.replace({ query: { ...route.query, season: newVal } })
  }
  await Inspection()
})
async function Inspection() {
  if (!route.query.season) {
    return onMountedMsg.value = $t("pages.players.errorMessages.selectSeason")
  }
  if (route.query.season === "all-seasons") {
    seasonParam.value = ""
  } else if (route.query.season) {
    seasonParam.value = `&season_id=${route.query.season}`
  }
  onMountedMsg.value = ""
  statsStatus.value = "pending"
  statsError.value = ""
  try {
    const data = await $fetch(`${config.public.apiBase}player-metrics/basic-stats?player_id=${id.value}${seasonParam.value}`)
    stats.value = data
    statsStatus.value = ""
  } catch (error) {
    statsError.value = error.message
    statsStatus.value = "error"
  }
}

onMounted(() => {
  Inspection()
})
</script>
<template>
  <div v-if="playerInfoError" class="error-message">
    Error: {{ playerInfoError.message }}
  </div>
  <div v-else-if="playerInfo" class="top-section">
    <div class="page-heading"> 
      <h1 class="h1-design" id="top-section">{{ playerInfo.name }}</h1>
    </div>
    <div class="player-info">
      <table class="info-table">
        <tr v-for="(val, key) in filterKyes(playerInfo)" :key="key">
          <td v-if="key != 'name'" class="info-key">{{ formatKey(key) }}</td>
          <td v-if="key != 'name'" class="info-val">{{ val }}</td>
        </tr>
      </table>
    </div>
  </div>
  <div class="seasons">
    <div class="season-selection-heading">
      <h3 id="seasons">{{ t('common.selectSeason') }} : </h3>
      <div class="all-seasons">
        <h3 id="allS">{{ t('common.orDataFrom') }}</h3  >
        <button class="all-seasons-button" @click="selectSeason(0)">{{ t('common.allSeasons') }}</button>
      </div>
    </div>
    <div class="player-seasons" v-if="!playerSeasonsError" >
      <div v-for="(val, key) in filterKyes(playerSeasons)" :key="key" @click="() => selectSeason(val)">
        <Card>{{ val }}</Card>
      </div>
    </div>
    <div v-else-if="playerSeasonsError" class="error-message">
      <p>{{ playerSeasonsError.message }}</p>
    </div>
    <div v-if="onMountedMsg" class="error-message">{{ onMountedMsg }}</div>
  </div>
  <div class="stats">
    <div v-if="statsStatus === 'pending'">
      {{ t('common.loading') }} <Icon icon="mdi:loading" />
    </div>
    <div v-else-if="statsError" class="error-message">
      {{ t('errors.loadingFailed') }}: {{ statsError.message }}
    </div>
    <div id="stats">
      <PlayerStatsDashBoard v-model="stats" />
    </div>
  </div>
  <div class="metrics">
      <div v-if="playerMetricOptionsError">
        Error loading metric options: {{  playerMetricOptionsError.message }}
      </div>
      <MetricDashboard v-if="playerMetricOptions" title="metricOptions"
      :item-id="id" :item-param-name="pageParam" :seasons="playerSeasons" 
      :metric-options="playerMetricOptions" :metric-config-map="PLAYER_METRIC_CONFIGS"
      />
  </div>

  <PageContent :page-sections="pageSections" />
</template>
<style scoped>
.player-info {
  display: flex;
  justify-content: center;
  align-items: space-evenly;
  flex-shrink: 0;
  margin-top: 20px;
}

td {
  padding: 10px 20px 10px 20px;
}

.info-table {
  width: 100%;
  font-size: 1.1rem;
  border-collapse: collapse;
  display: flex;
  justify-content: space-evenly;
}

.info-table tr {
  border-bottom: 1px solid rgba(255, 255, 255, 0.281);
  transition: background 0.15s ease;
}
.info-table tr:hover {
  background: rgba(255, 255, 255, 0.05);
}

.info-key {
  color: #aaa;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  white-space: nowrap;
  width: 1%; 
}

.info-val {
  color: #fff;
  width: 100%;
} 



.all-seasons {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}
.player-seasons {
  display: flex;
  flex-wrap: wrap;
  flex: 1;
  gap: 5px;
}

#selectS {
  margin-left: 20px;
}

</style>