<script setup>
import card from '~/components/card.vue';

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
  <div v-else v-for="team in teams" :key="team">
    <div  class="cards">
      <card v-for="value in team"><NuxtLink :to="`/teams/${value}`">{{ value }}</NuxtLink></card>
    </div>
  </div>
</template>

<style scoped>
</style>