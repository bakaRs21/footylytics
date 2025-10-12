<script setup>
const config = useRuntimeConfig()
const base = config.public.apiBase
const { data, error } = await useFetch(`${base}/api/hello`)
</script>

<template>
  <div>
    <h1>Nuxt SSR + FastAPI</h1>
    <div v-if="error">Error: {{ error.message }}</div>
    <pre v-else>{{ data }}</pre>
  </div>
</template>