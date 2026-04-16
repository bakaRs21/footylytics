<script setup>
  import { onMounted, ref, watch } from 'vue'
  import ColorThief from 'colorthief'
  import { TEAM_METRIC_CONFIGS } from '~/composables/useMetricConfig.js';
  import { Icon } from '@iconify/vue';
  const { t } = useI18n()
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id || "")
const pageParam = 'team_id'
const selectedSeason = ref("")
const seasonParam = ref("")
const matchesSeasonParam = ref("")
const onMountedMsg = ref("")
const stats = ref({})
const statsStatus = ref("")
const statsError = ref("")
const matches = ref([])
const referees = ref([])
const showMatches = ref(false)
const showMetrics = ref(false)
const sections = [
  { label: t("pages.teams.sections.logo"), anchor: "top-section" },
  { label: t("pages.teams.sections.seasonSelection"), anchor: "seasons" },
  { label: t("pages.teams.sections.teamStats"), anchor: "stats" },
  { label: t("pages.teams.sections.matches"), anchor: "matches" },
  { label: t("pages.teams.sections.metricsSelection"), anchor: "metrics" },
]
watch(() => stats.value, (newVal) => {
  if (newVal === null) {
    selectedSeason.value = ""
  }
})
watch(() => showMetrics.value, async (newVal) => {
  await router.push({ query: { ...route.query, metrics: showMetrics.value }})
})

const { status: teamInfoStatus, data: teamInfo, error: teamInfoError } = await useFetch(`${config.public.apiBase}teams/${id.value}`)
const { data: teamSeasons, error: teamSeasonsError } = await useFetch(`${config.public.apiBase}teams/${id.value}/seasons`)
const { data: teamMetricOptions, error: teamMetricOptionsError } = await useFetch(`${config.public.apiBase}team-metrics/options`)

const secondary = ref("")
function extractColors() {
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.src = teamInfo.value.logo;
  img.onload = () => {
    const colorThief = new ColorThief();
    const palette = colorThief.getPalette(img, 3);
    secondary.value = `rgb(${palette[0].join(',')})`
    let teamNameColor = `rgb(${palette[1].join(',')})`
    if (
      teamInfo.value.name === "Liverpool" || teamInfo.value.name === "Nottingham Forest" || teamInfo.value.name === "Blackpool" || teamInfo.value.name === "Bolton"
    ) {
      secondary.value = `rgb(${[220, 220, 220].join(',')})`
      teamNameColor = `rgb(${[ 160, 16, 20 ].join(',')})`
      palette[0] = [210, 210, 210]
    }
    if (teamInfo.value.name === "Leeds") {
      secondary.value = `rgb(${palette[1].join(',')})`
      teamNameColor = `rgb(${palette[0].join(',')})`
      palette[0] = palette[1]
    }
    if (teamInfo.value.name === "Arsenal" || teamInfo.value.name === "Everton" || teamInfo.value.name === "Stoke City") {
      teamNameColor = `rgb(${[ 255, 255, 255 ].join(',')})`
    }
    document.documentElement.style.setProperty(
      '--teamNameColor',
      teamNameColor
    )
    document.documentElement.style.setProperty(
      '--stripe-main',
      secondary.value
    )
    document.documentElement.style.setProperty(
      '--stripe-dark',
      `rgb(${palette[0].map(v => Math.round(v*0.75)).join(',')})`
    )
  }
}
watch(() => teamInfo.value.logo, () => {
  extractColors()
})

function seasonSelected(season) {
  selectedSeason.value = season;
}
watch(() => selectedSeason.value, async (newSeason) => {
  seasonParam.value = ""
  if (newSeason === 0) {
    await router.replace({ query: { ...route.query, season: 'all-seasons' } })
  } else if (newSeason) {
    await router.replace({ query: { ...route.query, season: newSeason} })
  }
  await Inspection()
})
watch(() => matchesSeasonParam.value, async (newMatchesSeason) => {
  if (newMatchesSeason) {
    await router.replace({ query: { ...route.query, matchesSeason: newMatchesSeason} })
    await Inspection()
  }
})
async function Inspection() {
  if (!route.query.season || !route.query.matchesSeason) {
    onMountedMsg.value = t("pages.players.errorMessages.selectSeason")
  }
  if (route.query.season === "all-seasons") {
    seasonParam.value = ""
  }
  if (route.query.season) {
    seasonParam.value = `&season_id=${route.query.season}`
  }
  onMountedMsg.value = ""
  statsStatus.value = "pending"
  statsError.value = ""
  try {
    if (route.query.matchesSeason) {
      const matchData = await $fetch(`${config.public.apiBase}teams/${id.value}/matches/${route.query.matchesSeason}`)
      const refereesData = await $fetch(`${config.public.apiBase}referees`)
      matches.value = matchData
      referees.value = refereesData
    }
    if (route.query.season) {
      const data = await $fetch(`${config.public.apiBase}team-metrics/basic-stats?team_id=${id.value}${seasonParam.value}`)
      stats.value = data
    }
    statsStatus.value = ""
  } catch (error) {
    statsError.value = error.message
    statsStatus.value = "error"
  }
}

