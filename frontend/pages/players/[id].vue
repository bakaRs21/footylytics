<script setup>
import { ref } from 'vue';

const config = useRuntimeConfig()
const route = useRoute()
const id = route.params.id

const { data: playerInfo, error: playerInfoError } = await useFetch(`${config.public.apiBase}players/${id}`, {
  lazy: true,
})
const { data: playerSeasons, error: playerSeasonsError } = await useFetch(`${config.public.apiBase}players/${id}/seasons`)

const info = { "age": 35, "name": "Darren Fletcher", "height_in_m": 1.83, "date_of_birth": null, "player_id": 19504, "nation_id": 6, "weight": null }
</script>
<template>
  <div v-if="isLoading">
    <h2 class="pending-design">Loading data... </h2>
    <loading-svg />
  </div>
  <div v-else-if="playerInfoError">
    Error: {{ playerInfoError.message }}
  </div>
  <div v-else>
    <div class="page-heading"> 
      <h1 class="h1-design">You've selected {{ playerInfo.name }}</h1>
    </div>
    {{ playerInfo }}
    
  </div>
</template>