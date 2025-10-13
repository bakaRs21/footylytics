<script setup>
const config = useRuntimeConfig()
const { team_names, error } = await useAsyncData("team_names", () => $fetch(`${config.public.apiBase}/api/team_names`))
console.log("Fetched team names:", team_names)
</script>

<template>
  <div>
    <h1>Teams Page</h1>
    <div v-if="error">Error: {{ error.message }}</div>
    <pre v-else>all teams: {{ team_names }}</pre>
  </div>
</template>