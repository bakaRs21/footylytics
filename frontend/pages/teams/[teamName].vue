<script setup>
const teamName = useRoute().params.teamName
String(teamName)
const config = useRuntimeConfig()
const { status, data: teamLeagues, error } = await useFetch(`${config.public.apiBase}api/team_seasons/${teamName}`, {
  lazy: true,
})

const selectedSeason = ref('')
const seasonData = ref(null)
const dataStatus = ref(false)
const dataError = ref(null)

const fetchSeasonData = async (season) => {
  if (!season) return

  dataStatus.value = true
  try {
    const { data: seasonDataResponse, error: seasonError } = await useFetch(`${config.public.apiBase}api/team_stats/${teamName}/${season}`, {
      lazy: true,
    })
    if (seasonError.value) {
      dataError.value = seasonError.value
      dataStatus.value = false
      return
    }
    seasonData.value = seasonDataResponse
  } catch (err) {
    dataError.value = err
    dataStatus.value = false
  }
  dataStatus.value = false
}


</script>
<template>
<pre>You've selected team: {{ teamName }}</pre>
<div v-if="status === 'pending'">
  Loading...
</div>
<div v-else-if="error">
  Error: {{ error.message }}
</div>
<div v-else>
  <h4>Select a season</h4>
  <select v-model="selectedSeason" v-for="teamLeague in teamLeagues" :key="teamLeague" @change="fetchSeasonData(selectedSeason)">
      <option disabled value="">Seasons</option>
      <option v-for="season in teamLeague" :key="season" :value="season">
        {{ season }}
      </option>
    </select>
    <div v-if="dataStatus === 'pending'">
      Loading season data...
    </div>
    <div v-else-if="dataError">
      Error loading season data: {{ dataError.message }}
    </div>
    <div v-else-if="seasonData">
      <h2>Data for {{ selectedSeason }}</h2>
      <div v-for="data in seasonData" :key="data">
        <pre>{{ data }}</pre>
      </div>
    </div>
</div>
</template>