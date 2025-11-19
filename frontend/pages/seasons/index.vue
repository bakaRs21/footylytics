<template>
  <div class="page-heading">
    <h1 class="h1-design">Seasons Page</h1>
  </div>
  <div>
    <div v-if="status === 'pending'">
      Loading...
    </div>
    <div v-else-if="error">
      Error: {{ error.message }}
    </div>
    <div v-else>
      <div v-for="(season, index) in seasons" :key="index">
        <pre><NuxtLink :to="`/teams/${season.year}`">{{ season.year }}</NuxtLink></pre>
      </div>
    </div>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const { status, data:seasons, error } = await useFetch(`${config.public.apiBase}api/seasons`, {
  lazy: true,
})
</script>

<style scoped>
</style>