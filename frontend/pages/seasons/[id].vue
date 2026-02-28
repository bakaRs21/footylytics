<script setup>
import { ref, onMounted } from 'vue';
const config = useRuntimeConfig()
const route = useRoute()
const selectedSeason = ref(route.params.id || "")
const onMountedMsg = ref("")
const stats = ref(null)
const statsStatus = ref("")
const statsError = ref("")

function Inspection() {
  if (!selectedSeason.value) {
    return onMountedMsg.value = "Season not selected. Please select a season to view the stats."
  }
  onMountedMsg.value = ""
  fetchData()
}
async function fetchData() {
  statsStatus.value = 'pending'
  statsError.value = ""
  try {
    const data = await $fetch(`${config.public.apiBase}season-metrics/stats?season_id=${selectedSeason.value}`)
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
  <div v-if="onMountedMsg">
    {{ onMountedMsg }}
  </div>
  <div v-if="statsStatus === 'pending'">
    Loading stats...
  </div>
  <div v-if="statsError">
    Error: {{ statsError }}
  </div>
  <div v-if="stats">
    <h2>Season Stats for {{ selectedSeason }}</h2>
  </div>
</template>