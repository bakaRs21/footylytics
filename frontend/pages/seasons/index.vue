<script setup>
import LoadingSvg from '~/components/Icons/loading_svg.vue';

const config = useRuntimeConfig()
const { status, data: seasons, error } = await useFetch(`${config.public.apiBase}compare/Seasons`, {
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
    <div v-else v-for="values in seasons" :key="values">
      <div v-for="value in values" :key="value">
        <pre><NuxtLink :to="`/Seasons/${value}`">{{ value }}</NuxtLink></pre>
      </div>
    </div>
  </div>
</template>



<style scoped>
</style>