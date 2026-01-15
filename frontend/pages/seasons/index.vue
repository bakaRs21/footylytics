<script setup>
const config = useRuntimeConfig()
const {status, data: seasons, error } = await useFetch(`${config.public.apiBase}compare/Seasons`, {
  lazy: true,
})
</script>
<template>
  <div class="page-heading">
    <h1 class="h1-design">Seasons Page</h1>
  </div>
  <div>
    <div v-if="status === 'pending'">
      <h2 class="pending-design">Loading data... </h2>
      <LoadingSvg />
    </div>
    <div v-else-if="error">
      Error: {{ error.message }}
    </div>
    <div v-else>
      <SearchableCards :enable-links="true" :items="seasons" :page="'season'" placeholder="Search season" />
    </div>
  </div>
</template>



<style scoped>
</style>