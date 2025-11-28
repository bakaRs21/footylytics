<script setup>
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const teamName = ref(route.params.teamName || "")
const selectedSeason = ref(route.query.season || "")
const { status, data: teamSeasons, error } = await useFetch(`${config.public.apiBase}teams/${teamName.value}`)

const stats = ref([])
const statsStatus = ref("")
const statsError = ref("")
const seasonSelected = async (season) => {
  selectedSeason.value = season
  router.push({ query: { ...route.query, season: season } })
  const { status: status, data: statsData, error: error } = await useFetch(`${config.public.apiBase}teams/${teamName.value}/season/${selectedSeason.value}`)
  stats.value = statsData.value
  statsStatus.value = status.value
  statsError.value = error.value
}
</script>
<template>
  <div class="page-heading">
        <h1 class ="h1-design">You've selected {{ teamName }}</h1>
  </div>
  <div v-if="status === 'pending'">
    Loading...
  </div>
  <div v-else-if="error">
    Error: {{ error.message }}
  </div>
  <div v-else>
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
    </div>
  </div>
</template>