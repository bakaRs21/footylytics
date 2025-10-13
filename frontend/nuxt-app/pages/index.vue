<script setup>
const config = useRuntimeConfig()
const { data, error } = await useFetch(`${config.public.apiBase}/api/hello`)
console.log("API Key:", config.public.apiKey)
</script>

<template>
  <div>
    <h1>Nuxt SSR + FastAPI</h1>
    <div v-if="error">Error: {{ error.message }}</div>
    <pre v-else>{{ data }}</pre><br/>
  </div>
</template>