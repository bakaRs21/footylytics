<script setup>
const config = useRuntimeConfig()
const { status, data: team_names, error } = await useFetch(`${config.public.apiBase}/api/team_names`, {
  lazy: true,
})
console.log("Fetched team names:", team_names)
</script>

<template>
  <h1>Teams Page</h1>
  <div>
    <div v-if="status === 'pending'">
      Loading...
    </div>
    <div v-else-if="error">
      Error: {{ error.message }}
    </div>
    <div v-else>
      <div v-for="(team, index) in team_names" :key="index">
        <pre>{{ team }}</pre>
      </div>
    </div>
  </div>
</template>