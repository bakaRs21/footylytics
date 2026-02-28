<script setup>
  import { onMounted, ref } from 'vue'
  import ColorThief from 'colorthief'
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id || "")
const selectedSeason = ref(route.query.season || "")
const seasonParam = ref("")
const onMountedMsg = ref("")
const stats = ref(null)
const statsStatus = ref("")
const statsError = ref("")

const { status: teamInfoStatus, data: teamInfo, error: teamInfoError } = await useFetch(`${config.public.apiBase}teams/${id.value}`)

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
const { data: teamSeasons, error: teamSeasonsError } = await useFetch(`${config.public.apiBase}teams/${id.value}/seasons`)
const seasonSelected = async (season) => {
  seasonParam.value = ""
  if (season === 0) {
    selectedSeason.value = "all-seasons"
  } else {
    selectedSeason.value = season
  }
  await router.push({ query: { ...route.query, season: selectedSeason.value } })
  Inspection()
}
function Inspection() {
  if (!route.query.season) {
    return onMountedMsg.value = "Please select a season to view the stats."
  } else if (!id.value || !selectedSeason.value ) {
    return onMountedMsg.value = "Invalid team ID or season. Please select a valid season."
  }
  if (route.query.season === "all-seasons") {
    seasonParam.value = ""
  } else if (route.query.season) {
    seasonParam.value = `&season_id=${route.query.season}`
  }
  onMountedMsg.value = ""
  fetchData()
}
async function fetchData() {
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
    <div class="team-box">
      <div class="team-card" :style="{backgroundColor: secondary}">
        <h4>{{ teamInfo.name }}</h4>
        <img :src="teamInfo.logo" :alt="teamInfo.name" />
      </div>
      <div class="team-seasons-wrapper">
        <div class="wrapper-heading">
          <h4 id="selectS">Select a season: </h4>
          <div class="all-seasons">
            <h4 id="allS">Or data from</h4>
            <button class="all-seasons-button" @click="seasonSelected(0)">All Seasons</button>
          </div>
        </div>
        <div class="team-seasons">
          <Card v-if="!teamSeasonsError" v-for="season in teamSeasons" :key="season" @click="() => seasonSelected(season)">{{ season }}</Card>
          <p v-else-if="teamSeasonsError">{{ teamSeasonsError.message }}</p>
        </div>
      </div>
    </div>
    <div v-if="onMountedMsg">
      {{ onMountedMsg }}
    </div>
    <div v-if="statsStatus === 'pending'">
      Loading stats...
      <Loading_svg />
    </div>
    <div v-else-if="statsError">
      Error loading stats: {{ statsError.message }}
    </div>
    <div v-else-if="stats">
      <TeamStatsDashoBoard :stats="stats" />
    </div>
  </div>
</template>
<style scoped>
.team-box {
  display: flex;
  align-items: flex-start;
  margin-top: 20px;
}
h4 {
    margin: 0;
    font-size: 32px;
    color: var(--teamNameColor);
}
#selectS {
  margin-left: 20px;
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
.team-seasons-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex: 1;
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
</style>