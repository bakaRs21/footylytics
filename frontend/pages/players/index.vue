<script setup>
const playerArray = ref([]);
const page = "player";

const config = useRuntimeConfig()
const { pending: isLoading, data: players, error } = await useFetch(`${config.public.apiBase}players/with-seasons-teams`, {
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
  <div v-else>
    <SearchableCards :enable-links="true" :items="players" :page="page" placeholder="Search players..."/>
  </div>
</template>