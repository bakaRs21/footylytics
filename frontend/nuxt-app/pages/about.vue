<script setup>
const config = useRuntimeConfig()
const { data, error } = await useFetch(`${config.public.apiBase}`)
console.log(`${config.public.apiBase}/nums`)
</script>

<template>
  <div>
    <h3>Nuxt SSR + FastAPI</h3>
    <div v-if="error">Error: {{ error.message }}</div>
    <pre v-else>{{ data }}</pre>
  </div>
</template>