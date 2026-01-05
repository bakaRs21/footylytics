<script setup>
const playerArray = ref([]);

const config = useRuntimeConfig()
const { pending: isLoading, data: players, error } = await useFetch(`${config.public.apiBase}compare/Players`, {
  lazy: true,
})
</script>
<template>
    <div class="page-heading"> 
    <h1 class="h1-design">Players Page</h1>
  </div>
  <div v-if="isLoading">
    <h2 class="pending-design">Loading data... </h2>
    <loading-svg />
  </div>
  <div v-else-if="error">
    Error: {{ error.message }}
  </div>
  <div v-else v-for="playerArray in players" :key="playerArray">
    <SearchableCards :enable-links="true" :items="playerArray" placeholder="Search players..."/>
  </div>
</template>