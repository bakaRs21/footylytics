<script setup>
import { Icon } from '@iconify/vue';

const config = useRuntimeConfig()
const { pending: isLoading, data: teams, error } = await useFetch(`${config.public.apiBase}teams/with-seasons`, {
  lazy: true,
})
</script>

<template>
  <div class="page-heading"> 
    <h1 class="h1-design">Teams Page</h1>
  </div>
  <div v-if="isLoading">
    <h2 class="pending-design">Loading data... </h2>
    <Icon icon="mdi:loading" />
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