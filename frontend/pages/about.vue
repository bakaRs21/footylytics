<script setup>
const config = useRuntimeConfig()
const { data, error } = await useFetch(`${config.public.apiBase}`)
const { data: teams, error: teamsError } = await useFetch(`${config.public.apiBase}api/teams`)

const selectedTeam = ref(null)
</script>

<template>
  <div class="container">
  <div>
    <h3>Nuxt SSSR + FastAPI</h3>
    <div v-if="error">Error: {{ error.message }}</div>
    <pre v-else>{{ data }}</pre>
  </div>

  <div>
    <h2>Team Dashboard</h2>
    <select v-model="selectedTeam">
      <option disabled value="">Please select a team</option>
      <option v-for="(team, index) in teams" :key="index" :value="team.name">
        {{ team.name }}
      </option>
    </select>
  </div>
  </div>
</template>