onMounted(() => {
  extractColors()
  Inspection()
})
</script>
<template>
  <div v-if="teamInfoStatus === 'pending'">
    {{ $t('common.loading') }} <Icon icon="mdi:loading" />
  </div>
  <div v-else-if="teamInfoError">
    Error: {{ teamInfoError.message }}
  </div>
  <div v-else>
    <div v-if="teamInfo" class="top-section team-top-section">
      <div class="team-card" :style="{backgroundColor: secondary}">
        <h4 id="top-section">{{ teamInfo.name }}</h4>
        <img :src="teamInfo.logo" :alt="teamInfo.name" />
      </div>
    </div>
    <div class="seasons">
      <div class="season-selection-heading">
        <h3 id="seasons">{{ $t('common.selectSeason') }}: </h3>
        <div class="all-seasons">
          <h3 id="allS">{{ $t('common.orDataFrom') }}</h3  >
          <button class="all-seasons-button" @click="seasonSelected(0)">{{ $t('common.allSeasons') }}</button>
        </div>
      </div>
      <div class="team-seasons">
        <Card v-if="!teamSeasonsError" v-for="season in teamSeasons" :key="season" @click="() => seasonSelected(season)">{{ season }}</Card>
        <p v-else-if="teamSeasonsError" class="error-message">{{ teamSeasonsError.message }}</p>
      </div>
      <div v-if="onMountedMsg" class="error-message">{{ onMountedMsg }}</div>
    </div>
    <div class="stats">
      <div v-if="statsStatus === 'pending'">
        {{ $t('common.loading') }}
        <Icon icon="mdi:loading" />
      </div>
      <div v-else-if="statsError">
        Error loading stats: {{ statsError.message }}
      </div>
      <div>
        <TeamStatsDashoBoard v-model="stats"/>
      </div>
    </div>
    <div class="matches">
      <div @click="showMatches = !showMatches" class="title-with-arrows" style="cursor: pointer;">
        <Icon icon="mdi:chevron-down" />
        <h2 id="matches">{{ $t('pages.teams.sections.matches') }}</h2>
        <Icon icon="mdi:chevron-down" />
      </div>
      <div class="seasons" v-if="showMatches" style="margin-bottom: 50px;">
        <div class="team-seasons">
          <Card v-for="season in teamSeasons" :key="season" @click="() => matchesSeasonParam = season">{{ season }}</Card>
        </div>
      </div>
      <div v-if="showMatches && matches.length > 0">
        <MatchesDashboard :matches="matches" :referees="referees" :page="'team'" />
      </div>
    </div>
    <div class="metrics">
        <div v-if="teamMetricOptionsError">
          Error loading metrics options: {{ teamMetricOptionsError.message}}
        </div>
        <MetricDashboard v-if="teamMetricOptions" title="metricOptions"
        :item-id="id" :item-param-name="pageParam" :seasons="teamSeasons"
        :metric-options="teamMetricOptions" :metric-config-map="TEAM_METRIC_CONFIGS"
        />
    </div>
  </div>

  <PageContent :page-sections="sections" />
</template>
<style scoped>
.team-top-section {
  display: flex;
  justify-content: center;
}

h4 {
    margin: 0;
    font-size: 32px;
    color: var(--teamNameColor);
}
.team-card {
  border-radius: 12px;
  width: 350px;
  height: 240px;
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: space-evenly;
  flex-shrink: 0;
  background: repeating-linear-gradient(
    -45deg,
    var(--stripe-main),
    var(--stripe-main) 20px,
    var(--stripe-dark) 22px,
    var(--stripe-dark) 50px
  );
  margin: 20px 10px 0 0;
}

.wrapper-heading {
  display: flex;
  flex-direction: row;
  gap: 80px;
  margin-bottom: 5px;
}
.all-seasons {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.team-seasons {
  display: flex;
  flex-wrap: wrap;
  flex: 1;
  gap: 5px;
}

.stats-h2 {
  margin-bottom: 0;
  font-size: 1.4rem;
  font-weight: 700;
  text-align: center;
}
</style>