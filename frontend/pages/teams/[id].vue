<script setup>
  import { onMounted, ref } from 'vue'
  import ColorThief from 'colorthief'
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


const stats = ref([])
const statsStatus = ref("")
const statsError = ref("")
const seasonSelected = async (season) => {
  selectedSeason.value = season
  router.push({ query: { ...route.query, season: season } })
  const { status: status, data: statsData, error: error } = await useFetch(`${config.public.apiBase}teams/${id.value}/season/${selectedSeason.value}`)
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
    
    <div class="team" :style="{backgroundColor: secondary}">
      <h4>{{ teamInfo.name }}</h4>
      <img :src="teamInfo.logo" :alt="teamInfo.name" />
    </div>
    <!--
    <h4>Select a season</h4>
    <select v-model="selectedSeason" v-for="seasons in teamSeasons" :key="seasons">
      <option disabled value="" >Seasons</option>
      <option v-for="season in seasons" :key="season" :value="season" @click="() => seasonSelected(season)">{{ season }}</option>
    </select>
    <div v-if="selectedSeason">
      <div v-if="statsStatus === 'pending'">
        Loading stats...
      </div>
      <div v-else-if="statsError">
        Error loading stats: {{ statsError.message }}
      </div>
      <div v-else v-for="stat in stats" :key="stat">
        {{ stat }}
      </div>
    </div>-->
  </div>
</template>
<style scoped>
  h4 {
    margin: 0;
    font-size: 32px;
    color: var(--teamNameColor);
  }
.team {
  border-radius: 12px;
  width: 350px;
  height: 230px;
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: space-evenly;
  background: repeating-linear-gradient(
    -45deg,
    var(--stripe-main),
    var(--stripe-main) 20px,
    var(--stripe-dark) 22px,
    var(--stripe-dark) 50px
  );
}
</style>