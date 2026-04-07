<script setup>
import { Icon } from '@iconify/vue';
import { ref, onMounted } from 'vue';
import SeasonRankingTable from '~/components/SeasonRankingTable.vue';
import SeasonStats from '~/components/SeasonStats.vue';
const config = useRuntimeConfig()
const route = useRoute()
const selectedSeason = ref(` ${route.params.id} - ${Number(route.params.id) + 1} `)
const seasonParam = ref(route.params.id)
const onMountedMsg = ref("")
const stats = ref(null)
const statsStatus = ref("")
const statsError = ref("")
const rankings = ref(null)
const sections = [
  { label: "Season Stats", anchor: "stats" },
  { label: "Season Ranking", anchor: "metrics" },
]

function Inspection() {
  if (!seasonParam.value) {
    return onMountedMsg.value = "Season not selected. Please select a season to view the stats."
  }
  onMountedMsg.value = ""
  fetchData()
}
async function fetchData() {
  statsStatus.value = 'pending'
  statsError.value = ""
  try {
    const [first, second] = await Promise.all([
      $fetch(`${config.public.apiBase}season-metrics/stats?season_id=${seasonParam.value}`),
      $fetch(`${config.public.apiBase}season-metrics/team-ranking?season_id=${seasonParam.value}`)
    ])
    stats.value = first
    rankings.value = second
    statsStatus.value = ""
    console.log("rankings", rankings.value)
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
  <div v-if="onMountedMsg">
    {{ onMountedMsg }}
  </div>
  <div v-if="statsStatus === 'pending'">
    Loading stats... <Icon icon="mdi:loading" />
  </div>
  <div v-if="statsError">
    Error: {{ statsError }}
  </div>
  <div v-if="stats">
    <h2 class="h1-design" id="stats">{{ selectedSeason }} Stats</h2>
    <SeasonStats :data="stats" />
  </div>
  <div v-if="rankings">
    <h2 class="h1-design" id="metrics">{{ selectedSeason }} Rankings</h2>
    <SeasonRankingTable :teams="rankings" />
  </div>

  <PageContent :page-sections="sections" />
</template>