<script setup>
  import { onMounted, ref, watch } from 'vue'
  import ColorThief from 'colorthief'
  import { TEAM_METRIC_CONFIGS } from '~/composables/useMetricConfig.js';
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id || "")
const pageParam = 'team_id'
const selectedSeason = ref("")
const seasonParam = ref("")
const onMountedMsg = ref("")
const stats = ref(null)
const statsStatus = ref("")
const statsError = ref("")
const showMetrics = ref(false)
const sections = [
  { label: "Team Logo", anchor: "team-logo" },
  { label: "Season Selection", anchor: "season-selection" },
  { label: "Team Statistics", anchor: "team-stats" },
  { label: "Team Metrics", anchor: "metrics" },
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
watch(() => selectedSeason.value, async (newVal) => {
  seasonParam.value = ""
  if (newVal === 0) {
    await router.replace({ query: { ...route.query, season: 'all-seasons' } })
  } else {
    await router.replace({ query: { ...route.query, season: newVal} })
  }
  await Inspection()
})
async function Inspection() {
  if (!route.query.season) {
    return onMountedMsg.value = "Please select a season to view the stats."
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
    const data = await $fetch(`${config.public.apiBase}team-metrics/basic-stats?team_id=${id.value}${seasonParam.value}`)
    stats.value = data
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
    Loading...
  </div>
  <div v-else-if="teamInfoError">
    Error: {{ teamInfoError.message }}
  </div>
  <div v-else>
    <div v-if="teamInfo" class="top-section team-top-section">
      <div class="team-card" :style="{backgroundColor: secondary}">
        <h4 id="team-logo">{{ teamInfo.name }}</h4>
        <img :src="teamInfo.logo" :alt="teamInfo.name" />
      </div>
    </div>
    <div class="seasons">
      <div class="season-selection-heading">
        <h3 id="season-selection">Select a season: </h3>
        <div class="all-seasons">
          <h3 id="allS">Or data from</h3  >
          <button class="all-seasons-button" @click="seasonSelected(0)">All Seasons</button>
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
        Loading stats...
        <Loading_svg />
      </div>
      <div v-else-if="statsError">
        Error loading stats: {{ statsError.message }}
      </div>
      <div id="team-stats">
        <TeamStatsDashoBoard v-model="stats"/>
      </div>
    </div>
    <div class="metrics">
      <div @click="showMetrics = !showMetrics" class="title-with-arrows tooltip" data-tooltip="Show metric options to be selected" >
      <ArrowDown />
        <h2 class="stats-h2" id="metrics"> Metrics </h2>
      <ArrowDown />
      </div>
      <div v-show="showMetrics">
        <div v-if="teamMetricOptionsError">
          Error loading metrics options: {{ teamMetricOptionsError.message}}
        </div>
        <MetricDashboard v-if="teamMetricOptions" title="metricOptions"
        :entity-id="id" :entity-param-name="pageParam" :seasons="teamSeasons"
        :metric-options="teamMetricOptions" :metric-config-map="TEAM_METRIC_CONFIGS"
        />
      </div>
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