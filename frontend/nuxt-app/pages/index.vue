<script setup>
const config = useRuntimeConfig()
const { data, error } = await useFetch(`${config.public.apiBase}/hello`)
</script>

<template>
  <div>
    <h1>Nuxt SSR + FastAPI</h1>
    <div v-if="error">Error: {{ error.message }}</div>
    <pre v-else>{{ data }}</pre>
  </div>
</template>