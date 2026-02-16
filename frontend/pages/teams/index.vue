<script setup>

const config = useRuntimeConfig()
const { pending: isLoading, data: teams, error } = await useFetch(`${config.public.apiBase}compare/Teams`, {
  lazy: true,
})
</script>

<template>
  <div class="page-heading"> 
    <h1 class="h1-design">Teams Page</h1>
  </div>
  <div v-if="isLoading">
    <h2 class="pending-design">Loading data... </h2>
    <loading-svg />
  </div>
  <div v-else-if="error">
    Error: {{ error.message }}
  </div>
  <div v-else>
    <SearchableCards :enable-links="true" :items="teams" :page="'team'" placeholder="Search teams..."/>
  </div>
</template>

<style scoped>
</style>