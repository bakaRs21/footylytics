<script setup>
const config = useRuntimeConfig()
const { status, data: teams, error } = await useFetch(`${config.public.apiBase}api/teams`, {
  lazy: true,
})
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
      <div v-for="team in teams" :key="team">
        <div v-for="index in team" :key="index">
          <div v-for="value in index" :key="value">
            <NuxtLink :to="`/teams/${value}`">{{ value }}</NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>