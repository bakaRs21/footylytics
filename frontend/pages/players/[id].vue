<script setup>
import { ref, onMounted } from 'vue';
const config = useRuntimeConfig()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id || "")
const onMountedMsg = ref("")
const seasonParam = ref("")
const stats = ref(null)
const statsStatus = ref("")
const statsError = ref("")

const { data: playerInfo, error: playerInfoError } = await useFetch(`${config.public.apiBase}players/${id.value}`)
const { data: playerSeasons, error: playerSeasonsError } = await useFetch(`${config.public.apiBase}players/${id.value}/seasons`)

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
  seasonParam.value = ""
  if (season === 0) {
    await router.push({ query: { ...route.query, season: "all-seasons" } })
  } else {
    await router.push({ query: { ...route.query, season: season } })
  }
  Inspection()
}
function Inspection() {
  if (!route.query.season) {
    return onMountedMsg.value = "Please select a season to view the stats."
  } else if (!id.value || !route.query.season ) {
    return onMountedMsg.value = "Invalid player ID or season. Please select a valid season."
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
  <div v-if="playerInfoError">
    Error: {{ playerInfoError.message }}
  </div>
  <div v-else-if="playerInfo">
    <div class="page-heading"> 
      <h1 class="h1-design">{{ playerInfo.name }}</h1>
    </div>
    <div class="player-box">
      <div class="player-info">
        <table >
          <tr v-for="(val, key) in filterKyes(playerInfo)" :key="key">
            <td v-if="key != 'name'">{{ formatKey(key) }}</td><td v-if="key != 'name'">{{ val }}</td>
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
          <div v-for="(val, key) in filterKyes(playerSeasons)" :key="key" @click="() => selectSeason(val)">
            <Card>{{ val }}</Card>
          </div>
        </div>
        <div v-else-if="playerSeasonsError">
          <p>{{ playerSeasonsError.message }}</p>
        </div>
      </div>
    </div>
  </div>
  <div v-if="onMountedMsg">{{ onMountedMsg }}</div>
  <div v-if="statsStatus === 'pending'">
    Loading player stats...
    <Loading_svg />
  </div>
  <div v-else-if="statsError">
    Error loading stats: {{ statsError.message }}
  </div>
  <div v-else-if="stats">
    <PlayerStatsDashBoard :stats="stats" />
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