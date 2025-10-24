<script setup>
const config = useRuntimeConfig()
const { status, data: teams, error } = await useFetch(`${config.public.apiBase}/api/teams`, {
  lazy: true,
})
console.log("Fetched teams:", teams)
</script>

<template>
  <div class="container">
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
        <pre><NuxtLink :to="`/teams/${teamName}`">{{ team.name }}</NuxtLink></pre>
      </div>
    </div>
  </div>
  </div>
</template>