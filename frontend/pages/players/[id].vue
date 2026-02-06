<script setup>
import { ref } from 'vue';

const config = useRuntimeConfig()
const route = useRoute()
const router = useRoute()
const id = route.params.id
const selectedSeason = ref(route.query.season || "")

const { data: playerInfo, error: playerInfoError } = await useFetch(`${config.public.apiBase}players/${id}`)
const { data: playerSeasons, error: playerSeasonsError } = await useFetch(`${config.public.apiBase}players/${id}/seasons`)
const stats = ref(null)
const statsError = ref("")

function filterKyes(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([key, value]) =>
      !key.toLowerCase().includes('id') && value !== null)
    )
}
async function selectSeason(season) {
  const seasonParam = ref("")
  if (season === 0) {
    selectedSeason.value = "all-seasons"
    router.push({ query: { ...route.query, season: selectedSeason.value } })
  } else {
    selectedSeason.value = season
    router.push({ query: { ...route.query, season: selectSeason.value } })
    seasonParam.value = `?season_id=${season}`
  }
  const { data: playerStats, error } = await useFetch(`${config.public.apiBase}players/${id.value}/season/${seasonParam.value}`)
  stats.value = playerStats.value
  statsError.value = error.value
  console.log(`${config.public.apiBase}players/${id.value}/season/${seasonParam.value}`)
}
</script>
<template>
  <div v-if="playerInfoError">
    Error: {{ playerInfoError.message }}
  </div>
  <div v-else>
    <div class="page-heading"> 
      <h1 class="h1-design">You've selected {{ playerInfo.name }}</h1>
    </div>
    <div class="player-box">
      <div class="player-info">
        <table >
          <tr v-for="(val, key) in filterKyes(playerInfo)" :key="key">
            <td>{{ key }}</td><td>{{ val }}</td>
          </tr>
        </table>
      </div>
      <div class="player-seasons-wrapper">
        <div class="wrapper-heading">
          <h3 id="selectS">Select a season: </h3>
          <div class="all-seasons">
            <h3 id="allS">Or data from</h3  >
            <button class="all-seasons-button" @click="selectSeason(0)">All Seasons</button>
          </div>
        </div>
        <div class="player-seasons" v-if="!playerSeasonsError" >
          <div v-for="obj in playerSeasons">
            <Card v-for="(val, key) in filterKyes(obj)" :key="key" @click="() => selectSeason(val)">{{ val }}</Card>
          </div>
        </div>
        <div v-else-if="playerSeasonsError">
          <p>{{ playerSeasonsError.message }}</p>
        </div>
      </div>
    </div>
  </div>
  <div v-if="stats">
    {{ stats }}
  </div>
  <div v-else-if="statsError">
    {{ statsError.message }}
  </div>
</template>
<style scoped>
.player-box {
  display: flex;
  align-items: flex-start;
}
.player-info {
  display: flex;
  align-items: start;
  flex-direction: column;
  justify-content: space-evenly;
  flex-shrink: 0;
}
.player-seasons-wrapper {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  margin-left: 15px;
}
.wrapper-heading {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  gap: 250px;
  margin-bottom: 5px;
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

table, td {
  border: 1px solid white;
}
td {
  padding: 8px;
}
#selectS {
  margin-left: 20px;
}
</style>