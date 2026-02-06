<script setup>
  import { onMounted, ref } from 'vue'
  import ColorThief from 'colorthief'
import Card from '~/components/card.vue'
import Loading_svg from '~/components/Icons/loading_svg.vue'
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id || "")
const selectedSeason = ref(route.query.season || "")
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
    let teamNameColor = `rgb(${[240, 240, 240].join(',')})`
    if (teamInfo.value.name === "Liverpool") {
      secondary.value = `rgb(${[220, 220, 220].join(',')})`
      teamNameColor = `rgb(${[ 160, 16, 20 ].join(',')})`
      palette[0] = [210, 210, 210]
    }
    document.documentElement.style.setProperty(
      '--teamNameColor',
      teamNameColor
    )
    document.documentElement.style.setProperty(
      '--stripe-main',
      secondary.value
    )
    const darker = palette[0].map(v => Math.round(v * 0.75))
    document.documentElement.style.setProperty(
      '--stripe-dark',
      `rgb(${darker.join(',')})`
    )
  }
}
onMounted(() => {
  extractColors()
})
watch(() => teamInfo.value.logo, () => {
  extractColors()
})
const { data: teamSeasons, error: teamSeasonsError } = await useFetch(`${config.public.apiBase}teams/${id.value}/seasons`)
let stats = ref(null)
const statsStatus = ref("")
const statsError = ref("")
const seasonSelected = async (season) => {
  const { status: status, data: statsData, error: error } = await useFetch(`${config.public.apiBase}teams/${id.value}/season/${selectedSeason.value}`)
  if (season === "all") {
    selectedSeason.value = "all-seasons"
    router.push({ query: { ...route.query, season: selectedSeason.value } })
  } else {
    selectedSeason.value = season
    router.push({ query: { ...route.query, season: season } })
  }
  const { status: status, data: statsData, error } = await useFetch(`${config.public.apiBase}teams/${id.value}/season/${seasonParam.value}`)
  console.log(`Fetching from: ${config.public.apiBase}teams/${id.value}/season/${seasonParam.value}`)
  stats.value = statsData.value
  statsStatus.value = status.value
  statsError.value = error.value
}


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
    <div v-if="statsStatus === 'pending'">
      Loading stats...
      <Loading_svg />
    </div>
    <div v-else-if="statsError">
      Error loading stats: {{ statsError.message }}
    </div>
    <div v-else-if="stats">
      <h3>Statistics for season {{ selectedSeason }}:</h3>
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